# LangGraph Research Assistant

## Right now:
              ┌───────────┐
              │   START   │
              └─────┬─────┘
                    │
                    ▼
              ┌───────────┐
              │  Planner  │
              └─────┬─────┘
                    │
             plan gets added
                    │
                    ▼
              ┌───────────┐
              │ Researcher│
              └─────┬─────┘
                    │
            answer gets added
                    │
                    ▼
              ┌───────────┐
              │    END    │
              └───────────┘

## Conceptually:
                    STATE
                      │
        ┌─────────────┼─────────────┐
        │             │             │
      query          plan         answer
        │             │             │
        │             │             │
        ▼             │             │
     Planner ─────────┘             │
                      │             │
                      ▼             │
                  Researcher ───────┘

## Note:
The Planner doesn't call the Researcher.
The Researcher doesn't call the Planner.
They don't know that the other node exists.
They only know about the state.
The graph controls the orchestration