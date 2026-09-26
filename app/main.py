from fastapi import FastAPI
from app.graph import build_graph

app = FastAPI(title='langGraph Research Assistant')
graph = build_graph()

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/research")
def research(query: str):
    result = graph.invoke({
        "query": query,
        "plan": "",
        "answer": "",
    })
    return result