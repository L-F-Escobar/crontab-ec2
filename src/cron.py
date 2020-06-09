from src.log import get_logger
from datetime import datetime

log = get_logger(
    "cron.py",
    "'[%(levelname)s] [%(name)s] [%(asctime)s] [%(funcName)s::%(lineno)d] [%(message)s]'",
)

def handle(event=None, context=None):
    log.info(f"Engine is running. Event --> {event}.")

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

    return "success"