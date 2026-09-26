# LangGraph Research Assistant

## Right now:

```text
                         ┌── DuckDuckGo → Qwen ─────┐
                         │                          │
START → Planner → Router ┤                          ├→ Synthesizer → END
                         │                          │
                         └── Qdrant → Qwen ─────────┘


Main Graph
    ↓
knowledge_researcher
    ↓
RAG Subgraph
    ├── retrieve
    └── generate
    ↓
knowledge_research
    ↓
Main Graph
    ↓
Synthesizer
```