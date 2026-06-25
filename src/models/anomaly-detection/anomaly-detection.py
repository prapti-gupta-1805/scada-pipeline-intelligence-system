"""
SCADA Pipeline Anomaly Detection
Isolation Forest
"""

import warnings
warnings.filterwarnings("ignore")

import pickle

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import IsolationForest
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_PATH = BASE_DIR / "data" / "scada_pipeline.csv"

df = pd.read_csv(DATA_PATH)

print("="*80)
print("SCADA ANOMALY DETECTION")
print("="*80)

print(df.shape)
print(df.head())

true_labels = df["event_type"]

print(true_labels.value_counts())

df["timestamp"] = pd.to_datetime(df["timestamp"])

df["hour"] = df["timestamp"].dt.hour
df["day_of_week"] = df["timestamp"].dt.dayofweek
df["day_of_month"] = df["timestamp"].dt.day

FEATURES = ["segment_id", "pressure", "flow_rate", "temperature", "valve_status", "pump_state", "pump_speed", "compressor_state", "energy_consumption", "alarm_triggered", "hour", "day_of_week", "day_of_month"]

X = df[FEATURES]

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

model = IsolationForest(n_estimators=200, contamination=0.05, random_state=42)

model.fit(X_scaled)

pred = model.predict(X_scaled)

pred = np.where(pred == -1, 1, 0)

df["anomaly"] = pred

scores = model.decision_function(X_scaled)

df["anomaly_score"] = scores

faults = true_labels != "normal"

faults = faults.astype(int)

sns.boxplot(
x=df["anomaly"],
y=df["pressure"]
)

plt.figure(figsize=(10,5))

sns.histplot(df["anomaly_score"],bins=50)

plt.axvline(0,color="red")

plt.title("Anomaly Score Distribution")

pickle.dump(model,open("anomaly_model.pkl","wb"))

pickle.dump(scaler,open("anomaly_scaler.pkl","wb"))

# ==============================================================================
# VISUALIZATIONS
# ==============================================================================

from sklearn.decomposition import PCA

