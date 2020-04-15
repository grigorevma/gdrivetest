from sanic import Blueprint

auth = Blueprint('auth', url_prefix='/auth')

from . import views
