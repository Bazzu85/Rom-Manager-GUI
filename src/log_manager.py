# standard and external libraries
import logging
import sys

# project libraries
import src.globals as globals
import src.pathManager as pathManager

def setLogging(log_level):
    # check if logging folder exist and if not create it
    pathManager.create_folder(globals.log_folder)
       
    #logging.getLogger().handlers.clear()
    globals.logger.handlers.clear()

    globals.logger.setLevel(log_level)
    logger_file = logging.FileHandler(globals.log_file)
    logger_file_formatter = logging.Formatter('%(asctime)s - %(levelname)-7s [%(filename)30s:%(lineno)-4s - %(funcName)35s()] %(message)s')
    logger_file.setFormatter(logger_file_formatter)
    globals.logger.addHandler(logger_file)
 
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logger_file_formatter)
    if globals.configuration.redirect_logs_to_console:
        globals.logger.addHandler(console_handler)
    else:
        globals.logger.removeHandler(console_handler)
