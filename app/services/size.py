from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, jsonify, request

from ..services.services import (create, update, get_all, get_by_id)
from ..controllers import SizeController

size = Blueprint('size', __name__)


@size.route('/', methods=POST)
def create_size():
    return create(SizeController)


@size.route('/', methods=PUT)
def update_size():
    return update(SizeController)


@size.route('/id/<_id>', methods=GET)
def get_size_by_id(_id: int):
    return get_by_id(_id, SizeController)


@size.route('/', methods=GET)
def get_sizes():
    return get_all(SizeController)
