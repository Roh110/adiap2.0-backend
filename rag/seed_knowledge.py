def query_knowledge(query, machine_id=None, n_results=4):
    KB = {
        "Bearing Wear": [
            {"text": "CNC-01 bearing replaced after temperature exceeded 68C. Found metal shavings in lubricant. Replaced SKF 6205 bearing. Back online in 6 hours.", "metadata": {"machine": "CNC-01", "type": "technician_note"}, "distance": 0.12},
            {"text": "Bearing wear on X-axis ballscrew detected early via 15C temperature rise. Replaced before failure. Avoided 2-day unplanned downtime.", "metadata": {"machine": "CNC-01", "type": "technician_note"}, "distance": 0.18},
            {"text": "Incident CNC-01: Bearing Wear. Duration 8h. Cost Rs45000. Resolution: Replaced spindle bearing. Temp 69C, vibration 3.1 mm/s.", "metadata": {"machine": "CNC-01", "cause": "Bearing Wear", "cost": "45000", "type": "incident"}, "distance": 0.15},
            {"text": "Incident PUMP-01: Bearing Wear. Duration 6h. Cost Rs22000. Resolution: Replaced impeller bearings. Detected via gradual vibration increase.", "metadata": {"machine": "PUMP-01", "cause": "Bearing Wear", "cost": "22000", "type": "incident"}, "distance": 0.21},
        ],
        "Lubrication Failure": [
            {"text": "PUMP-01 lubrication failure on shaft seal. Added grease via zerk fitting. Seal replaced after scheduled maintenance.", "metadata": {"machine": "PUMP-01", "type": "technician_note"}, "distance": 0.14},
            {"text": "Lubrication line blocked on press gibs. Surfaces running dry, current increased 2.5A. Flushed lube lines.", "metadata": {"machine": "PRESS-01", "type": "technician_note"}, "distance": 0.19},
            {"text": "Incident PRESS-01: Lubrication Failure. Duration 5h. Cost Rs18000. Resolution: Hydraulic oil contaminated. Full drain and refill ISO 46.", "metadata": {"machine": "PRESS-01", "cause": "Lubrication Failure", "cost": "18000", "type": "incident"}, "distance": 0.16},
        ],
        "Misalignment": [
            {"text": "PUMP-01 vibration spiked to 4.2 mm/s. Traced to misalignment after maintenance. Realigned coupling, vibration dropped to 0.9 mm/s.", "metadata": {"machine": "PUMP-01", "type": "technician_note"}, "distance": 0.13},
            {"text": "Incident PRESS-01: Misalignment. Duration 3h. Cost Rs9000. Resolution: Drive coupling laser aligned. Angular misalignment 0.6 degrees.", "metadata": {"machine": "PRESS-01", "cause": "Misalignment", "cost": "9000", "type": "incident"}, "distance": 0.17},
        ],
        "Motor Overload": [
            {"text": "Motor overload tripped at 22A rated 18A. Found swarf blocking coolant nozzle. Cleared obstruction and reset relay.", "metadata": {"machine": "CNC-01", "type": "technician_note"}, "distance": 0.11},
            {"text": "Incident PRESS-01: Motor Overload. Duration 12h. Cost Rs78000. Resolution: Motor rewound after sustained overload. Current was 31A vs 20A rated.", "metadata": {"machine": "PRESS-01", "cause": "Motor Overload", "cost": "78000", "type": "incident"}, "distance": 0.14},
        ],
    }
    for cause, docs in KB.items():
        if cause.lower() in query.lower():
            return docs[:n_results]
    return KB["Bearing Wear"][:n_results]
