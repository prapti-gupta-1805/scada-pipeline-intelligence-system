"""
SCADA Pipeline Anomaly Detection
Isolation Forest
"""

import warnings
warnings.filterwarnings("ignore")

import pickle
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# ==============================================================================
# LOAD DATA
# ==============================================================================

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "scada_pipeline.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 80)
print("SCADA ANOMALY DETECTION")
print("=" * 80)

print(df.shape)
print(df.head())

true_labels = df["event_type"].copy()

print(true_labels.value_counts())

# ==============================================================================
# FEATURE ENGINEERING
# ==============================================================================

df["timestamp"] = pd.to_datetime(df["timestamp"])
df["hour"] = df["timestamp"].dt.hour
df["day_of_week"] = df["timestamp"].dt.dayofweek
df["day_of_month"] = df["timestamp"].dt.day

MODEL_FEATURES = [
    "pressure",
    "flow_rate",
    "temperature",
    "valve_status",
    "pump_state",
    "pump_speed",
    "compressor_state",
    "energy_consumption",
]

X_raw = df[MODEL_FEATURES].copy()
y_raw = (true_labels != "normal").astype(int)

df = df.drop(columns=["timestamp", "segment_id", "alarm_triggered", "event_type"], errors="ignore")

# ==============================================================================
# TRAIN / VALIDATION / TEST SPLIT
# ==============================================================================

X_train_raw, X_test_raw, y_train_raw, y_test = train_test_split(
    X_raw,
    y_raw,
    test_size=0.2,
    random_state=42,
    stratify=y_raw,
)

X_train_raw, X_val_raw, y_train_raw, y_val = train_test_split(
    X_train_raw,
    y_train_raw,
    test_size=0.2,
    random_state=42,
    stratify=y_train_raw,
)

# ==============================================================================
# SCALING
# ==============================================================================

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train_raw)
X_val = scaler.transform(X_val_raw)
X_test = scaler.transform(X_test_raw)

# ==============================================================================
# CONTAMINATION SWEEP
# ==============================================================================

def evaluate_predictions(y_true, y_pred):
    accuracy = accuracy_score(y_true, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average="binary", zero_division=0
    )
    return accuracy, precision, recall, f1


def tune_threshold(y_true, anomaly_scores):
    best = None
    for threshold in np.unique(anomaly_scores):
        predictions = (anomaly_scores >= threshold).astype(int)
        accuracy, precision, recall, f1 = evaluate_predictions(y_true, predictions)
        candidate = (f1, precision, recall, accuracy, threshold)
        if best is None or candidate > best:
            best = candidate
    return best


contamination_values = [0.03, 0.05, 0.08, 0.10, 0.12, 0.15, 0.20]
validation_results = []
test_results = []
parameter_grid = [
    {"n_estimators": 200, "max_samples": "auto", "max_features": 1.0, "bootstrap": False},
    {"n_estimators": 300, "max_samples": 0.8, "max_features": 1.0, "bootstrap": False},
    {"n_estimators": 300, "max_samples": 0.8, "max_features": 0.8, "bootstrap": False},
]

for params in parameter_grid:
    for contamination in contamination_values:
        sweep_model = IsolationForest(
            n_estimators=params["n_estimators"],
            contamination=contamination,
            max_samples=params["max_samples"],
            max_features=params["max_features"],
            bootstrap=params["bootstrap"],
            random_state=42,
        )
        sweep_model.fit(X_train)
        val_scores = -sweep_model.decision_function(X_val)
        test_scores_sweep = -sweep_model.decision_function(X_test)
        threshold_f1, threshold_precision, threshold_recall, threshold_accuracy, threshold = tune_threshold(
            y_val,
            val_scores,
        )
        val_pred = (val_scores >= threshold).astype(int)
        test_pred_sweep = (test_scores_sweep >= threshold).astype(int)
        accuracy, precision, recall, f1 = evaluate_predictions(y_val, val_pred)
        test_accuracy_sweep, test_precision_sweep, test_recall_sweep, test_f1_sweep = evaluate_predictions(
            y_test, test_pred_sweep
        )
        validation_results.append(
            {
                "contamination": contamination,
                "n_estimators": params["n_estimators"],
                "max_samples": params["max_samples"],
                "max_features": params["max_features"],
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1": f1,
                "threshold": threshold,
            }
        )
        test_results.append(
            {
                "contamination": contamination,
                "n_estimators": params["n_estimators"],
                "max_samples": params["max_samples"],
                "max_features": params["max_features"],
                "accuracy": test_accuracy_sweep,
                "precision": test_precision_sweep,
                "recall": test_recall_sweep,
                "f1": test_f1_sweep,
                "threshold": threshold,
            }
        )

results_df = pd.DataFrame(validation_results)
test_results_df = pd.DataFrame(test_results)
print("\nContamination Sweep (Validation Set)")
print(results_df.to_string(index=False, float_format=lambda value: f"{value:.4f}"))
print("\nContamination Sweep (Test Set)")
print(test_results_df.to_string(index=False, float_format=lambda value: f"{value:.4f}"))

selected_row = results_df.sort_values(
    by=["f1", "precision", "recall"],
    ascending=[False, False, False],
).iloc[0]

selected_contamination = float(selected_row["contamination"])
selected_threshold = float(selected_row["threshold"])
selected_n_estimators = int(selected_row["n_estimators"])
selected_max_samples = selected_row["max_samples"]
selected_max_features = float(selected_row["max_features"])
print(f"\nSelected contamination: {selected_contamination:.2f}")
print(f"Selected threshold: {selected_threshold:.6f}")
print(f"Selected n_estimators: {selected_n_estimators}")
print(f"Selected max_samples: {selected_max_samples}")
print(f"Selected max_features: {selected_max_features:.2f}")

