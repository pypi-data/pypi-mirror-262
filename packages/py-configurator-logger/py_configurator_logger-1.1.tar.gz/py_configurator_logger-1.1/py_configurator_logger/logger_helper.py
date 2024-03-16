import os
import logging
import json
from enum import Enum
from .custom_logger import CustomLogger


class LogOutputFormat(Enum):
    PLAIN_TEXT = 'plain_text'
    JSON = 'json'


LOG_FORMATTER_PROVIDERS = {
    LogOutputFormat.PLAIN_TEXT.value:
        lambda plain_format: CustomLogFormatter(plain_format),
    LogOutputFormat.JSON.value:
        lambda json_format: JsonLogFormatter(json_format)
}

RESERVED_FORMAT_KEYS = ['name', 'msg', 'args', 'levelname', 'levelno',
                        'pathname', 'filename', 'module', 'exc_info',
                        'exc_text', 'stack_info', 'lineno', 'funcName',
                        'created', 'msecs', 'relativeCreated',
                        'thread', 'threadName', 'processName', 'process']

DEFAULT_PLAIN_TEXT_FORMAT = \
    '%(asctime)s %(levelname)s %(name)s:%(lineno)d %(message)s'

DEFAULT_JSON_FORMAT = {
    "timestamp": "%(asctime)s", "level": "%(levelname)s",
    "filename": "%(name)s", "lineno": "%(lineno)d",
    "message": "%(message)s"
}
DEFAULT_LOG_LEVEL = "DEBUG"
DEFAULT_LOG_OUTPUT_FORMAT = "plain_text"

TRACE = 5


class CustomLogFormatter(logging.Formatter):
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'
    green = '\x1b[38;5;2m'
    cyan = '\u001b[36m'

    def __init__(self, log_format):
        """
        Initializes a plain text formatter.

        :param log_format: Plain text format of the logger.
        """
        super().__init__()
        self.log_format = log_format
        self.FORMATS = {
            logging.DEBUG: self.blue + self.log_format + self.reset,
            logging.INFO: self.green + self.log_format + self.reset,
            logging.WARNING: self.yellow + self.log_format + self.reset,
            logging.ERROR: self.red + self.log_format + self.reset,
            logging.CRITICAL: self.bold_red + self.log_format + self.reset,
            TRACE: self.cyan + self.log_format + self.reset
        }

    def format(self, record):
        additional_info = ', '.join(
            f'{value}' for key, value in record.__dict__.items()
            if key not in RESERVED_FORMAT_KEYS
        )
        if additional_info:
            record.msg += f': {additional_info}'
        log_fmt = self.FORMATS.get(record.levelno)

        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class JsonLogFormatter(logging.Formatter):

    def __init__(self, log_format):
        """
        Initializes a json formatter.

        :param log_format: Json format of the logger.
        """
        super().__init__()
        self.log_format = log_format

    def format(self, record):
        extra = {key: value for key, value in record.__dict__.items()
                 if key not in RESERVED_FORMAT_KEYS}
        full_dict = {**self.log_format, **extra}
        formatter = logging.Formatter(json.dumps(full_dict))
        return formatter.format(record)


class ConfiguratorLogger:

    def __init__(self, logger_name):
        """
        Initializes a context-aware logger.

        :param logger_name: Name of the logger.
        """
        app_config = self.get_app_config()

        # Set custom logger class which includes "TRACE" as a new log_level
        logging.setLoggerClass(CustomLogger)
        self.logger = logging.getLogger(logger_name)
        log_level_str = app_config.get("logs_level", DEFAULT_LOG_LEVEL).upper()
        log_level = getattr(logging, log_level_str, logging.INFO)
        self.logger.setLevel(log_level)

        log_text_format = app_config.get("log_format", DEFAULT_PLAIN_TEXT_FORMAT)
        log_json_format = app_config.get("log_json_format", DEFAULT_JSON_FORMAT)
        console_handler = logging.StreamHandler()
        try:
            formatter_type = app_config.get("logs_output_format",
                                            DEFAULT_LOG_OUTPUT_FORMAT).lower()
        except Exception:
            formatter_type = LogOutputFormat.PLAIN_TEXT.value

        formatter = LOG_FORMATTER_PROVIDERS.get(
            formatter_type
        )(log_text_format if formatter_type == LogOutputFormat.PLAIN_TEXT.value
          else log_json_format)

        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        """
        Returns the instantiated logger.

        :return: Logger instance.
        """
        return self.logger

    def get_app_config(self):
        # Read configuration from environment variables
        config = {}

        # Look for all .env files in the directory
        env_files = [filename for filename in os.listdir() if
                     filename.endswith('.env')]

        # Load variables related to logs from all .env files found
        for env_file in env_files:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('log') and '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip('""')
        return config
