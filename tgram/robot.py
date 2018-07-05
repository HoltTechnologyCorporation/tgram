from argparse import ArgumentParser
import json

from telegram import ParseMode, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler

from tgram.config import load_config


class TgramRobot(object):

    def __init__(self, config_file='var/config.json'):
        self.config = load_config(config_file)
        self.opts = {
            'mode': None,
        }

    # PUBLIC API

    def parse_cli_opts(self):
        parser = ArgumentParser()
        parser.add_argument('-m', '--mode')
        opts = parser.parse_args()
        self.opts = {
            'mode': opts.mode,
        }
        self._check_opts_integrity()
        
    def set_opts(self, opts):
        self.opts = {}
        self.opts.update(opts)
        self._check_opts_integrity()

    def get_token(self):
        return self.config['api_token_%s' % self.opts['mode']]

    def run_polling(self):
        updater = self._init_updater(self.get_token())
        self.register_handlers(updater.dispatcher)
        self.before_start_processing()
        updater.bot.delete_webhook()
        updater.start_polling()

    def before_start_processing():
        pass

    # PRIVATE METHODS

    def _check_opts_integrity(self):
        assert self.opts['mode'] in ('production', 'test')

    def _init_updater(self, token):
        updater = Updater(token=token, workers=16)
        self.bot = updater.bot
        return updater

    def _init_bot(self, token):
        bot = Bot(token=token)
        self.bot = bot
        return bot
