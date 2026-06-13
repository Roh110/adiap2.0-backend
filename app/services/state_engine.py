def calculate_machine_state(readings):
    """
    readings = last N turbidity values (oldest → newest)
    """

    if len(readings) < 5:
        return {
            "state": "NORMAL",
            "risk_score": 10,
            "trend": "INSUFFICIENT_DATA"
        }

    latest = readings[-1]
    first = readings[0]

    # Trend calculation
    diff = latest - first

    avg = sum(readings) / len(readings)

    # Simple slope idea
    if diff > 800:
        trend = "FAST_RISING"
        risk_score = 90
        state = "FAILURE_IMMINENT"

    elif diff > 400:
        trend = "RISING"
        risk_score = 70
        state = "CRITICAL"

    elif diff > 150:
        trend = "SLOW_RISING"
        risk_score = 50
        state = "WARNING"

    else:
        trend = "STABLE"
        risk_score = 20
        state = "NORMAL"

    # extra adjustment
    if avg > 2500:
        risk_score += 10
        state = "CRITICAL"

    return {
        "state": state,
        "risk_score": min(risk_score, 100),
        "trend": trend
    }