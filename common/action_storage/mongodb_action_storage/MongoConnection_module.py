from pymongo import MongoClient
from common.utilities.utilities import get_dir_path, read_json

_APP_PATH = get_dir_path()
app_config = read_json("{}/config/appConfig.dat".format(_APP_PATH))
_MONGO_URL = app_config['mongo_url']

print("Getting connection")
conn = MongoClient(_MONGO_URL)
