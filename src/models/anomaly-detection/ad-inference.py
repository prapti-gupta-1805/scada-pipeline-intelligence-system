"""
SCADA Pipeline Anomaly Detection - Inference Script

Loads a trained Isolation Forest model and predicts
whether new SCADA measurements are anomalous.
"""

import pickle
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# ==============================================================================
# CONFIGURATION
# ==============================================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "anomaly_model.pkl"
SCALER_PATH = BASE_DIR / "anomaly_scaler.pkl"
STATS_PATH = BASE_DIR / "feature_stats.pkl"

FEATURE_COLS = [
    "segment_id",
    "pressure",
    "flow_rate",
    "temperature",
    "valve_status",
    "pump_state",
    "pump_speed",
    "compressor_state",
    "energy_consumption",
    "alarm_triggered",
    "hour",
    "day_of_week",
    "day_of_month"
]
SCORE_MIN = -0.3
SCORE_MAX = 0.4

# ==============================================================================
# LOAD MODEL
# ==============================================================================

print("Loading anomaly detector...")

try:

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    with open(SCALER_PATH, "rb") as f:
        scaler = pickle.load(f)

    with open(STATS_PATH, "rb") as f:
        feature_stats = pickle.load(f)

    print("✓ Anomaly model loaded successfully")

except FileNotFoundError as e:

    raise RuntimeError(
        f"Required model file not found:\n{e}"
    )

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def calculate_confidence(anomaly_score):
    """
    Normalize the raw inverted anomaly score to a 0.0 - 1.0 range
    using min-max scaling across typical Isolation Forest score boundaries.
    """
    normalized = (anomaly_score - SCORE_MIN) / (SCORE_MAX - SCORE_MIN)
    confidence = np.clip(normalized, 0.0, 1.0)
    return round(float(confidence), 3)


def calculate_risk_level(confidence_score):
    """
    Determine qualitative risk level directly from the 0-1 normalized confidence score.
    """
    if confidence_score >= 0.80:
        return "Critical"
    elif confidence_score >= 0.60:
        return "High"
    elif confidence_score >= 0.40:
        return "Medium"
    else:
        return "Low"


def calculate_feature_deviations(sample_df):
    """
    Calculate z-score deviation of every feature
    from the training distribution.
    """

    deviations = {}

    for feature in FEATURE_COLS:

        value = float(sample_df[feature].iloc[0])

        mean = feature_stats["mean"][feature]

        std = feature_stats["std"][feature]

        if std == 0:
            z_score = 0

        else:
            z_score = abs((value - mean) / std)

        deviations[feature] = {
            "value": value,
            "mean": float(mean),
            "std": float(std),
            "z_score": round(float(z_score), 3)
        }

    return deviations


# ==============================================================================
# SINGLE SAMPLE PREDICTION
# ==============================================================================

def predict(sample_dict, explain=True):
    """
    Predict anomaly for a single SCADA observation.

    Parameters
    ----------
    sample_dict : dict
        Dictionary containing all required SCADA features.

    explain : bool
        If True, returns top deviating features.

    Returns
    -------
    dict
    """

    missing_features = set(FEATURE_COLS) - set(sample_dict.keys())

    if missing_features:

        raise ValueError(
            f"Missing features: {missing_features}"
        )

    X = pd.DataFrame([sample_dict])

    X_scaled = scaler.transform(X)

    prediction = model.predict(X_scaled)[0]

    decision_score = model.decision_function(X_scaled)[0]

    anomaly_score = float(-decision_score)

    status = "Anomaly" if prediction == -1 else "Normal"
    confidence = calculate_confidence(anomaly_score)
    risk_level = calculate_risk_level(confidence)  # Now uses confidence

    result = {
        "status": status,
        "confidence": confidence,
        "risk_level": risk_level,
        "anomaly_score": round(anomaly_score, 4)
    }

    if explain:

        deviations = calculate_feature_deviations(X)

        top_features = sorted(

            deviations.items(),

            key=lambda item: item[1]["z_score"],

            reverse=True

        )[:5]

        result["top_deviating_features"] = [

            {

        "feature": feature,
        "value": data["value"],
        "expected": round(data["mean"], 2),
        "z_score": data["z_score"]

            }

            for feature, data in top_features

        ]

    return result

# ==============================================================================
# BATCH PREDICTION
# ==============================================================================

