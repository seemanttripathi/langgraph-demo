from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama

from app.state import ResearchState
from app.llm import get_llm

llm = get_llm()

def router_node(state: ResearchState):
    prompt = f'''
    You are a routing assistant.

    Decide whether the user's question requires detailed research
    or can be answered directly.

    Return ONLY one of these two values:

    RESEARCH
    DIRECT

    User question:
    {state["query"]}
    '''

    response = llm.invoke(prompt)

    route = response.content.strip().upper()

    if "RESEARCH" in route:
        return {"route": "research"}

    return {"route": "direct"}

def direct_answer_node(state: ResearchState):
    prompt = f'''
    Answer the user's question directly and concisely.

    User question:
    {state["query"]}
    '''

    response = llm.invoke(prompt)

    return {
        "answer": response.content
    }

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

# routing function
def route_after_planner(state: ResearchState):
    if state["route"] == "research":
        return "researcher"
    return "direct"

def build_graph():
    graph = StateGraph(ResearchState)
    
    graph.add_node("planner", planner_node)
    graph.add_node("router", router_node)
    graph.add_node("researcher", research_node)
    graph.add_node("direct", direct_answer_node)
    

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "router")

    graph.add_conditional_edges(
        "router",
        route_after_planner,
        {
            "researcher": "researcher",
            "direct": "direct",
        }
    )

    graph.add_edge("researcher", END)
    graph.add_edge("direct", END)

    return graph.compile()

