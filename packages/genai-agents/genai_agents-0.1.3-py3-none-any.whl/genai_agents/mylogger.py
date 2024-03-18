import logging
import inspect
import threading
from datetime import datetime

import os
import traceback
import time


# Configure basic logging settings
def configure_logging(filename="agents_app.log", level=logging.DEBUG):
    logging.basicConfig(
        filename=f"log/{filename}_{datetime.now():%Y-%m-%d_%H-%M-%S}.log",
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filemode="w",
    )
    print(f'logfile:: {filename}')

def getTracebackWithReturn():
    #if int(os.environ['G_TRACEBACK_FLAG']) == 1 :
    #traceback.print_stack()
    retString=[]
    for line in traceback.format_stack():
        retString.append(line.strip()) 
    print(retString)     
    return retString



# Simplified logger function
def log(message, level=logging.INFO):
    """Logs a message with the specified level."""
    frame = inspect.currentframe().f_back
    thread_id = threading.get_ident()
    logger = logging.getLogger()
    msg = f'Thread ID: {thread_id} - {frame.f_globals["__name__"]}:{frame.f_lineno} - {message}'
    if level == logging.DEBUG:
        logger.debug(msg)
    elif level == logging.INFO:
        logger.info(msg)
    elif level == logging.WARNING:
        logger.warning(msg)
    elif level == logging.ERROR:
        logger.error(msg)
    elif level == logging.CRITICAL:
        logger.critical(msg)
    else:
        logger.log(level, msg)


# # Example usage
# if __name__ == "__main__":
#     configure_logging("my_app", logging.DEBUG)
#     log("This is a debug message.", logging.DEBUG)
#     log("This is an info message.")
#     log("This is a warning message.", logging.WARNING)
#     log("This is an error message.", logging.ERROR)
#     log("This is a critical message.", logging.CRITICAL)
