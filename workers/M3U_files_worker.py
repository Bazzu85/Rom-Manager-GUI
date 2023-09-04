# standard and external libraries
import inspect
from nicegui import ui
from pathlib import Path

# project libraries
import src.globals as globals
from obj.Move_tracing import Move_tracing

def generate_preview():
    globals.logger.debug(inspect.currentframe().f_code.co_name)
    
    move_tracing_list = [Move_tracing()]
    move_tracing_list.clear()
    
    path = globals.ui_M3U_source_path_input.value
    globals.logger.debug('Working on ' + path + ' path')
    for item in Path(path).rglob('*'):
        globals.logger.debug(' Found item ' + str(item))
        if item.is_dir():
            globals.logger.debug(' Item is a directory. Jumping to next')
            continue
        if not item.is_file():
            globals.logger.debug(' Item is not a directory and file???. Jumping to next')
            continue
        
        
