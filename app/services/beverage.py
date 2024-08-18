from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, jsonify, request

from ..controllers import BeverageController
from ..services.services import (create, update, get_all, get_by_id)

beverage = Blueprint('beverage', __name__)


@beverage.route('/', methods=POST)
def create_beverage():
    return create(BeverageController)


@beverage.route('/', methods=PUT)
def update_beverage():
    return update(BeverageController)


@beverage.route('/id/<_id>', methods=GET)
def get_beverage_by_id(_id: int):
    return get_by_id(_id, BeverageController)


@beverage.route('/', methods=GET)
def get_beverages():
    return get_all(BeverageController)
