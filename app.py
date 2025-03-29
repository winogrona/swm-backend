import hashlib
import random

from datetime import datetime, timedelta

from flask import Flask # type: ignore
from dataclasses import dataclass
from flask import request, send_from_directory

from http import HTTPStatus

from config import config
from db import session as db, Products, Category, Materials, Machines

from enum import Enum

# We are not responsible for any psychological harm
# induced by reviewing this code.

# heeey saefjwehfhwe


class Response:
    status: int
    message: str
    data: dict

    def __init__(self, status: HTTPStatus, data: dict, message: str | None = None):
        self.status = status.value

        if message is None:
            self.message = status.phrase
        else:
            self.message = message

        self.data = data

    def to_dict(self):
        return {
            "status": self.status,
            "message": self.message,
            "data": self.data
        }

app = Flask(__name__)

@app.route("/getProducts", methods=["GET"])
def get_products():
    products = db.query(Products).all()
    products_list = [product.todict() for product in products]
    response = Response(
        status=HTTPStatus.OK,
        data={
            "products": products_list
        }
    )
    return response.to_dict(), 200

@app.route("/getProduct/<int:product_id>", methods=["GET"])
def get_product(product_id: int):
    product = db.query(Products).filter(Products.id == product_id).first()
    if product is None:
        response = Response(
            status=HTTPStatus.NOT_FOUND,
            data={},
            message="Product not found"
        )
        return response.to_dict(), 404

    response = Response(
        status=HTTPStatus.OK,
        data={
            "product": product.todict()
        }
    )
    return response.to_dict(), 200

@app.route("/imgs/<path:filename>")
def serve_file(filename):
    return send_from_directory("imgs", filename)

@app.route("/getStatistics", methods=["GET"])
def get_statistics():
    statistics = {
        "TotalRecycledProducts": 20,
        "GlassRecycled": 4, 
        "MetalRecycled": 5,
        "PlasticRecycled": 5,
        "PaperRecycled": 6,
        "MostPopularProduct": "Plastic Bottle"
    }
    response = Response(
        status=HTTPStatus.OK,
        data=statistics
    )
    return response.to_dict(), 200

@app.route("/getMachines", methods=["GET"])
def get_machines():
    machines = db.query(Machines).all()
    machines_list = [machine.todict() for machine in machines]
    response = Response(
        status=HTTPStatus.OK,
        data={
            "machines": machines_list
        }
    )
    return response.to_dict(), 200

if __name__ == '__main__':
    app.run()