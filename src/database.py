from pymongo import MongoClient

client = MongoClient(
    "mongodb://admin:password@mongodb-service:27017/"
)

db = client["hotel_db"]

reservations = db["reservations"]

hotels = db["hotels"]



