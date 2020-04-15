from . import index
from app.core import login_required
from sanic import response


@index.route('/')
@login_required(user_keyword='user')
async def profile(request, user):
    content = '<a href="/logout">Logout</a><p>Welcome, %s</p>' % user.name
    return response.html(content)
