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
    confusion_matrix
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

X = df[FEATURE_COLUMNS].copy()

target_encoder = LabelEncoder()

y = target_encoder.fit_transform(df[TARGET_COLUMN])

# ==============================================================================
# LABEL ENCODING
# ==============================================================================

material_encoder = LabelEncoder()
grade_encoder = LabelEncoder()

X["Material"] = material_encoder.fit_transform(
    X["Material"]
)

X["Grade"] = grade_encoder.fit_transform(
    X["Grade"]
)

# ==============================================================================
# TRAIN TEST SPLIT
# ==============================================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42,

    stratify=y

)

print("\nTrain Shape :", X_train.shape)

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

    num_class=3,

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

y_pred = model.predict(X_test)


# ==============================================================================
# MODEL EVALUATION
# ==============================================================================

accuracy = accuracy_score(

    y_test,

    y_pred

)

print("=" * 80)

print(f"Accuracy : {accuracy:.4f}")

print("=" * 80)

print("\nClassification Report\n")

print(

    classification_report(

        y_test,

        y_pred

    )

)

# ==============================================================================
# CONFUSION MATRIX
# ==============================================================================

cm = confusion_matrix(

    y_test,

    y_pred

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