import pymongo


client = pymongo.MongoClient('mongodb', 27017)
db = client['avito-db']

avito_pairs = db['avito_pairs']
counters = db['counters']


def add_counter(id_pair, value, timestamp):
    counter = {
        'id_pair': id_pair,
        'value': value,
        'timestamp': timestamp,
    }
    counters.insert_one(counter)


def add_to_db(id_pair, search_phrase, region):
    search_pair = {
        'id_pair': id_pair,
        'search_phrase': search_phrase,
        'region': region,
    }
    avito_pairs.insert_one(search_pair)


def get_from_db(id_pair, interval):
    avito_pairs



