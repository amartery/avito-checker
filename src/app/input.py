from pydantic import BaseModel
from pydantic import Field


class AddInput(BaseModel):
    """
    A class used to represent the data model of method Add
    Attributes
    ----------
    search_phrase: str
        search phrase is query string for search (max_length=128)
    region: str
        some search region (max_length=64)
    """
    search_phrase: str = Field(..., title="Text", description="Search phrase", max_length=128)
    region: str = Field(..., title="Text", description="Region", max_length=64)
