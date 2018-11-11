import logging
from logging.handlers import TimedRotatingFileHandler
from config import log_level

log_levels = {
    'CRITICAL' : logging.critical,
    'ERROR' : logging.ERROR,
    'WARNING' : logging.WARNING,
    'INFO' : logging.INFO,
    'DEBUG' : logging.DEBUG
}

# Log to file, rotate everyday, delete old ones
handler = TimedRotatingFileHandler('bot_oak.log', when='midnight', backupCount=5)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
if log_level not in log_levels:
    log_level = "DEBUG"
logger.setLevel(log_levels[log_level])
