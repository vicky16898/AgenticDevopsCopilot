from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.nodes.analysis import analyze_repo_node
from app.agents.nodes.risk import assess_risk_node
from app.agents.nodes.patch import generate_patch_node

workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("analyze_repo", analyze_repo_node)
workflow.add_node("assess_risk", assess_risk_node)
workflow.add_node("generate_patch", generate_patch_node)

# Set Entry Point
workflow.set_entry_point("analyze_repo")

# Define Edges
workflow.add_edge("analyze_repo", "assess_risk")
workflow.add_edge("assess_risk", "generate_patch")
workflow.add_edge("generate_patch", END)

# Compile
app_graph = workflow.compile()
