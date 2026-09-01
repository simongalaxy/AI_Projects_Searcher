from typing import TypedDict, List, Annotated

from src.Data.DataClasses import ParsedQuery


class State(TypedDict): # to store the overall state of the system, including the parsed query and the news items.
    original_query: str
    parsed_query: ParsedQuery
    next_node: str
    search_results: List[dict]
    media_summary: str