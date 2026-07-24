"""
Pipeline Predictive Maintenance
XGBoost Multi-Class Classification
"""

import warnings
warnings.filterwarnings("ignore")

import pickle
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import shap

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support
)
from sklearn.preprocessing import LabelEncoder

from xgboost import XGBClassifier

# ==============================================================================
# LOAD DATA
# ==============================================================================

BASE_DIR = Path(__file__).resolve().parents[3]
MODEL_SAVE_PATH = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "market_pipe_thickness_loss_dataset.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 80)
print("PIPELINE PREDICTIVE MAINTENANCE")
print("=" * 80)

print(df.shape)
print(df.head())

# ==============================================================================
# DATA OVERVIEW
# ==============================================================================

print("\nDataset Information\n")

print(df.info())

print("\nMissing Values\n")

print(df.isnull().sum())

print("\nTarget Distribution\n")

print(df["Condition"].value_counts())

# ==============================================================================
# FEATURE ENGINEERING
# ==============================================================================

FEATURE_COLUMNS = [

    "Pipe_Size_mm",
    "Thickness_mm",
    "Material",
    "Grade",
    "Max_Pressure_psi",
    "Temperature_C",
    "Corrosion_Impact_Percent",
    "Thickness_Loss_mm",
    "Material_Loss_Percent",
    "Time_Years"

]

TARGET_COLUMN = "Condition"

X_raw = df[FEATURE_COLUMNS].copy()
y_raw = df[TARGET_COLUMN].copy()

# ==============================================================================
# LABEL ENCODING
# ==============================================================================

# ==============================================================================
# TRAIN TEST SPLIT
# ==============================================================================

X_train_raw, X_test_raw, y_train_raw, y_test_raw = train_test_split(
    X_raw,
    y_raw,
    test_size=0.20,
    random_state=42,
    stratify=y_raw
)

X_train_raw, X_val_raw, y_train_raw, y_val_raw = train_test_split(
    X_train_raw,
    y_train_raw,
    test_size=0.20,
    random_state=42,
    stratify=y_train_raw
)

target_encoder = LabelEncoder()
y_train = target_encoder.fit_transform(y_train_raw)
y_val = target_encoder.transform(y_val_raw)
y_test = target_encoder.transform(y_test_raw)

material_encoder = LabelEncoder()
grade_encoder = LabelEncoder()

X_train = X_train_raw.copy()
X_val = X_val_raw.copy()
X_test = X_test_raw.copy()

X_train["Material"] = material_encoder.fit_transform(X_train["Material"])
X_val["Material"] = material_encoder.transform(X_val["Material"])
X_test["Material"] = material_encoder.transform(X_test["Material"])

X_train["Grade"] = grade_encoder.fit_transform(X_train["Grade"])
X_val["Grade"] = grade_encoder.transform(X_val["Grade"])
X_test["Grade"] = grade_encoder.transform(X_test["Grade"])

print("\nTrain Shape :", X_train.shape)

print("Validation Shape :", X_val.shape)

print("Test Shape  :", X_test.shape)

print("\nData preprocessing completed.")

print("=" * 80)
# ==============================================================================
# TRAIN XGBOOST MODEL
# ==============================================================================

model = XGBClassifier(

    n_estimators=300,

    max_depth=6,

    learning_rate=0.05,

    subsample=0.8,

    colsample_bytree=0.8,

    objective="multi:softprob",

    num_class=len(target_encoder.classes_),

    eval_metric="mlogloss",

    random_state=42

)

print("\nTraining XGBoost model...\n")

model.fit(

    X_train,

    y_train

)

print("✓ Training completed.")

# ==============================================================================
# MODEL PREDICTIONS
# ==============================================================================

y_pred_train = model.predict(X_train)
y_pred_val = model.predict(X_val)
y_pred_test = model.predict(X_test)


# ==============================================================================
# MODEL EVALUATION
# ==============================================================================

train_accuracy = accuracy_score(y_train, y_pred_train)
val_accuracy = accuracy_score(y_val, y_pred_val)
accuracy = accuracy_score(y_test, y_pred_test)

train_precision, train_recall, train_f1, _ = precision_recall_fscore_support(
    y_train, y_pred_train, average="macro", zero_division=0
)
val_precision, val_recall, val_f1, _ = precision_recall_fscore_support(
    y_val, y_pred_val, average="macro", zero_division=0
)
test_precision, test_recall, test_f1, _ = precision_recall_fscore_support(
    y_test, y_pred_test, average="macro", zero_division=0
)

print("=" * 80)

print(f"Accuracy : {accuracy:.4f}")
print(f"Train Accuracy : {train_accuracy:.4f}")
print(f"Validation Accuracy : {val_accuracy:.4f}")
print(f"Train Macro P/R/F1 : {train_precision:.4f} / {train_recall:.4f} / {train_f1:.4f}")
print(f"Validation Macro P/R/F1 : {val_precision:.4f} / {val_recall:.4f} / {val_f1:.4f}")
print(f"Test Macro P/R/F1 : {test_precision:.4f} / {test_recall:.4f} / {test_f1:.4f}")

