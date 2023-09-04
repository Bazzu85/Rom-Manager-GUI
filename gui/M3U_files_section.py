# standard and external libraries
import inspect
import logging
from nicegui import ui
from pathlib import Path

# project libraries
import src.globals as globals
from obj.Move_tracing import Move_tracing
import workers.M3U_files_worker as M3U_files_worker

show_preview = False
move_tracing_list = [Move_tracing()]


def create_M3U_files_section():
    globals.logger.debug(inspect.currentframe().f_code.co_name)
    with ui.card().classes('w-full items-center no-shadow'):
        with ui.row().classes('w-full items-center'):
            globals.ui_M3U_source_path_input = ui.input(label='Rom file location', 
                                                        validation={
                                                            'Insert something': lambda value: value != '' , 
                                                            'Path not valid': lambda value: Path(value).is_dir()
                                                            }, 
                                                        value=globals.configuration.last_used_rom_path
                                                        ).classes('w-full')
        with ui.row().classes('w-full items-center'):
            globals.ui_M3U_use_centralized_folder_switch = ui.switch("Create the M3U in a unique folder")
            globals.ui_M3U_destination_path_input = ui.input(label='Destination file location', 
                                                             validation={
                                                                 'Path not valid': lambda value: Path(value).is_dir()
                                                                 }, 
                                                             ).classes('w-full').bind_visibility_from(globals.ui_M3U_use_centralized_folder_switch, 'value')
        with ui.row().classes('w-full items-center'):
            globals.ui_M3U_overwrite_switch = ui.switch("Overwrite existing M3U files")
        with ui.row().classes('w-full items-center'):
            ui.button('Preview', on_click=generate_preview)

def generate_preview():
    global show_preview
    global move_tracing_list
    
    globals.logger.debug(inspect.currentframe().f_code.co_name)
    
    if globals.ui_M3U_use_centralized_folder_switch and globals.ui_M3U_destination_path_input.value == '':
        message = 'Cannot generate preview with "Create the M3U in a unique folder" flag and no Destination file location'
        globals.logger.info(message)
        ui.notify(message)
        return
    
    move_tracing_list.clear()
    move_tracing_list = M3U_files_worker.generate_preview()
        
    
