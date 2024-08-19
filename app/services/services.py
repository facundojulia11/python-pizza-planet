from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, jsonify, request


def create(entity_controller):
    entity, error = entity_controller.create(request.json)
    response = entity if not error else {'error': error}
    status_code = 200 if not error else 400
    return jsonify(response), status_code


def update(entity_controller):
    entity, error = entity_controller.update(request.json)
    response = entity if not error else {'error': error}
    status_code = 200 if not error else 400
    return jsonify(response), status_code


def get_by_id(_id: int, entity_controller):
    entity, error = entity_controller.get_by_id(_id)
    response = entity if not error else {'error': error}
    status_code = 200 if entity else 404 if not error else 400
    return jsonify(response), status_code


def get_all(entity_controller):
    entities, error = entity_controller.get_all()
    response = entities if not error else {'error': error}
    status_code = 200 if entities else 404 if not error else 400
    return jsonify(response), status_code
