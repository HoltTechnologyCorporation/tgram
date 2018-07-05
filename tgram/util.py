import logging


def run_polling(bot_class, logging_level=logging.DEBUG):
    logging.basicConfig(level=logging_level)
    robot = bot_class()
    robot.parse_cli_opts()
    robot.run_polling()
