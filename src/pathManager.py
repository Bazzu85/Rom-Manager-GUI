# standard and external libraries
import inspect
import logging
import os

# project libraries
import global_variables as global_variables

def addLastSlashIfMissing(path):
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    global_variables.logger.debug(' path: ' + path)
    if not path.endswith('\\'):
            path += '\\'
    return path
    
def deleteEmptyFolders(path):
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    global_variables.logger.debug(' path: ' + path)
    for root, folders, files in os.walk(path, topdown=False):
        for folder in folders:
            remove_empty_dir(os.path.realpath(os.path.join(root, folder)))
        
def remove_empty_dir(path):
    try:
        os.rmdir(path)
    except OSError:
        pass