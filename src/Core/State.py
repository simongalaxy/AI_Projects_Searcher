from typing import TypedDict, List

from Data.DataClasses import NewsItem, ParsedQuery


class State(TypedDict): # to store the overall state of the system, including the parsed query and the news items.
    original_query: str
    parsed_query: ParsedQuery
    dates: List[str]
    date_urls: List[str]
    news_urls: List[str]
    news_items: List[NewsItem]
    search_results: List[dict]
    media_summary: str