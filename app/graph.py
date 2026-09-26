from langgraph.graph import StateGraph, START, END
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt

from app.state import ResearchState
from app.llm import get_llm
from app.retrieval import retrieve
from app.rag_graph import build_rag_graph

llm = get_llm()
search = DuckDuckGoSearchRun()
rag_graph = build_rag_graph()

def approval_node(state: ResearchState):
    decision = interrupt({
        "question": "Do you approve this research result?",
        "answer": state["answer"],
    })

    return {
        "approval": decision
    }

def web_research_node(state: ResearchState):
    # Step 1: Perform the Seatch
    query = state["query"]
    search_results = search.invoke(query)

    # Step 2: USer Search outcome to tune it with llm
    prompt = f'''
    You are a web research specialist.

    Use the following web search results to analyze the user's question.

    User question:
    {query}

    Research plan:
    {state["plan"]}

    Web search results:
    {search_results}

    Extract the important facts and information relevant to the
    user's question.

    Do not invent information that is not supported by the
    search results.
    '''

    # response = llm.invoke(prompt)
    return {
        "web_research": search_results
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
    graph.add_node("knowledge_researcher", rag_graph)
    graph.add_node("synthesizer", synthesizer_node)

    graph.add_node("start_research", lambda state: {})

    graph.add_node("approval", approval_node)

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

    graph.add_edge("synthesizer", "approval")
    
    graph.add_edge("approval", END)
    graph.add_edge("direct", END)

    checkpointer = InMemorySaver()

    return graph.compile(
        checkpointer=checkpointer
    )

