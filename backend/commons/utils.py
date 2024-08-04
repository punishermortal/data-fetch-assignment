from datetime import datetime
from bson import ObjectId

def custom_serialize(val):
    if isinstance(val, datetime):
        return val.strftime("%B, %d %Y %H:%M:%S")
    if isinstance(val, ObjectId):
        return str(val)
    return val