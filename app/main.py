import json
# from dataclasses import asdict, is_dataclass

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from app.graph import build_graph
from langgraph.types import Command

from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title='langGraph Research Assistant')
graph = build_graph()

# def serialize_event(event):
#     if "__interrupt__" in event:
#         interrupts = event["__interrupt__"]

#         event["__interrupt__"] = [
#             asdict(item) if is_dataclass(item) else str(item)
#             for item in interrupts
#         ]

#     return event

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
        yield f"data: {json.dumps(event, default=str)}\n\n"

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/research")
def research(query: str):

    return StreamingResponse(
        generate_events(query),
        media_type="text/event-stream",
    )

@app.post("/research/resume")
def resume_research():

    config = {
        "configurable": {
            "thread_id": "research-1"
        }
    }

    result = graph.invoke(
        Command(resume="approved"),
        config=config,
    )

    return result