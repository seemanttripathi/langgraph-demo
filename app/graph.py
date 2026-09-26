from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama

from app.state import ResearchState
from app.llm import get_llm

llm = get_llm()

def research_node(state: ResearchState):
    response = llm.invoke(state['query'])
    return {
        "answer": response.content
    }

def build_graph():
    graph = StateGraph(ResearchState)
    
    graph.add_node("research", research_node)

    graph.add_edge(START, "research")
    graph.add_edge("research", END)

    return graph.compile()

