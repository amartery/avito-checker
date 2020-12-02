import pymongo
import datetime


class DataBase:
    """A class is used for working with the database"""

    def __init__(self):
        # connecting to the standard host and port
        client = pymongo.MongoClient('mongodb', 27017)  # 'localhost' 'mongodb'
        # getting the database with name 'avito-db'
        db = client['avito-db']
        # getting a collections 'registration_pairs' and 'counters' and 'top5'
        self.registration_pairs = db['registration_pairs']
        self.counters = db['counters']
        self.top5 = db['top5']

    def add_counter(self, id_pair: str, value: int, timestamp: datetime.datetime) -> None:
        """It takes three parameters (id_pair, value, timestamp)
        and save it in the database in collection 'counters'
        Parameters
        ----------
        :param id_pair: str
            unique identifier of the pair <search phrase, region>
        :param value: int
            the number of listings at the moment
        :param timestamp: datetime.datetime
            current time
        """
        counter = {
            "id_pair": id_pair,
            "value": value,
            "timestamp": timestamp,
        }
        self.counters.insert_one(counter)

    def registration_pair_in_db(self,
                                id_pair: str,
                                search_phrase: str,
                                region: str,
                                date_registration: datetime.datetime) -> None:
        """It takes four parameters (id_pair, search_phrase, region, date_registration)
        and save it in the database in collection 'registration_pairs'
        Parameters
        ----------
        :param id_pair: str
            unique identifier of the pair <search phrase, region>
        :param search_phrase: str
            some search phrase
        :param region: str
            some geographical region
        :param date_registration: datetime.datetime
            current time
        """
        search_pair = {
            "id_pair": id_pair,
            "search_phrase": search_phrase,
            "region": region,
            "date_registration": date_registration,
        }
        self.registration_pairs.insert_one(search_pair)

    def find_statistics_with_limit(self, id_pair: str, limit: datetime.datetime) -> list:
        """It takes two parameters (id_pair, limit)
        and finds entries in the collection 'counters' made before a certain time (limit)
        Parameters
        ----------
        :param id_pair: str
            unique identifier of the pair <search phrase, region>
        :param limit: datetime.datetime
            some limit for time interval
        Returns
        -------
        list
            a list of dicts like [{"value": some_value, "timestamp": timestamp}, ...]
        """
        result = []
        for item in self.counters.find():
            if item["id_pair"] == id_pair:
                if item["timestamp"] <= limit:
                    result.append({
                        "value": item["value"],
                        "timestamp": item["timestamp"]
                    })
        return result

    def get_date_registration(self, id_pair: str) -> datetime.datetime:
        """It takes one parameters (id_pair)
        and returns the time of registration of this pair (adding it to the database)
        Parameters
        ----------
        :param id_pair: str
            unique identifier of the pair <search phrase, region>
        Returns
        -------
        datetime.datetime
            time registration for id_pair
        """
        date_registration = None
        for item in self.registration_pairs.find():
            if item["id_pair"] == id_pair:
                date_registration = item["date_registration"]
        return date_registration

    def add_top5(self, id_pair: str, date: datetime.datetime, top: dict) -> None:
        """It takes two parameters (id_pair, top)
        and save it in the database in collection 'top5'
        Parameters
        ----------
        :param id_pair: str
            unique identifier of the pair <search phrase, region>
        :param date:
            date of getting the top 5
        :param top: dict
            dict with  top 5 ads
        """
        top5_dict = {
            "id_pair": id_pair,
            "date": date,
            "top": top
        }
        self.top5.insert_one(top5_dict)

    def get_top5_from_db(self, id_pair: str) -> dict:
        """It takes one parameter (id_pair)
        and find top 5 ads in collection 'top5' for pair with id_pair
        Parameters
        ----------
        :param id_pair: str
            unique identifier of the pair <search phrase, region>
        Returns
        -------
        dict
            a dict like {
                "id_pair": id_pair,
                "top": top
            } or None
        """
        result = self.top5.find_one({"id_pair": id_pair}, {'_id': 0})  # exclude the "_id" from the output
        return result
