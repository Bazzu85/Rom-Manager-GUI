# standard and external libraries
import inspect
import logging
from nicegui import ui
from pathlib import Path

# project libraries
import global_variables as global_variables
import src.configuration_manager as configuration_manager
from obj.m3u_tracing import M3U_tracing
import workers.M3U_files_worker as M3U_files_worker

show_preview = False
m3u_tracing_list = []


def create_M3U_files_section():
    global show_preview
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    with ui.card().classes('w-full items-center no-shadow'):
        with ui.row().classes('w-full items-center'):
            global_variables.ui_M3U_source_path_input = ui.input(label='Rom file location', 
                                                        validation={
                                                            'Insert something': lambda value: value != '' , 
                                                            'Path not valid': lambda value: Path(value).is_dir()
                                                            }, 
                                                        value=global_variables.configuration.last_used_rom_path
                                                        ).classes('w-full')
        with ui.row().classes('w-full items-center'):
            global_variables.ui_M3U_use_centralized_folder_switch = ui.switch("Create the M3U in a unique folder")
            global_variables.ui_M3U_destination_path_input = ui.input(label='Destination file location', 
                                                             validation={
                                                                 'Path not valid': lambda value: Path(value).is_dir()
                                                                 }, 
                                                             ).classes('w-full').bind_visibility_from(global_variables.ui_M3U_use_centralized_folder_switch, 'value')
        with ui.row().classes('w-full items-center'):
            global_variables.ui_M3U_overwrite_switch = ui.switch("Overwrite existing M3U files")
        with ui.row().classes('w-full items-center'):
            ui.button('Preview', on_click=generate_preview)
        with ui.row().classes('w-full items-center'):
            ui.switch('show preview').bind_enabled(locals(), 'show_preview')
            columns = [
                {'name': 'm3u_folder', 'label': 'Folder', 'field': 'm3u_folder', 'required': True, 'align': 'left', 'sortable': True},
                {'name': 'm3u_file', 'label': 'M3U file', 'field': 'm3u_file', 'required': True, 'align': 'left', 'sortable': True},
                {'name': 'm3u_file_list', 'label': 'Disc list', 'field': 'm3u_file_list', 'required': True, 'align': 'left', 'sortable': True}
                ]
            rows = []
            global_variables.ui_M3U_preview_table = ui.table(columns=columns, rows=rows).bind_visibility_from(show_preview).classes('w-full')

    
def generate_preview():
    global show_preview
    global m3u_tracing_list
    
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    
    if global_variables.ui_M3U_use_centralized_folder_switch.value and global_variables.ui_M3U_destination_path_input.value == '':
        message = 'Cannot generate preview with "Create the M3U in a unique folder" flag and no Destination file location'
        global_variables.logger.info(message)
        ui.notify(message)
        return
    
    global_variables.configuration.last_used_rom_path = Path(global_variables.ui_M3U_source_path_input.value).as_posix()
    m3u_tracing_list.clear()
    m3u_tracing_list = M3U_files_worker.generate_preview()
    
    if len(m3u_tracing_list) > 0:
        global_variables.ui_M3U_preview_table.rows.clear()
        global_variables.ui_M3U_preview_table.selected.clear()
        
        for item in m3u_tracing_list:
            global_variables.ui_M3U_preview_table.rows.append({
                'm3u_folder': Path(item.M3U_path).parent.as_posix(),
                'm3u_file': Path(item.M3U_path).name,
                'm3u_file_list': str(item.M3U_file_list)
            })
        global_variables.ui_M3U_preview_table.update()
        show_preview = True
    
    configuration_manager.write_configuration()
    
