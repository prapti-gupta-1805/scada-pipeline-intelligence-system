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
import warnings
warnings.filterwarnings('ignore')

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
data_path = script_dir.parent.parent / 'data' / 'scada_pipeline.csv'
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
print(df['event_type'].value_counts())

# Create a mapping from event_type to class labels
event_to_class = {
    'normal': 0,
    'leak': 1,
    'blockage': 2,
    'surge': 3,
    'degradation': 4
}

# Use event_type as the primary target (more descriptive)
df['class_label'] = df['event_type'].map(event_to_class)
df['class_name'] = df['event_type']

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

# Select features for the model (exclude identifiers and target)
feature_cols = ['segment_id', 'pressure', 'flow_rate', 'temperature', 
                'valve_status', 'pump_state', 'pump_speed', 'compressor_state',
                'energy_consumption', 'alarm_triggered', 'hour', 'day_of_week', 'day_of_month']

X = df[feature_cols].copy()
y = df['class_label'].copy()

print(f"\nFeatures selected: {len(feature_cols)}")
print(f"Features: {feature_cols}")
print(f"\nFeature statistics:")
print(X.describe())

# ============================================================================
# 4. TRAIN-TEST SPLIT
# ============================================================================

print("\n" + "=" * 80)
print("TRAIN-TEST SPLIT")
print("=" * 80)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\nTraining set size: {X_train.shape[0]}")
print(f"Test set size: {X_test.shape[0]}")
print(f"\nClass distribution in training set:")
print(y_train.value_counts().sort_index())
print(f"\nClass distribution in test set:")
print(y_test.value_counts().sort_index())

# Scale numerical features
scaler = StandardScaler()
X_train = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns, index=X_train.index)
X_test = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns, index=X_test.index)

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
model.fit(X_train, y_train, eval_set=[(X_test, y_test)], 
          verbose=False)

print(f"\nModel training completed!")

# ============================================================================
# 6. MODEL EVALUATION
# ============================================================================

print("\n" + "=" * 80)
print("MODEL EVALUATION")
print("=" * 80)

# Predictions
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)
y_pred_proba_test = model.predict_proba(X_test)

# Accuracy
train_accuracy = accuracy_score(y_train, y_pred_train)
test_accuracy = accuracy_score(y_test, y_pred_test)

print(f"\nAccuracy:")
print(f"  Training Set: {train_accuracy:.4f}")
print(f"  Test Set: {test_accuracy:.4f}")

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

fig = plt.figure(figsize=(20, 28))

# 1. Confusion Matrix Heatmap
ax1 = plt.subplot(5, 2, 1)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=class_names, yticklabels=class_names, ax=ax1)
ax1.set_title('Confusion Matrix - Test Set', fontsize=14, fontweight='bold')
ax1.set_ylabel('True Label')
ax1.set_xlabel('Predicted Label')

# 2. Feature Importance
ax2 = plt.subplot(5, 2, 2)
top_features = feature_importance.head(10)
bars = ax2.barh(range(len(top_features)), top_features['importance'].values, color='steelblue')
ax2.set_yticks(range(len(top_features)))
ax2.set_yticklabels(top_features['feature'].values)
ax2.set_xlabel('Importance Score')
ax2.set_title('Top 10 Feature Importance (XGBoost)', fontsize=14, fontweight='bold')
ax2.invert_yaxis()
for i, bar in enumerate(bars):
    width = bar.get_width()
    ax2.text(width, bar.get_y() + bar.get_height()/2, 
             f'{width:.4f}', ha='left', va='center', fontsize=9)

# 3. Class Distribution
ax3 = plt.subplot(5, 2, 3)
class_dist = y.value_counts().sort_index()
bars = ax3.bar(class_names, [class_dist[i] for i in range(n_classes)], 
               color=['#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', '#e67e22'])
ax3.set_ylabel('Count')
ax3.set_title('Class Distribution', fontsize=14, fontweight='bold')
ax3.grid(axis='y', alpha=0.3)
for bar in bars:
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}', ha='center', va='bottom')

# 4. Accuracy Comparison
ax4 = plt.subplot(5, 2, 4)
datasets = ['Training', 'Test']
accuracies = [train_accuracy, test_accuracy]
bars = ax4.bar(datasets, accuracies, color=['#3498db', '#e74c3c'])
ax4.set_ylabel('Accuracy')
ax4.set_ylim([0, 1])
ax4.set_title('Model Accuracy', fontsize=14, fontweight='bold')
ax4.grid(axis='y', alpha=0.3)
for bar, acc in zip(bars, accuracies):
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height,
             f'{acc:.4f}', ha='center', va='bottom')

# 5-8. SHAP Summary Plots for each class (or combined)
for idx in range(n_classes):
    ax = plt.subplot(5, 2, 5 + idx)
    if isinstance(shap_values, list):
        class_shap = shap_values[idx]
    else:
        class_shap = shap_values[:, :, idx] if shap_values.ndim == 3 else shap_values
    
    # Get mean absolute SHAP values
    mean_shap = np.abs(class_shap).mean(axis=0)
    
    # Create dataframe for plotting
    shap_importance = pd.DataFrame({
        'feature': feature_cols,
        'mean_shap': mean_shap
    }).sort_values('mean_shap', ascending=False).head(10)
    
    bars = ax.barh(range(len(shap_importance)), shap_importance['mean_shap'].values, 
                    color=plt.cm.Set3(idx))
    ax.set_yticks(range(len(shap_importance)))
    ax.set_yticklabels(shap_importance['feature'].values)
    ax.set_xlabel('Mean |SHAP value|')
    ax.set_title(f'SHAP Feature Importance - {class_names[idx]}', 
                 fontsize=12, fontweight='bold')
    ax.invert_yaxis()

plt.tight_layout()
plt.savefig('scada_model_analysis.png', dpi=300, bbox_inches='tight')
print("\nSaved: scada_model_analysis.png")
plt.close()

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
with open('scada_model.pkl', 'wb') as f:
    pickle.dump(model, f)
with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
    
print(f"\n✓ Model and scaler saved successfully!")
print("\n" + "=" * 80)