# ==============================================================================
# TRAIN FINAL MODEL
# ==============================================================================

model = IsolationForest(
    n_estimators=selected_n_estimators,
    contamination=selected_contamination,
    max_samples=selected_max_samples,
    max_features=selected_max_features,
    bootstrap=False,
    random_state=42
)

model.fit(X_train)

# ==============================================================================
# PREDICTIONS
# ==============================================================================

train_scores = -model.decision_function(X_train)
val_scores = -model.decision_function(X_val)
test_scores = -model.decision_function(X_test)

train_pred = (train_scores >= selected_threshold).astype(int)
val_pred = (val_scores >= selected_threshold).astype(int)
test_pred = (test_scores >= selected_threshold).astype(int)

train_accuracy, train_precision, train_recall, train_f1 = evaluate_predictions(y_train_raw, train_pred)
val_accuracy, val_precision, val_recall, val_f1 = evaluate_predictions(y_val, val_pred)
test_accuracy, test_precision, test_recall, test_f1 = evaluate_predictions(y_test, test_pred)

# ==============================================================================
# SAVE MODEL
# ==============================================================================

MODEL_SAVE_PATH = Path(__file__).resolve().parent

with open(MODEL_SAVE_PATH / "anomaly_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open(MODEL_SAVE_PATH / "anomaly_scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)


# ==============================================================================
# SAVE FEATURE STATISTICS
# ==============================================================================

feature_stats = {
    "mean": X_train_raw.mean(),
    "std": X_train_raw.std(),
    "decision_threshold": selected_threshold,
    "selected_contamination": selected_contamination,
    "selected_n_estimators": selected_n_estimators,
    "selected_max_samples": selected_max_samples,
    "selected_max_features": selected_max_features,
}
with open(MODEL_SAVE_PATH / "feature_stats.pkl", "wb") as f:
    pickle.dump(feature_stats, f)

print("✓ Model, scaler and feature statistics saved")

# ==============================================================================
# VISUALIZATIONS
# ==============================================================================

print("\nGenerating visualizations...")

def save_figure(fig, filename):
    fig.tight_layout()
    fig.savefig(MODEL_SAVE_PATH / filename, dpi=300, bbox_inches="tight")
    plt.close(fig)

# ------------------------------------------------------------------------------
# 1. Anomaly Score Distribution
# ------------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(
    test_scores,
    bins=50,
    kde=True,
    color="steelblue",
    ax=ax
)

ax.axvline(
    selected_threshold,
    color="red",
    linestyle="--",
    linewidth=2,
    label="Calibrated Threshold"
)

ax.set_title("Anomaly Score Distribution")
ax.set_xlabel("Anomaly Score")
ax.set_ylabel("Frequency")
ax.legend()
save_figure(fig, "anomaly_score_distribution.png")
print("✓ Saved anomaly_score_distribution.png")

# ------------------------------------------------------------------------------
# 2. PCA Projection
# ------------------------------------------------------------------------------

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_test)

fig, ax = plt.subplots(figsize=(8, 6))
scatter = ax.scatter(
    X_pca[:, 0],
    X_pca[:, 1],
    c=test_pred,
    cmap="coolwarm",
    alpha=0.7
)

ax.set_title("PCA Projection of SCADA Data")
ax.set_xlabel("Principal Component 1")
ax.set_ylabel("Principal Component 2")

legend = ax.legend(*scatter.legend_elements(), title="Prediction")
legend.get_texts()[0].set_text("Normal")
legend.get_texts()[1].set_text("Anomaly")
save_figure(fig, "anomaly_pca_projection.png")
print("✓ Saved anomaly_pca_projection.png")

# ------------------------------------------------------------------------------
# 3. Correlation Heatmap
# ------------------------------------------------------------------------------

corr = X_train_raw.corr()

fig, ax = plt.subplots(figsize=(8, 7))
sns.heatmap(
    corr,
    cmap="coolwarm",
    center=0,
    square=True,
    linewidths=0.3,
    cbar=True,
    ax=ax
)

ax.set_title("Feature Correlation Heatmap")
save_figure(fig, "anomaly_feature_correlation.png")
print("✓ Saved anomaly_feature_correlation.png")

# ------------------------------------------------------------------------------
# 4. Model Summary
# ------------------------------------------------------------------------------

normal = int((test_pred == 0).sum())
anomaly = int((test_pred == 1).sum())

summary = f"""
Isolation Forest Summary

Training Samples : {len(X_train_raw):,}

Validation Samples : {len(X_val_raw):,}

Test Samples : {len(X_test_raw):,}

Test Normal        : {normal:,}

Test Anomalies     : {anomaly:,}

Selected Contamination : {model.contamination}

Decision Threshold : {selected_threshold:.6f}

Test Anomaly Rate  : {(100 * anomaly / len(X_test_raw)):.2f}%

Features      : {len(MODEL_FEATURES)}

Algorithm     : Isolation Forest
"""

fig, ax = plt.subplots(figsize=(8, 6))
ax.axis("off")
ax.text(
    0.02,
    0.98,
    summary,
    fontsize=12,
    va="top",
    family="monospace"
)
ax.set_title("Model Analysis")
save_figure(fig, "anomaly_model_summary.png")
print("✓ Saved anomaly_model_summary.png")

print("\nFinal Metrics (Test Set)")
print(f"Accuracy : {test_accuracy:.4f}")
print(f"Precision: {test_precision:.4f}")
print(f"Recall   : {test_recall:.4f}")
print(f"F1-score : {test_f1:.4f}")

print("\nTest Confusion Matrix")
print(confusion_matrix(y_test, test_pred))
print("\n" + "=" * 80)
print("ANOMALY DETECTION TRAINING COMPLETED")
print("=" * 80)
