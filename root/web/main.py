import json
import os

from aiohttp import web
import csv
import io
import aiohttp_jinja2
import jinja2
from sqlalchemy.exc import IntegrityError

from dotenv import load_dotenv, find_dotenv

from root.logger.config import logger
from root.tg.main import send_message_to_users_manually

logger = logger
load_dotenv(find_dotenv())

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join('root', 'web', 'templates')),
    trim_blocks=True,
    lstrip_blocks=True,
    keep_trailing_newline=True
)


@aiohttp_jinja2.template('send_message_manually_form.html')
async def send_message_manually_form(request):
    return {}


async def send_message_manually(request):
    password = None
    csv_file = None
    message_text = None
    numeric_values = []
    try:
        data = await request.post()
        message_text = data['message_text']
        csv_file = data['csv_file'].file
        password = data['pass']
    except Exception as x:
        logger.exception(x)
    
    if password == os.getenv('WEB_PASSWORD'):
        
        with csv_file:
            csv_file_content = csv_file.read()
        
        try:
            # Read the file as CSV and extract numeric values from the first column
            reader_list_of_lists = csv.reader(csv_file_content.decode('utf-8').splitlines())
            list_of_values = [row[0] for row in reader_list_of_lists]
            numeric_values = [int(value) for value in list_of_values if value and value.isnumeric()]
            
            await send_message_to_users_manually(numeric_values, message_text)
        except Exception as x:
            logger.exception(x)
            raise web.HTTPFound('/fail')
        
        raise web.HTTPFound('/success')
    
    else:
        logger.info('Someone tried to access admin panel without paassword')
        raise web.HTTPFound('/wrong_password')


@logger.catch
@aiohttp_jinja2.template('success.html')
async def success(request):
    return {}


@logger.catch
@aiohttp_jinja2.template('fail.html')
async def fail(request):
    return {}


@logger.catch
@aiohttp_jinja2.template('start_menu.html')
async def start_menu(request):
    return {}


@logger.catch
@aiohttp_jinja2.template('wrong_password.html')
async def wrong_password(request):
    return {}


app = web.Application()

app.add_routes([web.get('/', start_menu),
                web.get('/success', success),
                web.get('/fail', fail),
                web.get('/wrong_password', wrong_password),
                web.get('/send_message_manually_form', send_message_manually_form),
                ])

app.add_routes([web.post('/send_message_manually', send_message_manually)])

# app.add_routes([web.get('/success', success)])
# app.add_routes([web.get('/fail', fail)])

# app.router.add_get('/send_message_manually_form', send_message_manually_form)
# app.router.add_post('/send_message_manually', send_message_manually)

aiohttp_jinja2.setup(app, loader=env.loader, context_processors=[aiohttp_jinja2.request_processor])

if __name__ == '__main__':
    # web.run_app(app, host='0.0.0.0')
    web.run_app(app, host='127.0.0.1', port=80)
