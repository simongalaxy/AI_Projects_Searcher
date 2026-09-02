from langgraph.graph import StateGraph, START, END

from src.Core.State import AgentState
from src.Util.logger import Logger
from src.Core.Nodes import (
    parse_query_node,
    # check_database_node,
    fetch_and_save_node,
    # retrieve_prs_node,
    # generate_summary_node,
    # routing_condition
)

def load_workflow():
    
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("parse_query", parse_query_node)
    # workflow.add_node("check_database", check_database_node)
    workflow.add_node("fetch_and_save", fetch_and_save_node)
    # workflow.add_node("retrieve_prs", retrieve_prs_node)
    # workflow.add_node("generate_summary", generate_summary_node)

    # Standard Linear Edges 
    workflow.add_edge(START, "parse_query")
    workflow.add_edge("parse_query", "fetch_and_save")
    workflow.add_edge("fetch_and_save", END)

    # # Conditional Routing Edge
    # workflow.add_conditional_edges(
    #     "check_database",
    #     routing_condition,
    #     {
    #         "fetch_and_save": "fetch_and_save",
    #         "retrieve_prs": "retrieve_prs"
    #     }
    # )

    # Compile into an executable application
    app = workflow.compile()
    
    return app