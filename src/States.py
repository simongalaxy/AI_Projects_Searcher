from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional

class ParsedQuery(BaseModel):
    start_date: str = Field(description="The beginning date, ISO date format YYYY-MM-DD")
    end_date: str | None = Field(description="The ending date, ISO date format YYYY-MM-DD")
    departments: List[str] | None = Field(description="Name of Department or Bureau")
    keywords: List[str] | None = Field(description="keywords for searching")
    action: str | None = Field(description="action to do in the query")

class Summary(BaseModel):
    id: str = Field(description="ID of the press release")
    content: str = Field(description="Summary of Press Release with maximum 800 words. All names should be kept.")
    embeddings: List[float] | None    
    
class ExtractedData(BaseModel):
    id: str = Field(description="ID of the press release")
    subject_department: str = Field(description="Subject Department/Bureau issued this press release")
    ai_related: bool = Field(description="if the content of the press release is relating to Artificial Intelligence, set True, Otherwise, False")

# class AI_Project(BaseModel):
#     project_name: str = Field(description="Name of AI project")
#     aspects_used_AI: List[str] = Field(description="Aspects applied AI, such as, data analysis, image processing, document editing")
#     AI_How_to: str = Field(description="ways to apply AI to workflow")
#     AI_tools: List[str] = Field(description="AI tools used")
#     benefits: str = Field(description="Benefits after AI adaption")
    
class NewsItem(BaseModel): # to store the news items that are relevant to the user query.
    id: str = Field(description="ID of the press release")
    title: str = Field(description="title of the press release")
    content: str = Field(description="Raw Content of the press release")
    content_type: str = Field(description="Type of content in press release")
    url: str = Field(description="url of the press release")
    published_date: date = Field(description="Date published the press release")
    extracted_data: ExtractedData | None = Field(description="Extracted data from the press release, if available")
    summary: Summary | None = Field(description="summary and its embedding of the press release")
    
class State(BaseModel): # to store the overall state of the system, including the parsed query and the news items.
    original_query: str = None
    parsed_query: ParsedQuery = None
    dates: List[str] = []
    date_urls: List[str] = []
    news_urls: List[str] = []
    news_items: List[NewsItem] = []
    search_results: List[dict] = []
    

    
    
