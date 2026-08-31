from langgraph.graph import StateGraph, END

from Core.State import State


def load_workflow(state: State) -> None:
    workflow = StateGraph(state)

    # Add Nodes
    workflow.add_node("parse_query", parse_query_node)
    workflow.add_node("check_database", check_database_node)
    workflow.add_node("fetch_and_save", fetch_and_save_node)
    workflow.add_node("retrieve_prs", retrieve_prs_node)
    workflow.add_node("generate_summary", generate_summary_node)

    # Set Entry Point
    workflow.set_entry_point("parse_query")

    # Standard Linear Edges
    workflow.add_edge("parse_query", "check_database")
    workflow.add_edge("fetch_and_save", "retrieve_prs")
    workflow.add_edge("retrieve_prs", "generate_summary")
    workflow.add_edge("generate_summary", END)

    # Conditional Routing Edge
    workflow.add_conditional_edges(
        "check_database",
        routing_condition,
        {
            "fetch_and_save": "fetch_and_save",
            "retrieve_prs": "retrieve_prs"
        }
    )

    # Compile into an executable application
    app = workflow.compile()
    
    return