from datetime import datetime

def run_supervisor_agent(machine_id, sensor_data, root_cause_result, knowledge_result, impact_result, alert_result):
    cause    = root_cause_result["root_cause"]
    conf     = root_cause_result["confidence_pct"]
    total    = impact_result["total_impact"]
    priority = alert_result["priority"]
    evidence = "; ".join(root_cause_result["evidence"]) if root_cause_result["evidence"] else "sensor deviation detected"
    summary  = (
        f"ADIAP detected an anomaly on {machine_id} at {datetime.utcnow().strftime('%H:%M UTC')}. "
        f"AI analysis identified {cause} as the most likely root cause with {conf}% confidence. "
        f"Evidence: {evidence}. "
        f"Estimated business impact: Rs{total:,}. "
        f"Priority: {priority}. "
        f"Recommended action: {knowledge_result['suggested_fix']}"
    )
    return {
        "machine_id":        machine_id,
        "timestamp":         datetime.utcnow().isoformat(),
        "executive_summary": summary,
        "root_cause":        cause,
        "confidence_pct":    conf,
        "evidence":          root_cause_result["evidence"],
        "similar_incidents": knowledge_result["similar_incidents"],
        "technician_notes":  knowledge_result["technician_notes"],
        "suggested_fix":     knowledge_result["suggested_fix"],
        "business_impact":   impact_result,
        "priority":          priority,
        "whatsapp_message":  alert_result["message"],
        "agents_ran":        ["DowntimeDetection","RootCause","KnowledgeBrain","BusinessImpact","Alert","Supervisor"],
    }
