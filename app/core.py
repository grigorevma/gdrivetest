from sanic_auth import Auth
import aiobotocore
from sanic_jinja2 import SanicJinja2

# This Auth object is shared by all blueprints
authentication = Auth()
login_required = authentication.login_required
logout_user = authentication.logout_user
login_user = authentication.login_user

jinja = SanicJinja2()

session_boto = aiobotocore.get_session()
