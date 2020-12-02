import uvicorn
import uuid
import datetime

from fastapi import FastAPI

from app.input import AddInput
from app.db import DataBase
from app.scheduler import Scheduler
from app.parser import Parser

app = FastAPI(title="Avito-checker")

scheduler = Scheduler()
scheduler.start()

db = DataBase()

parser = Parser()


def update_task(id_pair, search_phrase, region):
    timestamp = datetime.datetime.now()
    value = parser.get_number_of_proposals(search_phrase, region)  # приходит из парсера
    db.add_counter(id_pair, value, timestamp)
    scheduler.schedule_task(60, update_task, (id_pair, search_phrase, region,))  # 3600 сек = 1 час


@app.post(
    "/add/",
    response_description="Generated id_pair of pair <search phrase, region>",
    description="Add pair <search phrase, region> to database",
)
def add(input_data: AddInput) -> dict:
    """It takes one parameter (class AddInput)
    and returns the id_pair (unique identifier of the pair <search phrase, region>)
    Parameters
    ----------
    :param input_data: AddInput
        object of the AddInput class that represent the data model of input
    Returns
    -------
    dict
        a dict like {"id_pair": generated_id}
    """

    search_phrase = input_data.search_phrase
    region = input_data.region
    if search_phrase == "" or region == "":
        return {"error": "input data cannot be empty"}

    id_pair = str(uuid.uuid4())
    date_registration = datetime.datetime.now()
    db.registration_pair_in_db(id_pair, search_phrase, region, date_registration)

    update_task(id_pair, search_phrase, region)

    top_5_ads = parser.get_top5(search_phrase, region)
    db.add_top5(id_pair, date_registration, top_5_ads)

    return {"id_pair": id_pair}


@app.get(
    "/stat/",
    response_description="Statistics for the search phrase",
    description="Statistics for a specific search phrase with id_pair <search phrase, region>",
)
def stat(id_pair: str, interval: int) -> dict:
    """It takes two parameters (id pair, interval)
    and returns dict with statistics for a specific search phrase with id_pair
    Parameters
    ----------
    :param id_pair:  str
        unique identifier of the pair <search phrase, region> (max_length=56)
    :param interval: int
        the time interval in hours for which you need to collect statistics (max_length=64)
    Returns
    -------
    dict
        a dict like {"statistics": [some statistics]}
    """
    if interval < 1:
        return {"error": "interval should be > 0"}

    date_registration = db.get_date_registration(id_pair)
    if not date_registration:
        return {"error": "invalid id_pair"}

    limit = date_registration + datetime.timedelta(minutes=interval)  # hours=interval
    list_statistics = db.find_statistics_with_limit(id_pair, limit)
    return {"statistics": list_statistics}


@app.get(
    "/top5/",
    response_description="Top 5 ads for the search phrase",
    description="Top 5 ads on the avito site for pair with id pair",
)
def top5(id_pair: str) -> dict:
    """It takes one parameters (id pair)
    and returns dict with top 5 ads on the avito site for pair with id pair
    Parameters
    ----------
    :param id_pair:  str
        unique identifier of the pair <search phrase, region> (max_length=56)
    Returns
    -------
    dict
        a dict like {
            "id_pair": id_pair,
            "top": top
        }
    """
    result = db.get_top5_from_db(id_pair)
    if result:
        return result
    else:
        return {"error": "invalid id_pair"}

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8000)
