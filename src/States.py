from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional

class ParsedQuery(BaseModel):
    start_date: str = Field(description="The beginning date, ISO date format YYYY-MM-DD")
    end_date: str | None = Field(description="The ending date, ISO date format YYYY-MM-DD")

class ExtractedData(BaseModel):
    subject_department: str = Field(description="Subject Department/Bureau issued this press release")
    summary: str = Field(description="Summary of Press Release with maximum 800 words. All names should be kept.")
    
class NewsItem(BaseModel): # to store the news items that are relevant to the user query.
    id: str = Field(description="ID of the press release")
    title: str = Field(description="title of the press release")
    content: str = Field(description="Raw Content of the press release")
    content_type: str = Field(description="Type of content in press release")
    url: str = Field(description="url of the press release")
    published_date: date = Field(description="Date published the press release")
    extracted_data: ExtractedData | None = Field(description="Extracted data from the press release, if available")
    summary_embeddings: List[float] | None
    
class State(BaseModel): # to store the overall state of the system, including the parsed query and the news items.
    original_query: str = None
    parsed_query: ParsedQuery = None
    dates: List[str] = []
    date_urls: List[str] = []
    news_urls: List[str] = []
    news_items: List[NewsItem] = []
    search_results: List[dict] = []
    

    
    
