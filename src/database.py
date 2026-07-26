import os
from urllib.parse import quote_plus

from pymongo import MongoClient

mongo_host = os.getenv("MONGO_HOST")
mongo_hosts = os.getenv("MONGO_HOSTS")
mongo_port = os.getenv("MONGO_PORT")
database_name = os.getenv("DATABASE_NAME")
mongo_replica_set = os.getenv("MONGO_REPLICA_SET")
mongo_auth_source = os.getenv("MONGO_AUTH_SOURCE", "admin")
mongo_username = os.getenv("MONGO_USERNAME")
mongo_password = os.getenv("MONGO_PASSWORD")

encoded_username = quote_plus(mongo_username)
encoded_password = quote_plus(mongo_password)

if mongo_hosts and mongo_replica_set:
    mongo_uri = (
        f"mongodb://{encoded_username}:{encoded_password}@"
        f"{mongo_hosts}/{database_name}"
        f"?replicaSet={mongo_replica_set}&authSource={mongo_auth_source}"
    )
else:
    mongo_uri = f"mongodb://{encoded_username}:{encoded_password}@{mongo_host}:{mongo_port}/"

client = MongoClient(mongo_uri)

db = client[database_name]

reservations = db["reservations"]

hotels = db["hotels"]


