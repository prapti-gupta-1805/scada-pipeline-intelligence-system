"""
SCADA Fault Classification - Inference Script
Load trained model and make predictions on new SCADA measurements
"""

import pickle
import numpy as np
import pandas as pd
import shap
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

MODEL_PATH = 'scada_model.pkl'
SCALER_PATH = 'scaler.pkl'

FEATURE_COLS = ['segment_id', 'pressure', 'flow_rate', 'temperature', 
                'valve_status', 'pump_state', 'pump_speed', 'compressor_state',
                'energy_consumption', 'alarm_triggered', 'hour', 'day_of_week', 'day_of_month']

CLASS_NAMES = ['Normal', 'Leak', 'Blockage', 'Surge', 'Degradation']

# ============================================================================
# LOAD MODEL & SCALER
# ============================================================================

print("Loading model and scaler...")
try:
    model = pickle.load(open(MODEL_PATH, 'rb'))
    scaler = pickle.load(open(SCALER_PATH, 'rb'))
    print("✓ Model and scaler loaded successfully")
except FileNotFoundError as e:
    print(f"✗ Error: {e}")
    print("  Please ensure both scada_model.pkl and scaler.pkl are in the current directory")
    exit(1)

# ============================================================================
# FUNCTION: PREDICT ON SINGLE SAMPLE
# ============================================================================

def predict(sample_dict, explain=True):
    """
    Make prediction on a single SCADA measurement.

    Parameters:
    -----------
    sample_dict : dict
        Dictionary with keys: segment_id, pressure, flow_rate, temperature,
                             valve_status, pump_state, pump_speed,
                             compressor_state, energy_consumption,
                             alarm_triggered, hour, day_of_week, day_of_month

    explain : bool
        If True, provide SHAP explanation and save a SHAP plot.

    Returns:
    --------
    dict with prediction results and optional SHAP output.
    """

    # Validate input
    missing_features = set(FEATURE_COLS) - set(sample_dict.keys())
    if missing_features:
        raise ValueError(f"Missing features: {missing_features}")

    # Create dataframe and scale
    X = pd.DataFrame([sample_dict])
    X_scaled = scaler.transform(X)

    # Get prediction
    pred_class = model.predict(X_scaled)[0]
    pred_proba = model.predict_proba(X_scaled)[0]

    # Build result
    result = {
        'predicted_class': CLASS_NAMES[pred_class],
        'predicted_class_id': pred_class,
        'confidence': float(max(pred_proba)),
        'class_probabilities': {CLASS_NAMES[i]: float(prob)
                               for i, prob in enumerate(pred_proba)},
        'raw_sample': sample_dict
    }

    # Add SHAP explanation if requested
    if explain:
        try:
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X_scaled)

            # Extract SHAP values for predicted class
            if isinstance(shap_values, list):
                sample_shap = shap_values[pred_class][0]
            else:
                if shap_values.ndim == 3:
                    sample_shap = shap_values[0, :, pred_class]
                else:
                    sample_shap = shap_values[0]

            # Get top contributing features
            top_indices = np.abs(sample_shap).argsort()[-5:][::-1]
            top_features = [FEATURE_COLS[idx] for idx in top_indices]
            shap_values_top = sample_shap[top_indices]

            # Save SHAP plot
            plot_path = f"shap_explanation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.barh(range(len(top_features)), shap_values_top[::-1], color='tab:blue')
            ax.set_yticks(range(len(top_features)))
            ax.set_yticklabels(top_features[::-1])
            ax.set_xlabel('SHAP value')
            ax.set_title('Top SHAP Features for Prediction')
            ax.grid(axis='x', alpha=0.3)
            plt.tight_layout()
            fig.savefig(plot_path, dpi=200)
            plt.close(fig)

            result['shap_explanation'] = {
                'plot_path': plot_path,
                'top_features': [
                    {
                        'feature': FEATURE_COLS[idx],
                        'value': float(X[FEATURE_COLS[idx]].values[0]),
                        'shap_value': float(sample_shap[idx]),
                        'direction': 'toward' if sample_shap[idx] > 0 else 'away from'
                    }
                    for idx in top_indices
                ]
            }
        except Exception as e:
            result['shap_explanation'] = f"SHAP calculation failed: {str(e)}"

    return result

