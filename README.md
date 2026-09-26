# LangGraph Research Assistant

## Right now:
                         START
                           │
                           ▼
                     ┌──────────┐
                     │ Planner  │
                     └────┬─────┘
                          │
                          ▼
                     ┌──────────┐
                     │  Router  │
                     └────┬─────┘
                          │
                 ┌────────┴────────┐
                 │                 │
            route=research    route=direct
                 │                 │
                 ▼                 ▼
          ┌────────────┐     ┌────────────┐
          │ Researcher │     │   Direct   │
          └──────┬─────┘     └──────┬─────┘
                 │                  │
                 └────────┬─────────┘
                          ▼
                         END