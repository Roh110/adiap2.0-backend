from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from agents.root_cause_agent import run_root_cause_agent
from agents.knowledge_agent  import run_knowledge_agent
from agents.impact_agent     import run_impact_agent
from agents.alert_agent      import run_alert_agent
from agents.supervisor_agent import run_supervisor_agent

class InvestigationState(TypedDict):
    machine_id:        str
    temperature:       float
    vibration:         float
    current:           float
    root_cause_result: Optional[dict]
    knowledge_result:  Optional[dict]
    impact_result:     Optional[dict]
    alert_result:      Optional[dict]
    final_report:      Optional[dict]

def node_root_cause(state):
    return {**state, "root_cause_result": run_root_cause_agent(state["machine_id"], state["temperature"], state["vibration"], state["current"])}

def node_knowledge(state):
    return {**state, "knowledge_result": run_knowledge_agent(state["machine_id"], state["root_cause_result"]["root_cause"])}

def node_impact(state):
    return {**state, "impact_result": run_impact_agent(state["machine_id"], state["root_cause_result"]["root_cause"], state["root_cause_result"]["confidence"])}

def node_alert(state):
    return {**state, "alert_result": run_alert_agent(state["machine_id"], state["root_cause_result"]["root_cause"], state["root_cause_result"]["confidence"], state["impact_result"], state["knowledge_result"]["suggested_fix"])}

def node_supervisor(state):
    return {**state, "final_report": run_supervisor_agent(state["machine_id"], {}, state["root_cause_result"], state["knowledge_result"], state["impact_result"], state["alert_result"])}

def build_workflow():
    g = StateGraph(InvestigationState)
    g.add_node("root_cause", node_root_cause)
    g.add_node("knowledge",  node_knowledge)
    g.add_node("impact",     node_impact)
    g.add_node("alert",      node_alert)
    g.add_node("supervisor", node_supervisor)
    g.set_entry_point("root_cause")
    g.add_edge("root_cause", "knowledge")
    g.add_edge("knowledge",  "impact")
    g.add_edge("impact",     "alert")
    g.add_edge("alert",      "supervisor")
    g.add_edge("supervisor", END)
    return g.compile()

investigation_workflow = build_workflow()

def run_investigation(machine_id, temperature, vibration, current):
    result = investigation_workflow.invoke({
        "machine_id": machine_id, "temperature": temperature,
        "vibration":  vibration,  "current":     current,
        "root_cause_result": None, "knowledge_result": None,
        "impact_result": None, "alert_result": None, "final_report": None,
    })
    return result["final_report"]