print("=" * 80)

print("\nClassification Report\n")

print(

    classification_report(

        y_test,

        y_pred_test,
        target_names=target_encoder.classes_

    )

)

# ==============================================================================
# CONFUSION MATRIX
# ==============================================================================

cm = confusion_matrix(

    y_test,

    y_pred_test

)

print("\nConfusion Matrix\n")

print(cm)

# ==============================================================================
# SAVE MODEL
# ==============================================================================

with open(

    MODEL_SAVE_PATH / "maintenance_model.pkl",

    "wb"

) as f:

    pickle.dump(model, f)

with open(

    MODEL_SAVE_PATH / "material_encoder.pkl",

    "wb"

) as f:

    pickle.dump(material_encoder, f)

with open(
    MODEL_SAVE_PATH / "grade_encoder.pkl",
    "wb"
) as f:
    pickle.dump(grade_encoder, f)


with open(

    MODEL_SAVE_PATH / "target_encoder.pkl",

    "wb"

) as f:

    pickle.dump(target_encoder, f)

print("\n✓ Model saved")

print("✓ Material encoder saved")
print("✓ Grade encoder saved")
print("✓ Target encoder saved")

print("=" * 80)


# ==============================================================================
# SAVE CONFUSION MATRIX
# ==============================================================================

plt.figure(figsize=(6,5))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=target_encoder.classes_,
    yticklabels=target_encoder.classes_,
)

plt.title("Confusion Matrix")

plt.xlabel("Predicted")

plt.ylabel("Actual")

plt.tight_layout()

plt.savefig(
    MODEL_SAVE_PATH / "confusion_matrix.png",
    dpi=300
)

plt.close()

print("✓ Saved confusion_matrix.png")

# ==============================================================================
# SHAP EXPLAINABILITY
# ==============================================================================

print("\nGenerating SHAP explanations...")

explainer = shap.TreeExplainer(model)

shap_values = explainer(X_test).values

# ==============================================================================
# VISUALIZATIONS
# ==============================================================================

print("Generating visualizations...")

fig, axes = plt.subplots(2, 2, figsize=(18, 14))

# ------------------------------------------------------------------------------
# 1. Confusion Matrix
# ------------------------------------------------------------------------------

sns.heatmap(

    cm,

    annot=True,

    fmt="d",

    cmap="Blues",

    cbar=False,

    xticklabels=target_encoder.classes_,

    yticklabels=target_encoder.classes_,

    ax=axes[0,0]

)

axes[0,0].set_title("Confusion Matrix")

axes[0,0].set_xlabel("Predicted")

axes[0,0].set_ylabel("Actual")

# ------------------------------------------------------------------------------
# 2. Feature Importance
# ------------------------------------------------------------------------------

importance = pd.DataFrame({

    "Feature": FEATURE_COLUMNS,

    "Importance": model.feature_importances_

})

importance = importance.sort_values(

    by="Importance",

    ascending=False

)

sns.barplot(

    data=importance,

    x="Importance",

    y="Feature",

    ax=axes[0,1]

)

axes[0,1].set_title("XGBoost Feature Importance")

# ------------------------------------------------------------------------------
# 3. SHAP Feature Importance
# ------------------------------------------------------------------------------

print("SHAP values shape:", np.array(shap_values).shape)

# Handle different SHAP output formats
if isinstance(shap_values, list):

    # Older SHAP: list of arrays (one per class)
    mean_shap = np.mean(
        [np.abs(sv).mean(axis=0) for sv in shap_values],
        axis=0
    )

else:

    shap_values = np.array(shap_values)

    if shap_values.ndim == 3:

        # (samples, features, classes)
        if shap_values.shape[1] == len(FEATURE_COLUMNS):

            mean_shap = np.abs(shap_values).mean(axis=(0, 2))

        # (classes, samples, features)
        elif shap_values.shape[2] == len(FEATURE_COLUMNS):

            mean_shap = np.abs(shap_values).mean(axis=(0, 1))

        else:

            raise ValueError(
                f"Unexpected SHAP shape: {shap_values.shape}"
            )

    else:

        # Binary / regression
        mean_shap = np.abs(shap_values).mean(axis=0)

shap_df = pd.DataFrame({

    "Feature": FEATURE_COLUMNS,

    "SHAP": mean_shap

})

shap_df = shap_df.sort_values(

    by="SHAP",

    ascending=False

)

sns.barplot(

    data=shap_df,

    x="SHAP",

    y="Feature",

    ax=axes[1,0]

)

axes[1,0].set_title("Mean Absolute SHAP Values")
# ------------------------------------------------------------------------------
# 4. Model Summary
# ------------------------------------------------------------------------------

