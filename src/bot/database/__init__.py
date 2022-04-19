from pymongo import MongoClient

from config import Config


client = MongoClient(Config.db_host)
db = client["ShoplistDB"]

shoplist_collection = db["shoplist"]
users_collection = db["users"]
