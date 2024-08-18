from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, jsonify, request

from ..controllers import IngredientController
from ..services.services import (create, update, get_all, get_by_id)

ingredient = Blueprint('ingredient', __name__)


@ingredient.route('/', methods=POST)
def create_ingredient():
    return create(IngredientController)


@ingredient.route('/', methods=PUT)
def update_ingredient():
    return update(IngredientController)


@ingredient.route('/id/<_id>', methods=GET)
def get_ingredient_by_id(_id: int):
    return get_by_id(_id, IngredientController)


@ingredient.route('/', methods=GET)
def get_ingredients():
    return get_all(IngredientController)
