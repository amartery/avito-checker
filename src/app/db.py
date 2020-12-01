import pymongo


class DataBase:
    def __init__(self):
        client = pymongo.MongoClient('mongodb', 27017)  # 'localhost'
        db = client['avito-db']
        self.registration_pairs = db['registration_pairs']
        self.counters = db['counters']

    def add_counter(self, id_pair, value, timestamp):
        counter = {
            "id_pair": id_pair,
            "value": value,  # приходит из парсера
            "timestamp": timestamp,
        }
        self.counters.insert_one(counter)

    def registration_pair_in_db(self, id_pair, search_phrase, region, date_registration):
        search_pair = {
            "id_pair": id_pair,
            "search_phrase": search_phrase,
            "region": region,
            "date_registration": date_registration,
        }
        self.registration_pairs.insert_one(search_pair)

    def find_statistics_with_limit(self, id_pair, limit):
        result = []
        for item in self.counters.find():
            if item["id_pair"] == id_pair:
                if item["timestamp"] <= limit:
                    result.append({
                        "value": item["value"],
                        "timestamp": item["timestamp"]
                    })
        return result

    def get_date_registration(self, id_pair):
        date_registration = None
        for item in self.registration_pairs.find():
            if item["id_pair"] == id_pair:
                date_registration = item["date_registration"]
        return date_registration

# ----------------------------------------------------------------------
# Без бд, данные хранятся в python структурах
# ----------------------------------------------------------------------
# registration_pairs = []
# counters = []
#
#
# def write_to_file(filename, obj):
#     with open(filename, "w") as file:
#         for item in obj:
#             print(item, file=file)
#
#
# def add_counter(id_pair, value, timestamp):
#     counter = {
#         "id_pair": id_pair,
#         "value": value,  # приходит из парсера
#         "timestamp": timestamp,
#     }
#     counters.append(counter)
#     write_to_file("counters.txt", counters)
#
#
# def registration_pair_in_db(id_pair, search_phrase, region, date_registration):
#     search_pair = {
#         "id_pair": id_pair,
#         "search_phrase": search_phrase,
#         "region": region,
#         "date_registration": date_registration,
#     }
#     registration_pairs.append(search_pair)
#     write_to_file("registration_pairs.txt", registration_pairs)
#
#
# def find_statistics_with_limit(id_pair, limit):
#     result = []
#     for item in counters:
#         if item["id_pair"] == id_pair:
#             if item["timestamp"] <= limit:
#                 result.append({
#                     "value": item["value"],
#                     "timestamp": item["timestamp"]
#                 })
#     return result
#
#
# def get_date_registration(id_pair):
#     date_registration = None
#     for item in registration_pairs:
#         if item["id_pair"] == id_pair:
#             date_registration = item["date_registration"]
#     return date_registration




