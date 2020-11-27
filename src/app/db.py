import pymongo
import datetime


# client = pymongo.MongoClient('mongodb', 27017)
# db = client['avito-db']
#
# registration_pairs = db['registration_pairs']
# counters = db['counters']


registration_pairs = []
counters = []


def write_to_file(filename, obj):
    with open(filename, "w") as file:
        for item in obj:
            print(item, file=file)


def add_counter(id_pair, value, timestamp):
    counter = {
        "id_pair": id_pair,
        "value": value,  # приходит из парсера
        "timestamp": timestamp,
    }
    counters.append(counter)
    write_to_file("counters.txt", counters)


def registration_pair_in_db(id_pair, search_phrase, region, date_registration):
    search_pair = {
        "id_pair": id_pair,
        "search_phrase": search_phrase,
        "region": region,
        "date_registration": date_registration,
    }
    registration_pairs.append(search_pair)
    write_to_file("registration_pairs.txt", registration_pairs)


def find_statistics_with_limit(id_pair, limit):
    result = []
    for item in counters:
        if item["id_pair"] == id_pair:
            if item["timestamp"] <= limit:
                result.append({
                    "value": item["value"],
                    "timestamp": item["timestamp"]
                })
    return result


def get_date_registration(id_pair):
    date_registration = None
    for item in registration_pairs:
        if item["id_pair"] == id_pair:
            date_registration = item["date_registration"]
    return date_registration




