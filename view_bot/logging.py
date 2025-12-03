import logging
import logging.config


class BotNameFilter(logging.Filter):

    def filter(self, record):
        if not hasattr(record, "botName"):
            record.botName = "SYSTEM"
        return True


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] [%(levelname)s] | %(name)s.%(funcName)s:%(lineno)d | [%(botName)s] %(message)s",
        },
    },
    "filters": {
        "bot_filter": {
            "()": "view_bot.logging.BotNameFilter",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "DEBUG",
            "filters": ["bot_filter"],
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
}


def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
