# standard and external libraries
import logging
import sys
from pathlib import *

# project libraries
import src.globals as globals
import src.pathManager as pathManager

def setLogging(log_level):
    # create log file directory if missing
    Path(globals.configuration.log_file).parent.mkdir(exist_ok=True)
       
    #logging.getLogger().handlers.clear()
    globals.logger.handlers.clear()

    globals.logger.setLevel(log_level)
    logger_file = logging.FileHandler(globals.configuration.log_file)
    logger_file_formatter = logging.Formatter('%(asctime)s - %(levelname)-7s [%(filename)30s:%(lineno)-4s - %(funcName)35s()] %(message)s')
    logger_file.setFormatter(logger_file_formatter)
    globals.logger.addHandler(logger_file)
 
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logger_file_formatter)
    if globals.configuration.redirect_logs_to_console:
        globals.logger.addHandler(console_handler)
    else:
        globals.logger.removeHandler(console_handler)
