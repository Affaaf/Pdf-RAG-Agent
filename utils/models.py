from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
    response_type: str

class SearchResponse(BaseModel):
    content: str
    score: float
    page_number: int
    file_name: str
