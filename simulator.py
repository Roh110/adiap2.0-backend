import random

machine_states = {
    "CNC-01":   {"mode": "normal", "step": 0},
    "PRESS-01": {"mode": "normal", "step": 0},
    "PUMP-01":  {"mode": "normal", "step": 0},
}

FAILURE_PROFILES = {
    "bearing_wear":        {"temp_delta": 18, "vib_delta": 2.8, "curr_delta": 1.5},
    "lubrication_failure": {"temp_delta": 25, "vib_delta": 1.2, "curr_delta": 2.0},
    "misalignment":        {"temp_delta": 10, "vib_delta": 3.5, "curr_delta": 0.8},
    "motor_overload":      {"temp_delta": 30, "vib_delta": 0.5, "curr_delta": 5.0},
}

BASELINES = {
    "CNC-01":   {"temp": 45.0, "vib": 1.2, "curr": 12.0},
    "PRESS-01": {"temp": 55.0, "vib": 1.8, "curr": 18.0},
    "PUMP-01":  {"temp": 40.0, "vib": 0.9, "curr": 8.0},
}

def inject_failure(machine_id, failure_type):
    machine_states[machine_id]["mode"] = failure_type
    machine_states[machine_id]["step"] = 0

def reset_machine(machine_id):
    machine_states[machine_id]["mode"] = "normal"
    machine_states[machine_id]["step"] = 0

def get_sensor_reading(machine_id):
    state = machine_states[machine_id]
    base  = BASELINES[machine_id]
    temp  = base["temp"] + random.gauss(0, 0.3)
    vib   = base["vib"]  + abs(random.gauss(0, 0.03))
    curr  = base["curr"] + random.gauss(0, 0.5)
    anomaly = 0.0
    if state["mode"] != "normal":
        profile = FAILURE_PROFILES[state["mode"]]
        step    = min(state["step"], 20)
        ratio   = step / 20.0
        state["step"] += 1
        temp    += profile["temp_delta"]  * ratio
        vib     += profile["vib_delta"]   * ratio
        curr    += profile["curr_delta"]  * ratio
        anomaly  = ratio * 100.0
    return {
        "machine_id":    machine_id,
        "temperature":   round(temp, 2),
        "vibration":     round(max(0.1, vib), 2),
        "current":       round(max(0.1, curr), 2),
        "anomaly_score": round(anomaly, 1),
        "mode":          state["mode"],
    }

def generate_sensor_data():
    return [get_sensor_reading(m) for m in ["CNC-01", "PRESS-01", "PUMP-01"]]
