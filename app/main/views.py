from . import main
from app.core import login_required
from app.auth.views import handle_no_auth
from app.commands.rebuild_sanic_forboto import file_boto_stream
from app.commands.boto_cmd import sync_down
from app.models import Users, Archiv
from sanic import response


URL_FORM = '''
<a href="/main/download">Download</a>
<h2>Enter your urls</h2>

<p>{}</p>

<form action="" method="POST">
  <input class="url in gdrive" id="name" name="gdrive"
    placeholder="gdrive" type="text" value=""><br>
  <input id="submit" name="submit" type="submit" value="Upload">
</form>
'''


content_html = '''

<p>{}</p>

<form action="" method="GET">
  <input id="submit" name="submit" type="submit" value="Download">
</form>
'''


@main.route('/upload_server', methods=['GET', 'POST'])
@login_required(user_keyword='user', handle_no_auth=handle_no_auth)
async def upload_server(request, user):
    '''
    отправляем на загрузку файлы
    TODO переделать на простую загрузку файлов
    '''
    message = ""
    if request.method == 'POST':
        gdrive_url = request.form.get('gdrive')
        sync_down(gdrive_url, user)
        message = "Your file downloading"
    return response.html(URL_FORM.format(message))


@main.route('/download')
@login_required(user_keyword='user', handle_no_auth=handle_no_auth)
async def download_file(request, user):
    """
    Находим по имени пользователя архив и отправляем на загрузку
    """
    login_user = await Users.filter(name=user.name).first()
    files_name = await Archiv.filter(userid=login_user).first()

    return await file_boto_stream(filename=str(files_name))
