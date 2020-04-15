from sanic import Sanic
import sanic_cookiesession
from app.main import main
from app.auth import auth
from app.index import index
from app.core import authentication, jinja
from app.config import session_csy, session_key


def create_app():
    app = Sanic(__name__)
    jinja.init_app(app)
    app.config['SESSION_COOKIE_SECRET_KEY'] = session_csy
    app.config['SESSION_COOKIE_SECURE'] = False
    app.config['SECRET_KEY'] = session_key
    sanic_cookiesession.setup(app)
    authentication.setup(app)
    app.blueprint(auth)
    app.blueprint(main)
    app.blueprint(index)
    app.config.AUTH_LOGIN_ENDPOINT = '/auth/register'
    return app
