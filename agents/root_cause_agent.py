BASELINES = {
    "CNC-01":   {"temp": 45.0, "vib": 1.2, "curr": 12.0},
    "PRESS-01": {"temp": 55.0, "vib": 1.8, "curr": 18.0},
    "PUMP-01":  {"temp": 40.0, "vib": 0.9, "curr": 8.0},
}

RULES = [
    {"cause": "Bearing Wear",        "check": lambda t,v,c,bt,bv,bc: (t-bt)>12 and (v-bv)>1.5,                 "confidence": 0.87},
    {"cause": "Lubrication Failure", "check": lambda t,v,c,bt,bv,bc: (t-bt)>20 and (v-bv)>0.8 and (c-bc)>1.5, "confidence": 0.82},
    {"cause": "Misalignment",        "check": lambda t,v,c,bt,bv,bc: (v-bv)>2.5 and (t-bt)<15,                 "confidence": 0.79},
    {"cause": "Motor Overload",      "check": lambda t,v,c,bt,bv,bc: (c-bc)>4.0 and (t-bt)>20,                 "confidence": 0.91},
]

def run_root_cause_agent(machine_id, temperature, vibration, current):
    base = BASELINES.get(machine_id, {"temp": 50, "vib": 1.5, "curr": 15})
    bt, bv, bc = base["temp"], base["vib"], base["curr"]
    matched = []
    for rule in RULES:
        if rule["check"](temperature, vibration, current, bt, bv, bc):
            dev  = ((temperature-bt)/bt + (vibration-bv)/bv + (current-bc)/bc) / 3
            conf = min(0.99, rule["confidence"] + dev * 0.1)
            matched.append({"cause": rule["cause"], "confidence": round(conf, 2)})
    if not matched:
        matched.append({"cause": "Bearing Wear", "confidence": 0.55})
    matched.sort(key=lambda x: x["confidence"], reverse=True)
    primary = matched[0]
    evidence = []
    if temperature > bt + 5:
        evidence.append(f"Temperature elevated: {temperature}C (normal {bt}C, +{round(temperature-bt,1)}C)")
    if vibration > bv + 0.3:
        evidence.append(f"Vibration high: {vibration} mm/s (normal {bv}, +{round(vibration-bv,1)})")
    if current > bc + 0.5:
        evidence.append(f"Current spike: {current}A (normal {bc}A, +{round(current-bc,1)}A)")
    return {
        "root_cause":     primary["cause"],
        "confidence":     primary["confidence"],
        "confidence_pct": int(primary["confidence"] * 100),
        "all_candidates": matched,
        "evidence":       evidence,
    }