summary = f"""
Predictive Maintenance

Samples : {len(df):,}

Training : {len(X_train):,}

Testing : {len(X_test):,}

Accuracy : {accuracy:.4f}

Algorithm : XGBoost

Trees : {model.n_estimators}

Features : {len(FEATURE_COLUMNS)}

Target :

Condition
"""

axes[1,1].axis("off")

axes[1,1].text(

    0.02,

    0.98,

    summary,

    fontsize=12,

    va="top",

    family="monospace"

)

axes[1,1].set_title("Model Analysis")

plt.tight_layout()

plt.savefig(

    MODEL_SAVE_PATH / "maintenance_analysis.png",

    dpi=300,

    bbox_inches="tight"

)

plt.close()

print("✓ Saved maintenance_analysis.png")

# ==============================================================================
# SHAP SUMMARY PLOT
# ==============================================================================

plt.figure(figsize=(10,6))

if isinstance(shap_values, list):

    shap.summary_plot(
        shap_values,
        X_test,
        show=False
    )

elif np.array(shap_values).ndim == 3:

    shap.summary_plot(
        shap_values[:, :, 0],
        X_test,
        show=False
    )

else:

    shap.summary_plot(
        shap_values,
        X_test,
        show=False
    )

plt.tight_layout()

plt.savefig(

    MODEL_SAVE_PATH / "shap_summary.png",

    dpi=300,

    bbox_inches="tight"

)

plt.close()

print("✓ Saved shap_summary.png")

# ==============================================================================
# SAVE SEPARATE PLOT ARTIFACTS
# ============================================================================== 

fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    cbar=False,
    xticklabels=target_encoder.classes_,
    yticklabels=target_encoder.classes_,
    ax=ax,
)
ax.set_title("Confusion Matrix")
ax.set_xlabel("Predicted")
ax.set_ylabel("Actual")
fig.tight_layout()
fig.savefig(MODEL_SAVE_PATH / "maintenance_confusion_matrix.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print("✓ Saved maintenance_confusion_matrix.png")

importance = pd.DataFrame({
    "Feature": FEATURE_COLUMNS,
    "Importance": model.feature_importances_
})
importance = importance.sort_values(by="Importance", ascending=False)

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(data=importance, x="Importance", y="Feature", ax=ax)
ax.set_title("XGBoost Feature Importance")
fig.tight_layout()
fig.savefig(MODEL_SAVE_PATH / "maintenance_feature_importance.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print("✓ Saved maintenance_feature_importance.png")

if isinstance(shap_values, list):
    mean_shap = np.mean([np.abs(sv).mean(axis=0) for sv in shap_values], axis=0)
else:
    shap_values = np.array(shap_values)
    if shap_values.ndim == 3:
        if shap_values.shape[1] == len(FEATURE_COLUMNS):
            mean_shap = np.abs(shap_values).mean(axis=(0, 2))
        elif shap_values.shape[2] == len(FEATURE_COLUMNS):
            mean_shap = np.abs(shap_values).mean(axis=(0, 1))
        else:
            raise ValueError(f"Unexpected SHAP shape: {shap_values.shape}")
    else:
        mean_shap = np.abs(shap_values).mean(axis=0)

shap_df = pd.DataFrame({"Feature": FEATURE_COLUMNS, "SHAP": mean_shap})
shap_df = shap_df.sort_values(by="SHAP", ascending=False)

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(data=shap_df, x="SHAP", y="Feature", ax=ax)
ax.set_title("Mean Absolute SHAP Values")
fig.tight_layout()
fig.savefig(MODEL_SAVE_PATH / "maintenance_shap_feature_importance.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print("✓ Saved maintenance_shap_feature_importance.png")

summary = f"""
Predictive Maintenance

Samples : {len(df):,}

Training : {len(X_train):,}

Testing : {len(X_test):,}

Accuracy : {accuracy:.4f}

Algorithm : XGBoost

Trees : {model.n_estimators}

Features : {len(FEATURE_COLUMNS)}

Target :

Condition
"""

fig, ax = plt.subplots(figsize=(8, 6))
ax.axis("off")
ax.text(0.02, 0.98, summary, fontsize=12, va="top", family="monospace")
ax.set_title("Model Analysis")
fig.tight_layout()
fig.savefig(MODEL_SAVE_PATH / "maintenance_model_summary.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print("✓ Saved maintenance_model_summary.png")

# SAVE SHAP EXPLAINER
# ==============================================================================

with open(

    MODEL_SAVE_PATH / "shap_explainer.pkl",

    "wb"

) as f:

    pickle.dump(explainer, f)

print("✓ SHAP explainer saved")

print("\n" + "=" * 80)
print("PREDICTIVE MAINTENANCE TRAINING COMPLETED")
print("=" * 80)
