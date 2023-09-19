# standard and external libraries
import inspect
from nicegui import ui

# project libraries
import src.global_variables as global_variables
import gui.move_roms_section as move_roms_section
import gui.create_m3u_section as create_m3u_section

# custom variables
# xxx = ''

def createMainTab():
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    with ui.expansion(text='Move roms').classes('w-full'):
        move_roms_section.create_move_roms_section()
    with ui.expansion(text='Create M3U files for multidisc roms').classes('w-full'):
        create_m3u_section.create_M3U_files_section()