print("\nGenerating visualizations...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# ------------------------------------------------------------------------------
# 1. Anomaly Score Distribution
# ------------------------------------------------------------------------------

sns.histplot(
    df["anomaly_score"],
    bins=50,
    kde=True,
    ax=axes[0, 0],
    color="steelblue"
)

axes[0, 0].axvline(
    0,
    color="red",
    linestyle="--",
    linewidth=2,
    label="Decision Boundary"
)

axes[0, 0].set_title("Anomaly Score Distribution")
axes[0, 0].set_xlabel("Anomaly Score")
axes[0, 0].legend()

# ------------------------------------------------------------------------------
# 2. PCA Visualization
# ------------------------------------------------------------------------------

pca = PCA(n_components=2)

X_pca = pca.fit_transform(X_scaled)

scatter = axes[0, 1].scatter(

    X_pca[:, 0],

    X_pca[:, 1],

    c=df["anomaly"],

    cmap="coolwarm",

    alpha=0.7

)

axes[0, 1].set_title("PCA Projection of SCADA Data")
axes[0, 1].set_xlabel("Principal Component 1")
axes[0, 1].set_ylabel("Principal Component 2")

legend = axes[0, 1].legend(
    *scatter.legend_elements(),
    title="Prediction"
)

legend.get_texts()[0].set_text("Normal")
legend.get_texts()[1].set_text("Anomaly")

# ------------------------------------------------------------------------------
# 3. Correlation Heatmap
# ------------------------------------------------------------------------------

corr = df[FEATURES].corr()

sns.heatmap(

    corr,

    cmap="coolwarm",

    center=0,

    square=True,

    linewidths=0.3,

    cbar=True,

    ax=axes[1, 0]

)

axes[1, 0].set_title("Feature Correlation Heatmap")

# ------------------------------------------------------------------------------
# 4. Detection Summary
# ------------------------------------------------------------------------------

normal = (df["anomaly"] == 0).sum()
anomaly = (df["anomaly"] == 1).sum()

summary = f"""
Isolation Forest

Samples:
{len(df):,}

Normal:
{normal:,}

Anomalies:
{anomaly:,}

Anomaly Rate:
{100*anomaly/len(df):.2f}%

Contamination:
{model.contamination}

Features:
{len(FEATURES)}
"""

axes[1, 1].axis("off")

axes[1, 1].text(

    0.02,

    0.98,

    summary,

    fontsize=12,

    va="top",

    family="monospace"

)

axes[1, 1].set_title("Model Analysis")

plt.tight_layout()

plt.savefig(

    "anomaly_analysis.png",

    dpi=300,

    bbox_inches="tight"

)

plt.close()

print("✓ Saved anomaly_analysis.png")

# ==============================================================================
# SAVE FEATURE STATISTICS
# ==============================================================================

feature_stats = {
    "mean": X.mean(),
    "std": X.std()
}

with open("feature_stats.pkl", "wb") as f:
    pickle.dump(feature_stats, f)

print("✓ Feature statistics saved")

# ==============================================================================
# VISUALIZATIONS
# ==============================================================================

from sklearn.decomposition import PCA

print("\nGenerating visualizations...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# ------------------------------------------------------------------------------
# 1. Anomaly Score Distribution
# ------------------------------------------------------------------------------

sns.histplot(
    df["anomaly_score"],
    bins=50,
    kde=True,
    ax=axes[0, 0],
    color="steelblue"
)

axes[0, 0].axvline(
    0,
    color="red",
    linestyle="--",
    linewidth=2,
    label="Decision Boundary"
)

axes[0, 0].set_title("Anomaly Score Distribution")
axes[0, 0].set_xlabel("Anomaly Score")
axes[0, 0].set_ylabel("Frequency")
axes[0, 0].legend()

# ------------------------------------------------------------------------------
# 2. PCA Projection
# ------------------------------------------------------------------------------

pca = PCA(n_components=2)

X_pca = pca.fit_transform(X_scaled)

scatter = axes[0, 1].scatter(

    X_pca[:, 0],

    X_pca[:, 1],

    c=df["anomaly"],

    cmap="coolwarm",

    alpha=0.7

)

axes[0, 1].set_title("PCA Projection of SCADA Data")
axes[0, 1].set_xlabel("Principal Component 1")
axes[0, 1].set_ylabel("Principal Component 2")

legend = axes[0, 1].legend(
    *scatter.legend_elements(),
    title="Prediction"
)

legend.get_texts()[0].set_text("Normal")
legend.get_texts()[1].set_text("Anomaly")

# ------------------------------------------------------------------------------
# 3. Correlation Heatmap
# ------------------------------------------------------------------------------

corr = df[FEATURES].corr()

sns.heatmap(

    corr,

    cmap="coolwarm",

    center=0,

    square=True,

    linewidths=0.3,

    cbar=True,

    ax=axes[1, 0]

)

axes[1, 0].set_title("Feature Correlation Heatmap")

# ------------------------------------------------------------------------------
# 4. Model Analysis
# ------------------------------------------------------------------------------

normal = (df["anomaly"] == 0).sum()
anomaly = (df["anomaly"] == 1).sum()

summary = f"""
Isolation Forest Summary

Total Samples : {len(df):,}

Normal : {normal:,}

Anomalies : {anomaly:,}

Anomaly Rate : {(100 * anomaly / len(df)):.2f}%

Contamination : {model.contamination}

Features : {len(FEATURES)}

Algorithm : Isolation Forest
"""

axes[1, 1].axis("off")

axes[1, 1].text(

    0.02,

    0.98,

    summary,

    fontsize=12,

    va="top",

    family="monospace"

)

axes[1, 1].set_title("Model Analysis")

plt.tight_layout()

plt.savefig(

    "anomaly_analysis.png",

    dpi=300,

    bbox_inches="tight"

)

plt.close()

print("✓ Saved anomaly_analysis.png")