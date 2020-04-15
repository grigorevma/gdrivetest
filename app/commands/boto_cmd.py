from asyncio import gather
from aiohttp import ClientSession
from aiofiles import open as aiopen
from os import remove
from app.commands.cmd import get_id
from app.models import Users, Files, Archiv
from app.core import session_boto as sb
from zipfile import ZipFile
from app.config import bucket, AWS_IDKEY, AWS_SKEY
from random import randint
import os
import shutil


def sync_down(gdrive_url, userid):
    # асинхронно выполняет сохранение файлов в aws s3
    gather(download_file_from_google_drive(gdrive_url, userid))


async def download_file_from_google_drive(url, userid):
    # находить по айди файл и передает на сохранение
    query_id = get_id(url)
    URL = "https://docs.google.com/uc?export=download"
    async with ClientSession() as session:
        async with session.get(URL, params={'id': query_id}) as response:
            if response.status == 200:
                await save_response_content(response, userid)
            else:
                print(response.status)


async def save_response_content(response, user):
    # сохраняет файл для следующей передачи в s3 aws
    filename = response.content_disposition.filename
    async with aiopen(filename, 'wb') as fd:
        data = await response.content.read()
        await fd.write(data)
        login_user = await Users.filter(name=user.name).first()
        new_file = Files(name=filename, userid=login_user)
        await new_file.save()
    await save_to_aws(response, user, filename)


async def save_to_aws(response, user, filename):
    # сохраняет файл в aws s3 можно было бы сразу...
    async with aiopen(filename, 'rb') as fd:
        data = await fd.read()
        async with sb.create_client('s3', region_name='eu-central-1',
                                    aws_secret_access_key=AWS_SKEY,
                                    aws_access_key_id=AWS_IDKEY) as client:
            await client.put_object(Bucket=bucket, Key=filename, Body=data)
    remove(filename)
    await create_one_archive(user)


async def create_one_archive(user):
    # create one archive for user files
    randomdir = str(randint(1, 1000))
    # костыль чтобы конкуренцию победить
    # TODO: нужно добавить очереди и отложенную задачу
    uploaddir = 'upload/' + randomdir
    os.mkdir(uploaddir)
    arr_of_file = []
    login_user = await Users.filter(name=user.name).first()
    files_name = await Files.filter(userid=login_user).all()
    filename_arch = str(user.name) + ".zip"
    try:
        for files in files_name:
            arr_of_file.append(files)

        async with sb.create_client('s3', region_name='eu-central-1',
                                    aws_secret_access_key=AWS_SKEY,
                                    aws_access_key_id=AWS_IDKEY) as client:
            for files in arr_of_file:
                output = f"{uploaddir}/{files}"
                resp = await client.get_object(Bucket=bucket, Key=str(files))

                streaming = await resp['Body'].read()

                async with aiopen(output, 'wb') as fd:
                    await fd.write(streaming)

            # create a ZipFile object, and put in AWS S3

            path_zip = f"{uploaddir}/{filename_arch}"
            with ZipFile(path_zip, 'w') as zipObj2:
                for file_name in arr_of_file:
                    output = f"{uploaddir}/{str(file_name)}"
                    zipObj2.write(output)
            async with aiopen(path_zip, 'rb') as fd:
                data = await fd.read()
                await client.put_object(Bucket=bucket,
                                        Key=filename_arch,
                                        Body=data)
            for files in arr_of_file:
                output = f"{uploaddir}/{str(files)}"
                remove(output)
            remove(path_zip)
    finally:
        shutil.rmtree(uploaddir)

    archive = await Archiv.filter(userid=login_user).first()
    if archive is None:
        new_archive = Archiv(name=filename_arch, userid=login_user)
        await new_archive.save()
