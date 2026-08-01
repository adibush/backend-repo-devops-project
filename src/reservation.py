from flask import jsonify
from bson import ObjectId
from datetime import datetime

from database import db, reservations, hotels


def create_reservation(data):

    db.command("ping")

    required_fields = [
        "fullName",
        "email",
        "hotelId",
        "checkIn",
        "checkOut",
    ]

    if data is None:

        return jsonify(
            {
                "message": "Missing required fields"
            }
        ), 400

    for field in required_fields:

        if field not in data or not data[field]:

            return jsonify(
                {
                    "message": "Missing required fields"
                }
            ), 400

    hotel = hotels.find_one(
        {
            "hotelId": data["hotelId"]
        }
    )

    if hotel is None:

        return jsonify(
            {
                "message": "Hotel not found"
            }
        ), 404

    try:

        check_in = datetime.strptime(data["checkIn"], "%Y-%m-%d")
        check_out = datetime.strptime(data["checkOut"], "%Y-%m-%d")

    except ValueError:

        return jsonify(
            {
                "message": "Invalid date format. Use YYYY-MM-DD"
            }
        ), 400

    if check_in.date() < datetime.today().date():

        return jsonify(
            {
                "message": "Check-in date cannot be in the past"
            }
        ), 400

    if check_out <= check_in:

        return jsonify(
            {
                "message": "Check-out date must be after check-in date"
            }
        ), 400

    overlapping_reservation = reservations.find_one(
        {
            "hotelId": data["hotelId"],
            "checkIn": {
                "$lt": data["checkOut"]
            },
            "checkOut": {
                "$gt": data["checkIn"]
            },
        }
    )

    if overlapping_reservation is not None:

        return jsonify(
            {
                "message": "Hotel is not available for the selected dates"
            }
        ), 409

    reservation = {
        "fullName": data["fullName"],
        "email": data["email"],
        "hotelId": data["hotelId"],
        "checkIn": data["checkIn"],
        "checkOut": data["checkOut"],
    }

    result = reservations.insert_one(reservation)

    return jsonify(
        {
            "message": "Reservation created successfully",
            "reservationId": str(result.inserted_id)
        }
    ), 201


def get_reservation(reservation_id):

    if not ObjectId.is_valid(reservation_id):

        return jsonify(
            {
                "message": "Reservation not found"
            }
        ), 404

    reservation = reservations.find_one(
        {
            "_id": ObjectId(reservation_id)
        }
    )

    if reservation is None:

        return jsonify(
            {
                "message": "Reservation not found"
            }
        ), 404

    reservation["_id"] = str(reservation["_id"])

    return jsonify(reservation), 200


def find_reservation(search_value):

    if ObjectId.is_valid(search_value):

        return get_reservation(search_value)

    reservation = reservations.find_one(
        {
            "$or": [
                {
                    "fullName": search_value
                },
                {
                    "email": search_value
                },
            ]
        }
    )

    if reservation is None:

        return jsonify(
            {
                "message": "Reservation not found"
            }
        ), 404

    reservation["_id"] = str(reservation["_id"])

    return jsonify(reservation), 200


def delete_reservation(reservation_id):

    if not ObjectId.is_valid(reservation_id):

        return jsonify(
            {
                "message": "Reservation not found"
            }
        ), 404

    result = reservations.delete_one(
        {
            "_id": ObjectId(reservation_id)
        }
    )

    if result.deleted_count == 0:

        return jsonify(
            {
                "message": "Reservation not found"
            }
        ), 404

    return jsonify(
        {
            "message": "Reservation deleted successfully"
        }
    ), 200


def get_hotels():

    hotels_list = list(
        hotels.find(
            {},
            {
                "_id": 0
            }
        )
    )

    return jsonify(hotels_list), 200
