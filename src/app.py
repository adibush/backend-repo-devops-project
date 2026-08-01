from flask import Flask, request
from flask_cors import CORS

from reservation import (
    create_reservation,
    find_reservation,
    delete_reservation,
    get_hotels,
)

app = Flask(__name__)
CORS(app, origins=["http://localhost:8080"])


@app.route("/")
def home():
    return "Backend connected to MongoDB!"


@app.route("/reservation", methods=["POST"])
def create():

    data = request.get_json()

    return create_reservation(data)


@app.route("/reservation/<reservation_id>", methods=["GET"])
def get(reservation_id):

    return find_reservation(reservation_id)


@app.route("/reservation/<reservation_id>", methods=["DELETE"])
def delete(reservation_id):

    return delete_reservation(reservation_id)


@app.route("/hotels", methods=["GET"])
def hotels():

    return get_hotels()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
