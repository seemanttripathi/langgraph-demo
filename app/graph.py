from langgraph.graph import StateGraph, START, END

from app.state import ResearchState

def research_node(state: ResearchState):
    return {
        "answer": f"You asked {state['query']}"
    }

def build_graph():
    graph = StateGraph(ResearchState)
    
    graph.add_node("research", research_node)

    graph.add_edge(START, "research")
    graph.add_edge("research", END)

    return graph.compile()

