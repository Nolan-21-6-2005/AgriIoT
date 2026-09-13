"""Rule-based irrigation recommendation.

This module intentionally does not use machine learning.  It applies explicit,
deterministic rules to the current environmental readings.
"""

# Irrigation thresholds. Keep these values easy to explain and adjust.
SOIL_MOISTURE_THRESHOLD = 30.0   # Below this: soil is considered dry.
RAIN_THRESHOLD = 1.0             # At/above this: recent rain is enough to skip watering.


def predict_irrigation(v):
    """Return a deterministic irrigation recommendation.

    Rules:
    1. If soil moisture is below 30% AND rain is below 1 mm -> water.
    2. Otherwise -> do not water.

    The other sensor values are accepted by the API for compatibility with the
    existing form, but are not required by the current rule set.
    """
    soil_moisture = float(v.get("soil_moisture", 0))
    rain = float(v.get("rain", 0))

    irrigation = (
        soil_moisture < SOIL_MOISTURE_THRESHOLD
        and rain < RAIN_THRESHOLD
    )

    if irrigation:
        message = (
            f"Độ ẩm đất {soil_moisture:.1f}% < {SOIL_MOISTURE_THRESHOLD:.0f}% "
            f"và lượng mưa {rain:.1f} mm < {RAIN_THRESHOLD:.1f} mm."
        )
    else:
        if soil_moisture >= SOIL_MOISTURE_THRESHOLD:
            message = (
                f"Độ ẩm đất {soil_moisture:.1f}% >= "
                f"{SOIL_MOISTURE_THRESHOLD:.0f}%."
            )
        else:
            message = (
                f"Lượng mưa {rain:.1f} mm >= {RAIN_THRESHOLD:.1f} mm."
            )

    return {
        "irrigation": irrigation,
        "confidence": None,
        "model": "rule_based",
        "message": message,
    }