# ============================================================================
# FUNCTION: PREDICT ON BATCH
# ============================================================================

def predict_batch(dataframe, explain=False):
    """
    Make predictions on multiple samples
    
    Parameters:
    -----------
    dataframe : pd.DataFrame
        DataFrame with required feature columns
    
    explain : bool
        If True, provide SHAP explanation (slow for large batches)
    
    Returns:
    --------
    pd.DataFrame with predictions
    """
    
    # Validate columns
    missing_cols = set(FEATURE_COLS) - set(dataframe.columns)
    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")
    
    # Extract features and scale
    X = dataframe[FEATURE_COLS].copy()
    X_scaled = scaler.transform(X)
    
    # Get predictions
    pred_classes = model.predict(X_scaled)
    pred_probas = model.predict_proba(X_scaled)
    
    # Build results dataframe
    results = pd.DataFrame({
        'predicted_class': [CLASS_NAMES[pc] for pc in pred_classes],
        'predicted_class_id': pred_classes,
        'confidence': np.max(pred_probas, axis=1)
    })
    
    # Add class probabilities
    for i, class_name in enumerate(CLASS_NAMES):
        results[f'prob_{class_name.lower()}'] = pred_probas[:, i]
    
    return results

# ============================================================================
# ENTRYPOINT FOR MODULE USAGE
# ============================================================================

