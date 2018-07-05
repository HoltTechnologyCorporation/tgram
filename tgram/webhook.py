import logging
from queue import Queue
import uuid
import json
from threading import Thread

from bottle import request, abort, Bottle
from telegram import Update
from telegram.ext import Dispatcher

DEFAULT_WORKERS = 2


def build_wsgi_app(robot, workers=DEFAULT_WORKERS):
    app = Bottle()
    logging.basicConfig(level=logging.DEBUG)
    bot = robot._init_bot(token=robot.get_token())
    update_queue = Queue()
    dispatcher = Dispatcher(bot, update_queue, workers=workers)
    robot.register_handlers(dispatcher)
    robot.before_start_processing()

    thread = Thread(target=dispatcher.start, name='dispatcher')
    thread.start()

    secret_key = str(uuid.uuid4())

    @app.route('/%s/' % secret_key, method='POST')
    def page():
        if request.headers.get('content-type') == 'application/json':
            json_string = request.body.read().decode('utf-8')
            update = Update.de_json(json.loads(json_string), bot)
            dispatcher.process_update(update)
            return ''
        else:
            abort(403)

    logging.debug(robot.config)
    url = robot.config['webhook_url_%s' % robot.opts['mode']] % {
        'secret_key': secret_key,
    }
    logging.debug('Webhook has been set to %s' % url)
    bot.set_webhook(url=url)
    return app
