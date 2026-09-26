# LangGraph Research Assistant

## Right now:

```text
                    ┌── Web Research ─────┐
                    │                     │
Router → fan-out ───┤                     ├→ Synthesizer
                    │                     │
                    └── RAG Subgraph ─────┘
                                               ↓
                                          🛑 INTERRUPT
                                               ↓
                                         Human approval
                                               ↓
                                          Fact Checker
                                               ↓
                                              END




                    ┌── Web Search ─────┐
                    │                   │
Query → Planner → Router                ├→ Synthesizer
                    │                   │       ↓
                    └── RAG ────────────┘    Approval
                                                ↓
                                           interrupt()
                                                ↓
                                             PAUSE
                                                ↓
                                  Command(resume="approved")
                                                ↓
                                          approval=approved
                                                ↓
                                               END
```