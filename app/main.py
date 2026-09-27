from fastapi import FastAPI
from app.graph import build_graph
from langgraph.types import Command

app = FastAPI(title='langGraph Research Assistant')
graph = build_graph()

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/research")
def research(query: str):

    config = {
        "configurable": {
            "thread_id": "research-1"
        }
    }


    result = graph.invoke({
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
    )

    # print("\n========== FINAL STATE ==========")
    # print(result)

    # print("\n========== CHECKPOINT HISTORY ==========")

    # for checkpoint in graph.get_state_history(config):
    #     print("\n--------------------------------")
    #     print(
    #         "Checkpoint ID:",
    #         checkpoint.config["configurable"].get("checkpoint_id")
    #     )
    #     print("State:")
    #     print(checkpoint.values)

    result = graph.invoke(
    Command(resume="approved"),
    config=config,
)

    return result