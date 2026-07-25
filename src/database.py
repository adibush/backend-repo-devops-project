import os

from pymongo import MongoClient

mongo_host = os.getenv("MONGO_HOST")
mongo_port = os.getenv("MONGO_PORT")
database_name = os.getenv("DATABASE_NAME")
mongo_username = os.getenv("MONGO_USERNAME")
mongo_password = os.getenv("MONGO_PASSWORD")

mongo_uri = f"mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{mongo_port}/"

client = MongoClient(mongo_uri)

db = client[database_name]

reservations = db["reservations"]

hotels = db["hotels"]


