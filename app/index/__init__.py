from sanic import Blueprint

index = Blueprint('index', url_prefix='/')

from . import views
