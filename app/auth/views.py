from app.models import Users
from . import auth
from sanic import response
from app.commands.cmd import get_hash
from os import urandom
from app.core import login_required, logout_user, jinja, login_user
from .forms import LoginForm, RegisterForm
# типичная лайтовая регистрация и авторизация ползователя


def handle_no_auth(request):
    return response.json(dict(message='unauthorized'), status=401)


@auth.route('/login', methods=['GET', 'POST'])
async def login(request):
    form = LoginForm(request)
    some = ""
    if form.validate_on_submit():

        username = form.name.data
        password = form.password.data
        login_ = await Users.filter(name=username).first()
        if login_ is not None:

            new_key = get_hash(password, login_.password[:32])

            if new_key == login_.password[32:]:
                login_user(request, login_)
                return response.redirect('/main/upload_server')
            else:
                some = "Invalid user or password"
        else:
            some = "Invalid user or password"
    return jinja.render('/auth/login.html', request, form=form, some=some)


@auth.route('/register', methods=['GET', 'POST'])
async def register(request):
    message = ''
    form = RegisterForm(request)
    if form.validate_on_submit():
        username = form.name.data
        password = form.password.data

        login_ = await Users.filter(name=username).first()
        if login_ is not None:
            message = "Need other username"
        else:
            salt = urandom(32)
            key = get_hash(password, salt)
            hash_key = salt + key

            new_user = Users(name=username, password=hash_key)
            await new_user.save()

            return response.redirect('/auth/login')

    return jinja.render('/auth/register.html',
                        request,
                        form=form,
                        some=message)


@auth.route('/logout')
@login_required
async def logout(request):
    logout_user(request)
    return response.redirect('/login')