if __name__ == "__main__":
    print("This module exposes the inference functions:")
    print("  - predict(sample_dict)")
    print("  - predict_batch(df)")
    print("Run `src/models/inference_demo.py` for example usage and SHAP plot generation.")
    print("-" * 80)
    
    normal_sample = {
        'segment_id': 25,
        'pressure': 72.5,
        'flow_rate': 4.6,
        'temperature': 32.1,
        'valve_status': 1,
        'pump_state': 1,
        'pump_speed': 1400,
        'compressor_state': 1,
        'energy_consumption': 33.2,
        'alarm_triggered': 0,
        'hour': 14,
        'day_of_week': 2,
        'day_of_month': 15
    }
    
    result1 = predict(normal_sample, explain=True)
    
    print(f"Predicted Fault: {result1['predicted_class']}")
    print(f"Confidence: {result1['confidence']:.4f}")
    print(f"\nClass Probabilities:")
    for class_name, prob in result1['class_probabilities'].items():
        bar_length = int(prob * 40)
        bar = "█" * bar_length + "░" * (40 - bar_length)
        print(f"  {class_name:15} {bar} {prob:.4f}")
    
    if 'shap_explanation' in result1 and isinstance(result1['shap_explanation'], dict):
        print(f"\nTop Contributing Features (SHAP):")
        for i, feat in enumerate(result1['shap_explanation']['top_features'], 1):
            print(f"  {i}. {feat['feature']:20} = {feat['value']:8.2f} " +
                  f"(SHAP: {feat['shap_value']:+.4f} - {feat['direction']} {result1['predicted_class']})")
    
    # ========================================================================
    # EXAMPLE 2: Single Sample - Blockage Detection
    # ========================================================================
    
    print("\n\n[Example 2] Single Sample - Blockage Detection")
    print("-" * 80)
    
    blockage_sample = {
        'segment_id': 16,
        'pressure': 95.2,
        'flow_rate': 1.8,
        'temperature': 30.8,
        'valve_status': 2,
        'pump_state': 1,
        'pump_speed': 1320,
        'compressor_state': 1,
        'energy_consumption': 37.5,
        'alarm_triggered': 1,
        'hour': 10,
        'day_of_week': 1,
        'day_of_month': 8
    }
    
    result2 = predict(blockage_sample, explain=True)
    
    print(f"Predicted Fault: {result2['predicted_class']}")
    print(f"Confidence: {result2['confidence']:.4f}")
    print(f"\nClass Probabilities:")
    for class_name, prob in result2['class_probabilities'].items():
        bar_length = int(prob * 40)
        bar = "█" * bar_length + "░" * (40 - bar_length)
        print(f"  {class_name:15} {bar} {prob:.4f}")
    
    if 'shap_explanation' in result2 and isinstance(result2['shap_explanation'], dict):
        print(f"\nTop Contributing Features (SHAP):")
        for i, feat in enumerate(result2['shap_explanation']['top_features'], 1):
            print(f"  {i}. {feat['feature']:20} = {feat['value']:8.2f} " +
                  f"(SHAP: {feat['shap_value']:+.4f} - {feat['direction']} {result2['predicted_class']})")
    
    # ========================================================================
    # EXAMPLE 3: Batch Prediction
    # ========================================================================
    
    print("\n\n[Example 3] Batch Prediction")
    print("-" * 80)
    
    batch_samples = pd.DataFrame([
        {
            'segment_id': 10, 'pressure': 70.5, 'flow_rate': 4.5, 'temperature': 32.0,
            'valve_status': 1, 'pump_state': 1, 'pump_speed': 1380, 'compressor_state': 1,
            'energy_consumption': 32.1, 'alarm_triggered': 0, 'hour': 9, 
            'day_of_week': 0, 'day_of_month': 1
        },
        {
            'segment_id': 20, 'pressure': 88.3, 'flow_rate': 2.2, 'temperature': 31.5,
            'valve_status': 2, 'pump_state': 1, 'pump_speed': 1300, 'compressor_state': 1,
            'energy_consumption': 36.8, 'alarm_triggered': 1, 'hour': 12, 
            'day_of_week': 2, 'day_of_month': 5
        },
        {
            'segment_id': 35, 'pressure': 75.0, 'flow_rate': 3.5, 'temperature': 33.2,
            'valve_status': 1, 'pump_state': 0, 'pump_speed': 0, 'compressor_state': 1,
            'energy_consumption': 20.5, 'alarm_triggered': 0, 'hour': 15, 
            'day_of_week': 3, 'day_of_month': 10
        }
    ])
    
    batch_results = predict_batch(batch_samples)
    
    print(batch_results.to_string(index=False))
    
    # ========================================================================
    # EXAMPLE 4: Risk Assessment
    # ========================================================================
    
    print("\n\n[Example 4] Risk Assessment - Anomalous Reading")
    print("-" * 80)
    
    anomalous_sample = {
        'segment_id': 42,
        'pressure': 110.5,        # Extremely high
        'flow_rate': 0.5,         # Very low
        'temperature': 45.2,      # Very high
        'valve_status': 2,
        'pump_state': 1,
        'pump_speed': 500,        # Very low
        'compressor_state': 0,    # Off
        'energy_consumption': 15.2,
        'alarm_triggered': 1,
        'hour': 3,
        'day_of_week': 4,
        'day_of_month': 20
    }
    
    result4 = predict(anomalous_sample, explain=True)
    
    print(f"⚠ ALERT: Predicted Fault: {result4['predicted_class']}")
    print(f"Confidence: {result4['confidence']:.4f}")
    print(f"\nRisk Level: {'HIGH' if result4['confidence'] > 0.8 else 'MEDIUM' if result4['confidence'] > 0.5 else 'LOW'}")
    print(f"\nClass Probabilities:")
    for class_name, prob in result4['class_probabilities'].items():
        bar_length = int(prob * 40)
        bar = "█" * bar_length + "░" * (40 - bar_length)
        risk_marker = "⚠" if prob > 0.3 and class_name != result4['predicted_class'] else ""
        print(f"  {class_name:15} {bar} {prob:.4f} {risk_marker}")
    
    if 'shap_explanation' in result4 and isinstance(result4['shap_explanation'], dict):
        print(f"\nCritical Contributing Factors:")
        for i, feat in enumerate(result4['shap_explanation']['top_features'], 1):
            print(f"  {i}. {feat['feature']:20} = {feat['value']:8.2f} " +
                  f"(SHAP: {feat['shap_value']:+.4f})")
    
    print("\n" + "="*80)
    print("INFERENCE EXAMPLES COMPLETED")
    print("="*80)