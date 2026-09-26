from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama

from app.state import ResearchState
from app.llm import get_llm

llm = get_llm()

def planner_node(state: ResearchState):
    prompt = f'''
    You are a research planner.

    Create a short plan for answering the user's question.

    Break the task into 3 to 5 clear steps.

    User question:
    {state["query"]}
    '''

    response = llm.invoke(prompt)
    return {
        'plan': response.content
    }

def research_node(state: ResearchState):
    prompt = f'''
    You are a research assistant.
    Answer the user's question clearly and concisely.

    User question:
    {state["query"]}

    Research plan:
    {state["plan"]}

    Provide a clear and useful answer.
    '''
    response = llm.invoke(prompt)
    return {
        "answer": response.content
    }

def build_graph():
    graph = StateGraph(ResearchState)
    
    graph.add_node("researcher", research_node)
    graph.add_node("planner", planner_node)

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "researcher")
    graph.add_edge("researcher", END)

    return graph.compile()

