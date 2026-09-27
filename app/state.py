from typing import TypedDict

class ResearchState(TypedDict):
    query: str
    plan: str
    route: str
    web_research: str
    knowledge_research: str
    answer: str
    approval: str
    review: str
    review_count: int
