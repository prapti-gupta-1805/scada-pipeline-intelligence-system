"""
SCADA Pipeline Fault Classification Model
Multi-class Classification using XGBoost with SHAP Explainability
Classes: Normal, Leak, Blockage, Surge, Degradation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import (classification_report, confusion_matrix, accuracy_score, 
                             precision_recall_fscore_support, roc_auc_score, roc_curve, auc)
import xgboost as xgb
import shap
from pathlib import Path
import sys
import warnings
warnings.filterwarnings('ignore')

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Set style for better visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

# ============================================================================
# 1. DATA LOADING AND EXPLORATION
# ============================================================================

print("=" * 80)
print("SCADA PIPELINE FAULT CLASSIFICATION - XGBoost with SHAP")
print("=" * 80)

# Load data
script_dir = Path(__file__).resolve().parent
repo_root = Path(__file__).resolve().parents[2]
data_path = repo_root / 'data' / 'scada_pipeline.csv'
df = pd.read_csv(data_path)
print(f"\nDataset shape: {df.shape}")
print(f"\nFirst few rows:")
print(df.head())
print(f"\nData types:\n{df.dtypes}")
print(f"\nMissing values:\n{df.isnull().sum()}")

# ============================================================================
# 2. DATA PREPROCESSING
# ============================================================================

print("\n" + "=" * 80)
print("DATA PREPROCESSING")
print("=" * 80)

# Analyze target variable
print(f"\nTarget variable distribution:")
print(df['target'].value_counts())
print(f"\nEvent type distribution:")
event_labels = df['event_type'].copy()
print(event_labels.value_counts())

# Create a mapping from event_type to class labels
event_to_class = {
    'normal': 0,
    'leak': 1,
    'blockage': 2,
    'surge': 3,
    'degradation': 4
}

# Use event_type as the primary target (more descriptive)
df['class_label'] = event_labels.map(event_to_class)
df['class_name'] = event_labels

print(f"\nClass distribution:")
for class_name, class_idx in event_to_class.items():
    count = (df['class_label'] == class_idx).sum()
    pct = count / len(df) * 100
    print(f"  {class_name.capitalize():15} (Class {class_idx}): {count:5} samples ({pct:5.1f}%)")

# ============================================================================
# 3. FEATURE ENGINEERING & SELECTION
# ============================================================================

print("\n" + "=" * 80)
print("FEATURE ENGINEERING")
print("=" * 80)

# Convert timestamp to datetime features
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['hour'] = df['timestamp'].dt.hour
df['day_of_week'] = df['timestamp'].dt.dayofweek
df['day_of_month'] = df['timestamp'].dt.day

# Select features for the model after removing the excluded telemetry fields
feature_cols = ['pressure', 'flow_rate', 'temperature',
                'valve_status', 'pump_state', 'pump_speed', 'compressor_state',
                'energy_consumption', 'hour', 'day_of_week', 'day_of_month']

X = df[feature_cols].copy()
y = df['class_label'].copy()

df = df.drop(columns=['timestamp', 'segment_id', 'alarm_triggered', 'event_type'], errors='ignore')

print(f"\nFeatures selected: {len(feature_cols)}")
print(f"Features: {feature_cols}")
print(f"\nFeature statistics:")
print(X.describe())

# ============================================================================
# 4. TRAIN / VALIDATION / TEST SPLIT
# ============================================================================

print("\n" + "=" * 80)
print("TRAIN-TEST SPLIT")
print("=" * 80)

X_train_raw, X_test_raw, y_train_raw, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

X_train_raw, X_val_raw, y_train, y_val = train_test_split(
    X_train_raw,
    y_train_raw,
    test_size=0.2,
    random_state=42,
    stratify=y_train_raw,
)

print(f"\nTraining set size: {X_train_raw.shape[0]}")
print(f"Validation set size: {X_val_raw.shape[0]}")
print(f"Test set size: {X_test_raw.shape[0]}")
print(f"\nClass distribution in training set:")
print(y_train.value_counts().sort_index())
print(f"\nClass distribution in validation set:")
print(y_val.value_counts().sort_index())
print(f"\nClass distribution in test set:")
print(y_test.value_counts().sort_index())

# Scale numerical features
scaler = StandardScaler()
X_train = pd.DataFrame(
    scaler.fit_transform(X_train_raw),
    columns=X_train_raw.columns,
    index=X_train_raw.index,
)
X_val = pd.DataFrame(
    scaler.transform(X_val_raw),
    columns=X_val_raw.columns,
    index=X_val_raw.index,
)
X_test = pd.DataFrame(
    scaler.transform(X_test_raw),
    columns=X_test_raw.columns,
    index=X_test_raw.index,
)

# ============================================================================
# 5. XGBOOST MODEL TRAINING
# ============================================================================

print("\n" + "=" * 80)
print("XGBOOST MODEL TRAINING")
print("=" * 80)

# Determine number of classes
n_classes = len(np.unique(y))
print(f"\nNumber of classes: {n_classes}")

# XGBoost parameters
xgb_params = {
    'max_depth': 6,
    'learning_rate': 0.1,
    'n_estimators': 200,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'objective': 'multi:softprob',
    'num_class': n_classes,
    'random_state': 42,
    'verbosity': 0
}

print(f"\nXGBoost Parameters:")
for param, value in xgb_params.items():
    print(f"  {param}: {value}")

# Train model
model = xgb.XGBClassifier(**xgb_params)
model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)

print(f"\nModel training completed!")

# ============================================================================
# 6. MODEL EVALUATION
# ============================================================================

print("\n" + "=" * 80)
print("MODEL EVALUATION")
print("=" * 80)

# Predictions
y_pred_train = model.predict(X_train)
y_pred_val = model.predict(X_val)
y_pred_test = model.predict(X_test)
y_pred_proba_test = model.predict_proba(X_test)

# Accuracy
train_accuracy = accuracy_score(y_train, y_pred_train)
val_accuracy = accuracy_score(y_val, y_pred_val)
test_accuracy = accuracy_score(y_test, y_pred_test)

train_precision, train_recall, train_f1, _ = precision_recall_fscore_support(
    y_train, y_pred_train, average='macro', zero_division=0
)
val_precision, val_recall, val_f1, _ = precision_recall_fscore_support(
    y_val, y_pred_val, average='macro', zero_division=0
)
test_precision, test_recall, test_f1, _ = precision_recall_fscore_support(
    y_test, y_pred_test, average='macro', zero_division=0
)

print(f"\nAccuracy:")
print(f"  Training Set:   {train_accuracy:.4f}")
print(f"  Validation Set: {val_accuracy:.4f}")
print(f"  Test Set:       {test_accuracy:.4f}")

print(f"\nMacro Metrics:")
print(f"  Training Set -> Precision: {train_precision:.4f}, Recall: {train_recall:.4f}, F1: {train_f1:.4f}")
print(f"  Validation Set -> Precision: {val_precision:.4f}, Recall: {val_recall:.4f}, F1: {val_f1:.4f}")
print(f"  Test Set -> Precision: {test_precision:.4f}, Recall: {test_recall:.4f}, F1: {test_f1:.4f}")

# Detailed classification report
print(f"\nClassification Report (Test Set):")
class_names = ['Normal', 'Leak', 'Blockage', 'Surge', 'Degradation']
print(classification_report(y_test, y_pred_test, target_names=class_names, digits=4))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred_test)
print(f"\nConfusion Matrix:")
print(cm)

# ============================================================================
# 7. FEATURE IMPORTANCE (XGBoost)
# ============================================================================

print("\n" + "=" * 80)
print("FEATURE IMPORTANCE (XGBoost)")
print("=" * 80)

feature_importance = pd.DataFrame({
    'feature': feature_cols,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print(f"\nTop 10 Features by Importance:")
print(feature_importance.head(10).to_string(index=False))

# ============================================================================
# 8. SHAP EXPLAINABILITY
# ============================================================================

print("\n" + "=" * 80)
print("SHAP EXPLAINABILITY ANALYSIS")
print("=" * 80)

print("\nCalculating SHAP values... (This may take a moment)")

# Create SHAP explainer with a smaller sample for speed
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

print("SHAP values calculated successfully!")

# ============================================================================
# 9. VISUALIZATIONS
# ============================================================================

print("\n" + "=" * 80)
print("GENERATING VISUALIZATIONS")
print("=" * 80)

output_dir = script_dir


def save_figure(fig, filename):
    fig.tight_layout()
    fig.savefig(output_dir / filename, dpi=300, bbox_inches='tight')
    plt.close(fig)

# 1. Confusion Matrix
fig, ax = plt.subplots(figsize=(7, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=class_names, yticklabels=class_names, ax=ax)
ax.set_title('Confusion Matrix - Test Set', fontsize=14, fontweight='bold')
ax.set_ylabel('True Label')
ax.set_xlabel('Predicted Label')
save_figure(fig, 'fault_confusion_matrix.png')
print("\nSaved: fault_confusion_matrix.png")

# 2. Feature Importance
fig, ax = plt.subplots(figsize=(8, 6))
top_features = feature_importance.head(10)
sns.barplot(data=top_features, x='importance', y='feature', ax=ax, palette='Blues_r')
ax.set_xlabel('Importance Score')
ax.set_title('Top 10 Feature Importance (XGBoost)', fontsize=14, fontweight='bold')
ax.invert_yaxis()
save_figure(fig, 'fault_feature_importance.png')
print("Saved: fault_feature_importance.png")

# 3. Class Distribution
fig, ax = plt.subplots(figsize=(7, 5))
class_dist = y.value_counts().sort_index()
bars = ax.bar(class_names, [class_dist[i] for i in range(n_classes)],
              color=['#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', '#e67e22'])
ax.set_ylabel('Count')
ax.set_title('Class Distribution', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}', ha='center', va='bottom')
save_figure(fig, 'fault_class_distribution.png')
print("Saved: fault_class_distribution.png")

# 4. Accuracy Comparison
fig, ax = plt.subplots(figsize=(6, 4))
datasets = ['Training', 'Validation', 'Test']
accuracies = [train_accuracy, val_accuracy, test_accuracy]
bars = ax.bar(datasets, accuracies, color=['#3498db', '#f39c12', '#e74c3c'])
ax.set_ylabel('Accuracy')
ax.set_ylim([0, 1])
ax.set_title('Model Accuracy', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
for bar, acc in zip(bars, accuracies):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{acc:.4f}', ha='center', va='bottom')
save_figure(fig, 'fault_accuracy_comparison.png')
print("Saved: fault_accuracy_comparison.png")

# 5. SHAP Summary
fig = plt.figure(figsize=(10, 6))
if isinstance(shap_values, list):
    shap.summary_plot(shap_values, X_test, show=False)
else:
    shap.summary_plot(shap_values, X_test, show=False)
save_figure(fig, 'fault_shap_summary.png')
print("Saved: fault_shap_summary.png")

# ============================================================================
# 10. SAMPLE PREDICTIONS WITH SHAP EXPLANATION
# ============================================================================

print("\n" + "=" * 80)
print("SAMPLE PREDICTIONS WITH SHAP EXPLANATIONS")
print("=" * 80)

# Select interesting samples
sample_indices = [0, 50, 100, 150, 200]
sample_indices = [idx for idx in sample_indices if idx < len(X_test)]

for idx in sample_indices:
    sample = X_test.iloc[idx:idx+1]
    pred_prob = model.predict_proba(sample)[0]
    pred_class = model.predict(sample)[0]
    
    print(f"\nSample {idx}:")
    print(f"  True Class: {class_names[y_test.iloc[idx]]}")
    print(f"  Predicted Class: {class_names[pred_class]}")
    print(f"  Prediction Confidence: {max(pred_prob):.4f}")
    print(f"  Class Probabilities:")
    for i, prob in enumerate(pred_prob):
        print(f"    {class_names[i]:15}: {prob:.4f}")
    
    # Get SHAP values for this sample
    if isinstance(shap_values, list):
        sample_shap = [sv[idx] for sv in shap_values]
        top_shap_idx = np.abs(sample_shap[pred_class]).argsort()[-3:][::-1]
    else:
        sample_shap_vals = shap_values[idx]
        if sample_shap_vals.ndim == 2:
            sample_shap_vals = sample_shap_vals[:, pred_class]
        top_shap_idx = np.abs(sample_shap_vals).argsort()[-3:][::-1]
    
    print(f"  Top 3 Contributing Features:")
    for rank, feat_idx in enumerate(top_shap_idx, 1):
        feature = feature_cols[feat_idx]
        if isinstance(shap_values, list):
            shap_val = sample_shap[pred_class][feat_idx]
        else:
            if shap_values.ndim == 3:
                shap_val = shap_values[idx, feat_idx, pred_class]
            else:
                shap_val = shap_values[idx, feat_idx]
        print(f"    {rank}. {feature:20} (SHAP: {shap_val:+.4f})")

# ============================================================================
# 11. SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("MODEL SUMMARY")
print("=" * 80)
print(f"\n✓ Model Type: XGBoost Classifier")
print(f"✓ Number of Classes: {n_classes}")
print(f"✓ Test Set Accuracy: {test_accuracy:.4f}")
print(f"✓ Training Samples: {len(X_train)}")
print(f"✓ Test Samples: {len(X_test)}")
print(f"✓ Number of Features: {len(feature_cols)}")
print(f"✓ Explainability Method: SHAP")
print(f"\n✓ Outputs Generated:")
print(f"  - scada_model_analysis.png (comprehensive visualizations)")
print(f"  - Model pickle file: scada_model.pkl (to be saved)")
print(f"  - Scaler pickle file: scaler.pkl (to be saved)")

# Save the model and scaler
import pickle
with open(script_dir / 'scada_model.pkl', 'wb') as f:
    pickle.dump(model, f)
with open(script_dir / 'scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
    
print(f"\n✓ Model and scaler saved successfully!")
print("\n" + "=" * 80)
