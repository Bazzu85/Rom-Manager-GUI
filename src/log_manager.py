# standard and external libraries
import logging
import sys
from pathlib import *

# project libraries
import global_variables as global_variables
import src.pathManager as pathManager

def setLogging(log_level):
    # create log file directory if missing
    Path(global_variables.configuration.log_file).parent.mkdir(exist_ok=True)
       
    #logging.getLogger().handlers.clear()
    global_variables.logger.handlers.clear()

    global_variables.logger.setLevel(log_level)
    logger_file = logging.FileHandler(global_variables.configuration.log_file)
    logger_file_formatter = logging.Formatter('%(asctime)s - %(levelname)-7s [%(filename)30s:%(lineno)-4s - %(funcName)35s()] %(message)s')
    logger_file.setFormatter(logger_file_formatter)
    global_variables.logger.addHandler(logger_file)
 
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logger_file_formatter)
    if global_variables.configuration.redirect_logs_to_console:
        global_variables.logger.addHandler(console_handler)
    else:
        global_variables.logger.removeHandler(console_handler)
