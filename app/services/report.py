from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, jsonify, request
from ..services.services import get_all
from ..controllers import ReportController

report = Blueprint('report', __name__)

@report.route('/', methods=GET)
def get_report():
    return get_all(ReportController)
