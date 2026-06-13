FIXES = {
    "Bearing Wear":        "Inspect and replace bearings immediately. Check lubrication intervals. Estimated repair: 6-8 hours. Order SKF/FAG replacement bearing.",
    "Lubrication Failure": "Apply grease/oil to all lubrication points now. Check lube pump. Flush lines if contaminated. Estimated: 2-4 hours.",
    "Misalignment":        "Perform laser alignment check. Inspect coupling for wear. Correct to within 0.05mm tolerance. Estimated: 3-5 hours.",
    "Motor Overload":      "Check current draw. Inspect for mechanical obstruction. Verify cooling. If sustained over 130 percent FLA, plan motor inspection. Estimated: 4-12 hours.",
}

KB = {
    "Bearing Wear": {
        "notes": [
            {"text": "CNC-01 bearing replaced after temperature exceeded 68C for 3 hours. Found metal shavings in lubricant. Replaced SKF 6205 bearing. Back online in 6 hours.", "metadata": {"machine": "CNC-01", "type": "technician_note"}, "distance": 0.12},
            {"text": "Bearing wear on X-axis ballscrew detected early via 15C temperature rise. Replaced before failure. Avoided 2-day unplanned downtime.", "metadata": {"machine": "CNC-01", "type": "technician_note"}, "distance": 0.18},
        ],
        "incidents": [
            {"text": "Incident CNC-01: Bearing Wear. Duration 8h. Cost Rs45000. Resolution: Replaced spindle bearing. Temp 69C, vibration 3.1 mm/s.", "metadata": {"machine": "CNC-01", "cause": "Bearing Wear", "cost": "45000", "type": "incident"}, "distance": 0.15},
            {"text": "Incident PUMP-01: Bearing Wear. Duration 6h. Cost Rs22000. Resolution: Replaced impeller bearings. Detected via gradual vibration increase.", "metadata": {"machine": "PUMP-01", "cause": "Bearing Wear", "cost": "22000", "type": "incident"}, "distance": 0.21},
        ],
    },
    "Lubrication Failure": {
        "notes": [
            {"text": "PUMP-01 lubrication failure on shaft seal. Added grease via zerk fitting. Seal replaced after scheduled maintenance.", "metadata": {"machine": "PUMP-01", "type": "technician_note"}, "distance": 0.14},
            {"text": "Lubrication line blocked on press gibs. Surfaces running dry, current increased 2.5A. Flushed lube lines.", "metadata": {"machine": "PRESS-01", "type": "technician_note"}, "distance": 0.19},
        ],
        "incidents": [
            {"text": "Incident PRESS-01: Lubrication Failure. Duration 5h. Cost Rs18000. Resolution: Hydraulic oil contaminated. Full drain and refill ISO 46.", "metadata": {"machine": "PRESS-01", "cause": "Lubrication Failure", "cost": "18000", "type": "incident"}, "distance": 0.16},
        ],
    },
    "Misalignment": {
        "notes": [
            {"text": "PUMP-01 vibration spiked to 4.2 mm/s. Traced to misalignment after maintenance. Realigned coupling, vibration dropped to 0.9 mm/s.", "metadata": {"machine": "PUMP-01", "type": "technician_note"}, "distance": 0.13},
        ],
        "incidents": [
            {"text": "Incident PRESS-01: Misalignment. Duration 3h. Cost Rs9000. Resolution: Drive coupling laser aligned. Angular misalignment 0.6 degrees.", "metadata": {"machine": "PRESS-01", "cause": "Misalignment", "cost": "9000", "type": "incident"}, "distance": 0.17},
        ],
    },
    "Motor Overload": {
        "notes": [
            {"text": "Motor overload tripped at 22A rated 18A. Found swarf blocking coolant nozzle causing thermal buildup. Cleared obstruction and reset relay.", "metadata": {"machine": "CNC-01", "type": "technician_note"}, "distance": 0.11},
        ],
        "incidents": [
            {"text": "Incident PRESS-01: Motor Overload. Duration 12h. Cost Rs78000. Resolution: Motor rewound after sustained overload. Current was 31A vs 20A rated.", "metadata": {"machine": "PRESS-01", "cause": "Motor Overload", "cost": "78000", "type": "incident"}, "distance": 0.14},
        ],
    },
}

def run_knowledge_agent(machine_id, root_cause):
    kb = KB.get(root_cause, KB["Bearing Wear"])
    return {
        "technician_notes":  kb["notes"],
        "similar_incidents": kb["incidents"],
        "suggested_fix":     FIXES.get(root_cause, "Inspect machine and consult maintenance manual."),
        "sources_found":     len(kb["notes"]) + len(kb["incidents"]),
    }