def predict_batch(dataframe):
    """
    Predict anomalies for multiple SCADA observations.
    """
    missing_columns = set(FEATURE_COLS) - set(dataframe.columns)
    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    X = dataframe[FEATURE_COLS].copy()
    X_scaled = scaler.transform(X)

    predictions = model.predict(X_scaled)
    decision_scores = model.decision_function(X_scaled)
    anomaly_scores = -decision_scores

    # Vectorized normalization for confidence
    normalized_scores = (anomaly_scores - SCORE_MIN) / (SCORE_MAX - SCORE_MIN)
    confidences = np.clip(normalized_scores, 0.0, 1.0)

    # Map risk levels from confidences
    risk_levels = [calculate_risk_level(c) for c in confidences]

    results = pd.DataFrame({
        "status": np.where(predictions == -1, "Anomaly", "Normal"),
        "confidence": np.round(confidences, 3),
        "risk_level": risk_levels,
        "anomaly_score": np.round(anomaly_scores, 4)
    })

    return results

# ==============================================================================
# DEMO
# ==============================================================================

if __name__ == "__main__":

    print("=" * 80)
    print("SCADA ANOMALY DETECTION - INFERENCE")
    print("=" * 80)

    # --------------------------------------------------------------------------
    # Example 1
    # --------------------------------------------------------------------------

    print("\n[Example 1] Normal Pipeline Reading")
    print("-" * 80)

    normal_sample = {

        "segment_id": 25,
        "pressure": 72.5,
        "flow_rate": 4.6,
        "temperature": 32.1,
        "valve_status": 1,
        "pump_state": 1,
        "pump_speed": 1400,
        "compressor_state": 1,
        "energy_consumption": 33.2,
        "alarm_triggered": 0,
        "hour": 14,
        "day_of_week": 2,
        "day_of_month": 15

    }

    result = predict(normal_sample)

    print(f"Status          : {result['status']}")
    print(f"Confidence      : {result['confidence']:.3f}")
    print(f"Risk Level      : {result['risk_level']}")
    print(f"Anomaly Score   : {result['anomaly_score']:.4f}")

    print("\nTop Deviating Features")

    for i, feature in enumerate(result["top_deviating_features"], start=1):

        print(
            f"{i}. "
            f"{feature['feature']:20}"
            f"Value = {feature['value']:10.2f}"
            f"   Z-score = {feature['z_score']:.2f}"
        )

    # --------------------------------------------------------------------------
    # Example 2
    # --------------------------------------------------------------------------

    print("\n\n[Example 2] Suspicious Pipeline Reading")
    print("-" * 80)

    anomaly_sample = {

        "segment_id": 42,
        "pressure": 110.5,
        "flow_rate": 0.5,
        "temperature": 45.2,
        "valve_status": 2,
        "pump_state": 1,
        "pump_speed": 500,
        "compressor_state": 0,
        "energy_consumption": 15.2,
        "alarm_triggered": 1,
        "hour": 3,
        "day_of_week": 4,
        "day_of_month": 20

    }

    result = predict(anomaly_sample)

    print(f"Status          : {result['status']}")
    print(f"Confidence      : {result['confidence']:.3f}")
    print(f"Risk Level      : {result['risk_level']}")
    print(f"Anomaly Score   : {result['anomaly_score']:.4f}")

    print("\nTop Deviating Features")

    for i, feature in enumerate(result["top_deviating_features"], start=1):

        print(
            f"{i}. "
            f"{feature['feature']:20}"
            f"Value = {feature['value']:10.2f}"
            f"   Z-score = {feature['z_score']:.2f}"
        )

    # --------------------------------------------------------------------------
    # Example 3
    # --------------------------------------------------------------------------

    print("\n\n[Example 3] Batch Prediction")
    print("-" * 80)

    batch_df = pd.DataFrame([

        normal_sample,

        anomaly_sample,

        {

            "segment_id": 12,
            "pressure": 75,
            "flow_rate": 3.8,
            "temperature": 31,
            "valve_status": 1,
            "pump_state": 1,
            "pump_speed": 1350,
            "compressor_state": 1,
            "energy_consumption": 31,
            "alarm_triggered": 0,
            "hour": 11,
            "day_of_week": 1,
            "day_of_month": 10

        }

    ])

    batch_results = predict_batch(batch_df)

    print(batch_results.to_string(index=False))

    print("\n" + "=" * 80)
    print("INFERENCE COMPLETED")
    print("=" * 80)