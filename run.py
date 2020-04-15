from app import create_app
from tortoise import Tortoise
from app.config import urldb, userpass
import os


app = create_app()


async def db_setup():

    # Here we connect to a SQLite DB file.
    # also specify the app name of "models"
    # which contain models from "app.models"
    await Tortoise.init(
        db_url='postgres://'+userpass+"@"+urldb,
        modules={'models': ['app.models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()


@app.listener('before_server_start')
async def setup_db(app, loop):
    print("init db")
    app.db = await db_setup()


@app.listener('after_server_start')
async def notify_server_started(app, loop):
    print('Server successfully started!')

port = int(os.environ.get("PORT", 5000))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)
