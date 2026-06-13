MACHINE_CONFIG = {
    "CNC-01":   {"production_rate": 15000, "repair_base": 25000, "criticality": 1.2},
    "PRESS-01": {"production_rate": 12000, "repair_base": 20000, "criticality": 1.0},
    "PUMP-01":  {"production_rate": 8000,  "repair_base": 15000, "criticality": 0.8},
}
CAUSE_REPAIR = {"Bearing Wear": 1.5, "Lubrication Failure": 0.8, "Misalignment": 1.2, "Motor Overload": 2.0}
CAUSE_HOURS  = {"Bearing Wear": 8,   "Lubrication Failure": 4,   "Misalignment": 6,   "Motor Overload": 12}

def run_impact_agent(machine_id, root_cause, confidence):
    cfg   = MACHINE_CONFIG.get(machine_id, {"production_rate": 10000, "repair_base": 18000, "criticality": 1.0})
    hours = CAUSE_HOURS.get(root_cause, 6)
    mult  = CAUSE_REPAIR.get(root_cause, 1.0)
    production_loss = cfg["production_rate"] * hours * cfg["criticality"]
    repair_cost     = cfg["repair_base"] * mult
    labor_cost      = 2500 * (hours / 8)
    scrap_loss      = production_loss * 0.05
    total           = production_loss + repair_cost + labor_cost + scrap_loss
    return {
        "machine_id":              machine_id,
        "root_cause":              root_cause,
        "downtime_hours_estimate": hours,
        "breakdown": {
            "production_loss": round(production_loss),
            "repair_cost":     round(repair_cost),
            "labor_cost":      round(labor_cost),
            "scrap_loss":      round(scrap_loss),
        },
        "total_impact":    round(total),
        "expected_impact": round(total * confidence),
        "currency":        "INR",
        "severity":        "HIGH" if total > 80000 else ("MEDIUM" if total > 40000 else "LOW"),
    }
