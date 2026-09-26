from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.llm import get_llm
from app.retrieval import retrieve

llm = get_llm()

class RAGState(TypedDict):
    query: str
    plan: str
    context: str
    knowledge_research: str

def retrieve_node(state: RAGState):
    documents = retrieve(
        state["query"],
        k=3,
    )

    context = "\n\n".join(
        f"Source: {doc.metadata.get('source')}\n"
        f"Content: {doc.page_content}"
        for doc in documents
    )

    return {
        "context": context
    }

def generate_node(state: RAGState):
    prompt = f"""
    You are a knowledge-base research specialist.

    Answer the user's question using ONLY the retrieved knowledge.

    User question:
    {state["query"]}

    Research plan:
    {state["plan"]}

    Retrieved knowledge:
    {state["context"]}

    Provide the important facts and technical details
    relevant to the user's question.

    If the retrieved knowledge does not contain enough
    information to answer the question, say so rather
    than inventing information.
    """

    # response = llm.invoke(prompt)

    return {
        "knowledge_research": state["context"]
    }

def build_rag_graph():
    graph = StateGraph(RAGState)

    graph.add_node("retrieve", retrieve_node)
    graph.add_node("generate", generate_node)

    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)

    return graph.compile()