import uvicorn
import uuid
import datetime
import asyncio

from fastapi import FastAPI

from src.app.input import AddInput

from src.app.db import add_counter
from src.app.db import registration_pair_in_db
from src.app.db import get_date_registration
from src.app.db import find_statistics_with_limit

from src.app.scheduler import Scheduler


app = FastAPI(title="Avito-checker")

scheduler = Scheduler()
scheduler.start()


def update_task(id_pair):
    timestamp = datetime.datetime.now()  # .strftime('%H:%M:%S')
    value = 100  # приходит из парсера
    add_counter(id_pair, value, timestamp)
    scheduler.schedule_task(60, update_task, (id_pair,))  # 3600 сек = 1 час


@app.post(
    "/add/",
    response_description="Generated id_pair of pair <search phrase, region>",
    description="Add pair <search phrase, region> to database",
)
def add(input_data: AddInput) -> dict:
    """It takes two parameters (search phrase, region)
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

    id_pair = str(uuid.uuid4())  # generate random sequence with uuid
    date_registration = datetime.datetime.now()  # .strftime('%H:%M:%S')
    registration_pair_in_db(id_pair, search_phrase, region, date_registration)

    update_task(id_pair)
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
        a dict of dicts like {
            {
                "number_of_ads": value,
                "timestamp": timestamp,
            }...}
    """
    if interval < 1:
        return {"error": "interval should be > 0"}

    date_registration = get_date_registration(id_pair)
    if not date_registration:
        return {"error": "invalid id_pair"}
    limit = date_registration + datetime.timedelta(minutes=interval)  # hours=interval

    list_statistics = find_statistics_with_limit(id_pair, limit)

    return {"statistics": list_statistics}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
    loop = asyncio.get_event_loop()
    loop.run_forever()
