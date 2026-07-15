"""
Pipeline Predictive Maintenance - Inference Script

Loads the trained XGBoost model and predicts the
pipeline condition (Normal, Moderate or Critical).
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

MODEL_PATH = BASE_DIR / "maintenance_model.pkl"
MATERIAL_ENCODER_PATH = BASE_DIR / "material_encoder.pkl"
GRADE_ENCODER_PATH = BASE_DIR / "grade_encoder.pkl"
TARGET_ENCODER_PATH = BASE_DIR / "target_encoder.pkl"
SHAP_EXPLAINER_PATH = BASE_DIR / "shap_explainer.pkl"

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

# ==============================================================================
# LOAD MODEL
# ==============================================================================

print("Loading predictive maintenance model...")

try:

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    with open(MATERIAL_ENCODER_PATH, "rb") as f:
        material_encoder = pickle.load(f)

    with open(GRADE_ENCODER_PATH, "rb") as f:
        grade_encoder = pickle.load(f)

    with open(TARGET_ENCODER_PATH, "rb") as f:
        target_encoder = pickle.load(f)

    with open(SHAP_EXPLAINER_PATH, "rb") as f:
        explainer = pickle.load(f)

    print("✓ Predictive Maintenance model loaded successfully")
    print(f"✓ Loaded {len(FEATURE_COLUMNS)} input features")

except FileNotFoundError as e:

    raise RuntimeError(f"Missing required model file:\n{e}")

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def calculate_risk_level(predicted_condition):

    if predicted_condition == "Critical":
        return "Critical"

    elif predicted_condition == "Moderate":
        return "Medium"

    else:
        return "Low"

# ==============================================================================
# SINGLE SAMPLE PREDICTION
# ==============================================================================

def predict(sample_dict, explain=True):

    missing = set(FEATURE_COLUMNS) - set(sample_dict.keys())

    if missing:

        raise ValueError(

            f"Missing features: {missing}"

        )

    X = pd.DataFrame([sample_dict])

    X["Material"] = material_encoder.transform(

        X["Material"]

    )

    X["Grade"] = grade_encoder.transform(

        X["Grade"]

    )

    prediction = model.predict(X)[0]

    prediction_label = target_encoder.inverse_transform(

        [prediction]

    )[0]

    probabilities = model.predict_proba(X)[0]

    confidence = float(np.max(probabilities))

    result = {

        "prediction":

        prediction_label,

        "confidence":

        round(confidence,4),

        "risk_level":

        calculate_risk_level(prediction_label),

        "class_probabilities": {

            target_encoder.classes_[i]:

            round(float(probabilities[i]),4)

            for i in range(len(probabilities))

        }

    }

    if explain:

        shap_values = explainer(X).values

        if shap_values.ndim == 3:

            feature_scores = np.mean(

                np.abs(shap_values[0]),

                axis=1

            )

        else:

            feature_scores = np.abs(

                shap_values[0]

            )

        top_idx = np.argsort(

            feature_scores

        )[::-1][:5]

        explanations = []

        for idx in top_idx:

            explanations.append({

                "feature":

                FEATURE_COLUMNS[idx],

                "value":

                sample_dict[FEATURE_COLUMNS[idx]],

                "importance":

                round(

                    float(feature_scores[idx]),

                    4

                )

            })

        result["top_contributing_features"] = explanations

    return result
# ==============================================================================
# BATCH PREDICTION
# ==============================================================================

def predict_batch(dataframe):

    """
    Predict pipeline condition for multiple samples.
    """

    missing = set(FEATURE_COLUMNS) - set(dataframe.columns)

    if missing:

        raise ValueError(

            f"Missing features: {missing}"

        )

    X = dataframe.copy()

    X["Material"] = material_encoder.transform(

        X["Material"]

    )

    X["Grade"] = grade_encoder.transform(

        X["Grade"]

    )

    predictions = model.predict(X)

    prediction_labels = target_encoder.inverse_transform(

        predictions

    )

    probabilities = model.predict_proba(X)

    confidence = probabilities.max(axis=1)

    results = pd.DataFrame({

        "prediction":

        prediction_labels,

        "confidence":

        np.round(confidence,4),

        "risk_level":[

            calculate_risk_level(label)

            for label in prediction_labels

        ]

    })

    return results


# ==============================================================================
# DEMO
# ==============================================================================

if __name__ == "__main__":

    print("=" * 80)
    print("PIPELINE PREDICTIVE MAINTENANCE - INFERENCE")
    print("=" * 80)

    # --------------------------------------------------------------------------
    # Example 1
    # --------------------------------------------------------------------------

    print("\n[Example 1] Healthy Pipeline")
    print("-" * 80)

    healthy = {

        "Pipe_Size_mm": 800,
        "Thickness_mm": 25.78,
        "Material": "Stainless Steel",
        "Grade": "ASTM A333 Grade 6",
        "Max_Pressure_psi": 150,
        "Temperature_C": 11.6,
        "Corrosion_Impact_Percent": 18.68,
        "Thickness_Loss_mm": 0.53,
        "Material_Loss_Percent": 2.06,
        "Time_Years": 1

    }

    result = predict(healthy)

    print(f"Predicted Condition : {result['prediction']}")
    print(f"Confidence          : {result['confidence']:.3f}")
    print(f"Risk Level          : {result['risk_level']}")

    print("\nClass Probabilities")

    for cls, prob in result["class_probabilities"].items():

        print(f"  {cls:<10}: {prob:.4f}")

    print("\nTop Contributing Features")

    for i, feature in enumerate(

        result["top_contributing_features"],

        start=1

    ):

        print(

            f"{i}. "

            f"{feature['feature']:30}"

            f"Value = {str(feature['value']):>8}"

            f"   Importance = {feature['importance']:.4f}"

        )

    # --------------------------------------------------------------------------
    # Example 2
    # --------------------------------------------------------------------------

    print("\n\n[Example 2] Critical Pipeline")
    print("-" * 80)

    critical = {

        "Pipe_Size_mm": 150,
        "Thickness_mm": 6.12,
        "Material": "Carbon Steel",
        "Grade": "API 5L X52",
        "Max_Pressure_psi": 1500,
        "Temperature_C": 42.6,
        "Corrosion_Impact_Percent": 12.29,
        "Thickness_Loss_mm": 6.31,
        "Material_Loss_Percent": 103.10,
        "Time_Years": 17

    }

    result = predict(critical)

    print(f"Predicted Condition : {result['prediction']}")
    print(f"Confidence          : {result['confidence']:.3f}")
    print(f"Risk Level          : {result['risk_level']}")

    print("\nClass Probabilities")

    for cls, prob in result["class_probabilities"].items():

        print(f"  {cls:<10}: {prob:.4f}")

    print("\nTop Contributing Features")

    for i, feature in enumerate(

        result["top_contributing_features"],

        start=1

    ):

        print(

            f"{i}. "

            f"{feature['feature']:30}"

            f"Value = {str(feature['value']):>8}"

            f"   Importance = {feature['importance']:.4f}"

        )

    # --------------------------------------------------------------------------
    # Example 3
    # --------------------------------------------------------------------------

    print("\n\n[Example 3] Batch Prediction")
    print("-" * 80)

    batch_df = pd.DataFrame([

        healthy,

        critical,

        {

            "Pipe_Size_mm": 300,
            "Thickness_mm": 13.87,
            "Material": "Carbon Steel",
            "Grade": "ASTM A106 Grade B",
            "Max_Pressure_psi": 900,
            "Temperature_C": 40.8,
            "Corrosion_Impact_Percent": 5.57,
            "Thickness_Loss_mm": 3.02,
            "Material_Loss_Percent": 21.77,
            "Time_Years": 21

        }

    ])

    batch_results = predict_batch(batch_df)

    print(batch_results.to_string(index=False))

    print("\n" + "=" * 80)
    print("INFERENCE COMPLETED")
    print("=" * 80)