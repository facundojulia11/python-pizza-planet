import pytest

from app.test.utils.functions import get_random_string, get_random_price


def test_create_order(create_order):
    order = create_order.json
    print("ORDER: ", order)
    print("STARTTS: ",create_order.status)
    pytest.assume(create_order.status.startswith('200'))
    pytest.assume("client_name" in order)
    pytest.assume("detail" in order)
    pytest.assume(order['_id'])
    pytest.assume(order['size'])
    pytest.assume(order['client_name'])
    pytest.assume(order['date'])
    pytest.assume(order['client_dni'])
    pytest.assume(order['client_phone'])

def test_get_orders_service(client, create_orders, order_uri):
    response = client.get(order_uri)
    pytest.assume(response.status.startswith('200'))

    returned_orders = {order["_id"]: order for order in response.json}

    for order_response in create_orders:
        order_data = order_response.json
        pytest.assume(order_data['_id'] in returned_orders)
