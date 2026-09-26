from langgraph.graph import StateGraph, START, END

from app.state import ResearchState
from app.llm import get_llm

llm = get_llm()

def web_research_node(state: ResearchState):
    prompt = f'''
    You are a web research specialist.

    Analyze the user's question from the perspective of
    information that would typically be gathered from
    external sources.

    Provide important facts, perspectives, and areas that
    should be investigated.

    User question:
    {state["query"]}

    Research plan:
    {state["plan"]}
    '''

    response = llm.invoke(prompt)
    return {
        "web_research": response.content
    }

def knowledge_research_node(state: ResearchState):
    prompt = f'''
    You are a knowledge-base research specialist.

    Analyze the user's question using your existing knowledge.
    Focus on concepts, technical details, definitions,
    and important relationships.

    User question:
    {state["query"]}

    Research plan:
    {state["plan"]}
    '''

    response = llm.invoke(prompt)
    return {
        "knowledge_research": response.content
    }

def synthesizer_node(state: ResearchState):
    prompt = f'''
    You are a research report synthesizer.

    Combine the information from the two research branches
    into one clear and useful answer.

    User question:
    {state["query"]}

    Research plan:
    {state["plan"]}

    Web research:
    {state["web_research"]}

    Knowledge research:
    {state["knowledge_research"]}

    Produce a coherent final answer. Do not mention the
    internal research process.
    '''

    response = llm.invoke(prompt)
    return {
        "answer": response.content
    }

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

# routing function
def route_after_router(state: ResearchState):
    if state["route"] == "research":
        return "parallel_research"
    return "direct"

def build_graph():
    graph = StateGraph(ResearchState)
    
    graph.add_node("planner", planner_node)
    graph.add_node("router", router_node)
    graph.add_node("direct", direct_answer_node)

    graph.add_node("web_researcher", web_research_node)
    graph.add_node("knowledge_researcher", knowledge_research_node)
    graph.add_node("synthesizer", synthesizer_node)

    graph.add_node("start_research", lambda state: {})

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "router")

    graph.add_conditional_edges(
        "router",
        route_after_router,
        {
            "parallel_research": "start_research",
            "direct": "direct",
        }
    )

    graph.add_edge("start_research", "web_researcher")
    graph.add_edge("start_research", "knowledge_researcher")
    graph.add_edge("web_researcher", "synthesizer")
    graph.add_edge("knowledge_researcher", "synthesizer")

    graph.add_edge("synthesizer", END)
    graph.add_edge("direct", END)

    return graph.compile()

