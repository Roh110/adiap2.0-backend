from app.models.alert import Alert


def create_alert(db, machine_id, state_result):

    # Only trigger alerts for dangerous states
    if state_result["state"] in ["CRITICAL", "FAILURE_IMMINENT"]:

        message = ""

        if state_result["state"] == "CRITICAL":
            message = "Machine is in CRITICAL condition. Immediate inspection required."

        elif state_result["state"] == "FAILURE_IMMINENT":
            message = "Machine failure predicted. STOP operation immediately."

        alert = Alert(
            machine_id=machine_id,
            message=message,
            risk_score=state_result["risk_score"],
            state=state_result["state"]
        )

        db.add(alert)
        db.commit()
        db.refresh(alert)

        return alert

    return None