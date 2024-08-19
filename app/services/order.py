from app.common.http_methods import GET, POST
from flask import Blueprint

from ..controllers import OrderController
from ..services.services import (create, get_all, get_by_id)

order = Blueprint('order', __name__)


@order.route('/', methods=POST)
def create_order():
    return create(OrderController)

@order.route('/id/<_id>', methods=GET)
def get_order_by_id(_id: int):
    return get_by_id(_id, OrderController)


@order.route('/', methods=GET)
def get_orders():
    return get_all(OrderController)