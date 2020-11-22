import uvicorn
import uuid

from fastapi import FastAPI
from pydantic import BaseModel
from pydantic import Field


from src.app.db import get_from_db
from src.app.db import add_to_db


app = FastAPI(title="Avito-checker")


class AddInput(BaseModel):
    """
    A class used to represent the data model of method Add input
    ...
    Attributes
    ----------
    search_phrase: str
        search phrase is query string for search (max_length=128)
    region: str
        some search region (max_length=64)
    """
    search_phrase: str = Field(..., title="Text", description="Search phrase", max_length=128)
    region: str = Field(..., title="Text", description="Region", max_length=64)


@app.post(
    "/add/",
    response_description="Generated id_pair of pair <search phrase, region>",
    description="Add pair <search phrase, region> to database",
)
def add(input_data: AddInput) -> dict:
    """It takes two  or three parameters (search phrase, region)
    and returns the id_pair (unique identifier of the pair <search phrase, region>)
    Parameters
    ----------
    input data: AddInput
        object of the AddInput class that represent the data model of input
    Returns
    -------
    dict
        a dict like {"id_pair": generated_id}
    """
    if input_data.search_phrase is "" or input_data.region is "":
        return {"error": "input data cannot be empty"}
    id_pair = str(uuid.uuid4())  # generate random sequence with uuid
    add_to_db(id_pair, search_phrase, region)
    return {"id_pair": id_pair}

