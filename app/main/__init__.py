from sanic import Blueprint


main = Blueprint('main', url_prefix='/main')

from . import views
