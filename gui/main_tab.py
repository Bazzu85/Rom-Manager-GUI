# standard and external libraries
import inspect
from nicegui import ui
from pathlib import Path

# project libraries
import global_variables as global_variables
import gui.m3u_files_section as m3u_files_section

# custom variables
# xxx = ''

def createMainTab():
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    with ui.expansion(text='Move roms to subfolders based on rom name').classes('w-full'):
        pass
    with ui.expansion(text='Move roms to folder').classes('w-full'):
        pass
    with ui.expansion(text='Create M3U files for multidisc roms').classes('w-full'):
        m3u_files_section.create_M3U_files_section()
