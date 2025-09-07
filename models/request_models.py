from pydantic import BaseModel

class PageInfo(BaseModel):
    page: int = 1
    limit: int = 10

class SearchRequest(BaseModel):
    search_message: str
    page_info: PageInfo
