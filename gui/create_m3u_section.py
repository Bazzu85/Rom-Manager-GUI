# standard and external libraries
import inspect
import logging
from nicegui import ui
from pathlib import Path

# project libraries
import src.global_variables as global_variables
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
                                                            }
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
        with ui.row().classes('w-full items-center').bind_visibility_from(globals(), 'show_preview'):
            add_table_to_ui()
            
    
    apply_bindings()

def apply_bindings():
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    global_variables.ui_M3U_source_path_input.bind_value(global_variables.user_data.create_m3u, 'source_path')
    global_variables.ui_M3U_use_centralized_folder_switch.bind_value(global_variables.user_data.create_m3u, 'use_centralized_folder')
    global_variables.ui_M3U_destination_path_input.bind_value(global_variables.user_data.create_m3u, 'destination_path')
    global_variables.ui_M3U_overwrite_switch.bind_value(global_variables.user_data.create_m3u, 'overwrite')

def add_table_to_ui():
    columns = [
                {'name': 'm3u_folder', 'label': 'Folder', 'field': 'm3u_folder', 'required': True, 'align': 'left', 'sortable': True},
                {'name': 'm3u_file', 'label': 'M3U file', 'field': 'm3u_file', 'required': True, 'align': 'left', 'sortable': True},
                {'name': 'm3u_file_list', 'label': 'Disc list', 'field': 'm3u_file_list', 'required': True, 'align': 'left', 'sortable': True, 'wrap-cells': True}
                ]
    rows = []
    global_variables.ui_M3U_preview_table = ui.table(columns=columns, rows=rows).classes('w-full')

def add_rows_to_table():
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)

    for item in m3u_tracing_list:
        item: M3U_tracing
        
        M3U_file_list_cell = ''
        for M3U_file in item.M3U_file_list:
            if M3U_file_list_cell == '':
                M3U_file_list_cell = M3U_file_list_cell + M3U_file
            else:
                M3U_file_list_cell = M3U_file_list_cell + '<br>' + M3U_file
                
        global_variables.ui_M3U_preview_table.rows.append({
            'm3u_folder': Path(item.M3U_path).parent.as_posix(),
            'm3u_file': Path(item.M3U_path).name,
            'm3u_file_list': item.M3U_file_list
        })
    
    # this add_slot are for build a non standard table with multirows cell
    # the add_slot('header') loop over the props to add the column headers
    # the add_slot('body') loop over the props to add the rows
    # if the row is not m3u_file_list, add the value directly
    # if the row is m3u_file_list, loop over the m3u_file_list previously added to the row as a list and create a div for every value 
    global_variables.ui_M3U_preview_table.add_slot('header', r'''
        <q-tr :props="props">
            <q-th v-for="col in props.cols" :key="col.name" :props="props">
                {{ col.label }}
            </q-th>
        </q-tr>
    ''')
    global_variables.ui_M3U_preview_table.add_slot('body', r'''
        <q-tr :props="props">
            <q-td v-for="col in props.cols" :key="col.name" :props="props">
                <template v-if="col.name !== 'm3u_file_list'">
                    {{ col.value }}
                </template>
                <template v-else>
                    <div v-for="file in props.row.m3u_file_list" class="text-left">{{ file }}</div>
                </template>
            </q-td>
        </q-tr>
        ''')
    global_variables.ui_M3U_preview_table.update()
    
def generate_preview():
    global show_preview
    global m3u_tracing_list
    
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)

    show_preview = False
    
    global_variables.ui_M3U_preview_table.rows.clear()
    global_variables.ui_M3U_preview_table.update()

    if global_variables.ui_M3U_source_path_input.error != None:
        message = 'Cannot generate preview. Source path not valid'
        global_variables.logger.info(message)
        ui.notify(message)
        return

    if global_variables.user_data.create_m3u.use_centralized_folder:
        if global_variables.user_data.create_m3u.destination_path == '':
            message = 'Cannot generate preview with "Create the M3U in a unique folder" flag and no Destination file location'
            global_variables.logger.info(message)
            ui.notify(message)
            return
        if global_variables.ui_M3U_destination_path_input.error != None:
            message = 'Cannot generate preview. Destination path not valid'
            global_variables.logger.info(message)
            ui.notify(message)
            return
    
    m3u_tracing_list.clear()
    m3u_tracing_list = M3U_files_worker.generate_preview()
    
    if len(m3u_tracing_list) > 0:
        global_variables.ui_M3U_preview_table.rows.clear()
        global_variables.ui_M3U_preview_table.selected.clear()
        
        add_rows_to_table()
        
        show_preview = True
    
    configuration_manager.write_configuration()
    
