from flask import Blueprint

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

from . import status_routes
from . import prediksi_routes
