import os
# os.environ["PYMONGOIM__OPERATING_SYSTEM"] = "windows"
# os.environ["PYMONGOIM__OS_VERSION"] = "generic"
# os.environ["PYMONGOIM__MONGOD_PORT"] = "27017"


# set PYMONGOIM__OPERATING_SYSTEM=windows
# set PYMONGOIM__OS_VERSION=generic
# set PYMONGOIM__MONGOD_PORT=27017


from pymongo_inmemory import MongoClient
from datetime import datetime
import inspect
import json


# PYMONGOIM__OPERATING_SYSTEM=ubuntu
# PYMONGOIM__OS_VERSION=22
# PYMONGOIM__MONGOD_PORT=27017


client = MongoClient()

COMMON_DIRECTORY_PATH = os.path.dirname(os.path.abspath(inspect.getfile(lambda: 0)))

database = client.get_database('black-coffer')

def get_records_collection():
    records = database.get_collection('records')
    indexes = records.index_information()
    keys_to_index = ['intensity', 'likelihood', 'relevance', 'start_year', 'end_year', 'country', 'topic', 'region']
    for key in keys_to_index:
        if key not in indexes:
            records.create_index(key, name=key)
    
    return records

def initialize_records():
    with open(os.path.join(COMMON_DIRECTORY_PATH, 'data.json'), 'r') as f:
        records = json.load(f)
    for record in records:
        for key in ["published", "added"]:
            try:
                # "January, 20 2017 03:51:25"
                record[key] = datetime.strptime(record["added"], "%B, %d %Y %H:%M:%S")
            except:
                record[key] = None
        for key, val in record.items():
            if not val:
                record[key] = None
    # with open('corrected.json', 'w+') as f:
    #     json.dump(records, f, default=custom_serialize)
    get_records_collection().insert_many(records)

if __name__ == "__main__":
    initialize_records()
    client.close()