# standard and external libraries
import inspect
import logging
import os

# project libraries
import src.globals as globals

def create_folder(path):
    globals.logger.debug(inspect.currentframe().f_code.co_name)
    globals.logger.debug(" path: " + path)

    if os.path.exists(path) and os.path.isdir(path):
        pass
    else:
        os.mkdir(path)
        
def addLastSlashIfMissing(path):
    globals.logger.debug(inspect.currentframe().f_code.co_name)
    globals.logger.debug(" path: " + path)
    if not path.endswith("\\"):
            path += '\\'
    return path
    
def deleteEmptyFolders(path):
    globals.logger.debug(inspect.currentframe().f_code.co_name)
    globals.logger.debug(" path: " + path)
    for root, folders, files in os.walk(path, topdown=False):
        for folder in folders:
            remove_empty_dir(os.path.realpath(os.path.join(root, folder)))
        
def remove_empty_dir(path):
    try:
        os.rmdir(path)
    except OSError:
        pass