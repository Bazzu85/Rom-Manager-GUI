# standard and external libraries
import inspect
from nicegui import ui
from pathlib import Path

# project libraries
import src.globals as globals
import gui.M3U_files_section as M3U_files_section

# custom variables
# xxx = ''

def createMainTab():
    globals.logger.debug(inspect.currentframe().f_code.co_name)
    with ui.expansion(text='Move roms to subfolders based on rom name').classes('w-full'):
        pass
    with ui.expansion(text='Move roms to folder').classes('w-full'):
        pass
    with ui.expansion(text='Create M3U files for multidisc roms').classes('w-full'):
        M3U_files_section.create_M3U_files_section()
