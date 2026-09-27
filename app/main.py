import json

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from app.graph import build_graph
from langgraph.types import Command

app = FastAPI(title='langGraph Research Assistant')
graph = build_graph()

def generate_events(query: str):
    config = {
        "configurable": {
            "thread_id": "research-1"
        }
    }

    for event in graph.stream(
        {
            "query": query,
            "plan": "",
            "router": "",
            "web_research": "",
            "knowledge_research": "",
            "answer": "",
            "approval": "",
            "review_count": 0
        },
        config=config,
    ):
        yield f"data: {json.dumps(event)}\n\n"

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/research")
def research(query: str):

    return StreamingResponse(
        generate_events(query),
        media_type="text/event-stream",
    )