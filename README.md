# LangGraph Research Assistant

## Right now:

```text
                    Checkpointer
                        │
                        ▼
Request → LangGraph → State → checkpoint
                         │
                         ▼
                    Resume later



             Checkpointer
                  │
       ┌──────────┴──────────┐
       ↓                     ↓
 research-1              research-2
       │                     │
    State A               State B




                 InMemorySaver
                      │
          ┌───────────┴───────────┐
          │                       │
     research-1              research-2
          │                       │
      checkpoints             checkpoints
          │                       │
     execution A              execution B
```