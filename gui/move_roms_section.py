# standard and external libraries
import asyncio
import inspect
from nicegui import ui
from pathlib import Path

# project libraries
import src.global_variables as global_variables
import src.configuration_manager as configuration_manager
from obj.move_tracing import Move_Tracing
import workers.move_roms_worker as move_roms_worker

show_move_roms_to_folder_elements = False
show_move_roms_to_subfolder_elements = False
show_preview = False
enable_ui_elements = True

def create_move_roms_section():
    global show_move_roms_to_subfolder_elements
    global show_move_roms_to_folder_elements
    global show_preview
    global enable_ui_elements
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    with ui.card().classes('w-full items-center no-shadow'):
        with ui.row().classes('w-full items-center'):
            global_variables.ui_move_roms_choice_radio = ui.radio({global_variables.MOVE_ROMS_TO_SUBFOLDER: 'Move roms to subfolders based on rom name', global_variables.MOVE_ROMS_TO_FOLDER: 'Move roms to folder'}, on_change=check_move_roms_choice).props('inline')
        with ui.row().classes('w-full items-center'):
            global_variables.ui_move_roms_source_path_input = ui.input(label='Rom file location', 
                                                        validation={
                                                            'Insert something': lambda value: value != '' , 
                                                            'Path not valid': lambda value: Path(value).is_dir()
                                                            }
                                                        ).classes('w-full')
        with ui.row().classes('w-full items-center').bind_visibility(globals(), 'show_move_roms_to_subfolder_elements'):
            global_variables.ui_move_roms_use_same_folder_for_multidisc_switch = ui.switch("Use the same folder for multidisc roms?")
        with ui.row().classes('w-full items-center').bind_visibility(globals(), 'show_move_roms_to_folder_elements'):
            global_variables.ui_move_roms_use_different_folder_switch = ui.switch("Use as destination folder a custom folder?")
            global_variables.ui_move_roms_destination_path_input = ui.input(label='Destination file location', 
                                                             validation={
                                                                 'Path not valid': lambda value: Path(value).is_dir()
                                                                 }, 
                                                             ).classes('w-full')
        with ui.row().classes('w-full items-center'):
            global_variables.ui_move_roms_preview_button = ui.button('Preview', on_click=generate_preview)
            global_variables.ui_move_roms_run_button = ui.button('Run!', on_click=run)
        with ui.row().classes('w-full items-center').bind_visibility_from(globals(), 'show_preview'):
            add_table_to_ui()
            
    
    apply_bindings()

def apply_bindings():
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    global_variables.ui_move_roms_choice_radio.bind_value(global_variables.user_data.move_roms, 'choice')
    global_variables.ui_move_roms_choice_radio.bind_enabled_from(globals(), 'enable_ui_elements')

    global_variables.ui_move_roms_source_path_input.bind_value(global_variables.user_data.move_roms, 'source_path')
    global_variables.ui_move_roms_source_path_input.bind_enabled_from(globals(), 'enable_ui_elements')

    global_variables.ui_move_roms_use_same_folder_for_multidisc_switch.bind_value(global_variables.user_data.move_roms, 'use_same_folder_for_multidisc')
    global_variables.ui_move_roms_use_same_folder_for_multidisc_switch.bind_enabled_from(globals(), 'enable_ui_elements')

    global_variables.ui_move_roms_use_different_folder_switch.bind_value(global_variables.user_data.move_roms, 'use_different_folder')
    global_variables.ui_move_roms_use_different_folder_switch.bind_enabled_from(globals(), 'enable_ui_elements')

    global_variables.ui_move_roms_destination_path_input.bind_value(global_variables.user_data.move_roms, 'destination_path')
    global_variables.ui_move_roms_destination_path_input.bind_enabled_from(globals(), 'enable_ui_elements')
    global_variables.ui_move_roms_destination_path_input.bind_visibility_from(global_variables.ui_move_roms_use_different_folder_switch, 'value')

    global_variables.ui_move_roms_preview_button.bind_enabled_from(globals(), 'enable_ui_elements')

    global_variables.ui_move_roms_run_button.bind_enabled_from(globals(), 'enable_ui_elements')
    global_variables.ui_move_roms_run_button.bind_visibility_from(globals(), 'show_preview')

def check_move_roms_choice():
    global show_move_roms_to_subfolder_elements
    global show_move_roms_to_folder_elements
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    if global_variables.ui_move_roms_choice_radio.value == global_variables.MOVE_ROMS_TO_FOLDER:
        show_move_roms_to_subfolder_elements = False
        show_move_roms_to_folder_elements = True
    elif global_variables.ui_move_roms_choice_radio.value == global_variables.MOVE_ROMS_TO_SUBFOLDER:
        show_move_roms_to_subfolder_elements = True
        show_move_roms_to_folder_elements = False

    
def add_table_to_ui():
    columns = [
                {'name': 'source', 'label': 'Source', 'field': 'source', 'required': True, 'align': 'left', 'sortable': True},
                {'name': 'destination', 'label': 'Destination', 'field': 'destination', 'required': True, 'align': 'left', 'sortable': True},
                ]
    rows = []
    global_variables.ui_move_roms_preview_table = ui.table(columns=columns, rows=rows).classes('w-full')

def add_rows_to_table():
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)

    for item in global_variables.move_roms_tracing_list:
        item: Move_Tracing
        
        global_variables.ui_move_roms_preview_table.rows.append({
            'source': item.source,
            'destination': item.destination,
        })
    
    global_variables.ui_move_roms_preview_table.update()
    
async def generate_preview():
    global show_preview
    global enable_ui_elements
    
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)

    show_preview = False
    
    global_variables.ui_move_roms_preview_table.rows.clear()
    global_variables.ui_move_roms_preview_table.update()

    # do the checks. if False (ko) exit
    if not check_for_preview():
        return False
    
    global_variables.move_roms_tracing_list.clear()

    enable_ui_elements = False
    
    # add the spinner to apply the ui enable change from enable_ui_elements and show the loading animation
    spinner = ui.spinner('dots', size='xl')
    await asyncio.to_thread(move_roms_worker.generate_preview)

    if len(global_variables.move_roms_tracing_list) > 0:
        global_variables.ui_move_roms_preview_table.rows.clear()
        global_variables.ui_move_roms_preview_table.selected.clear()
        
        add_rows_to_table()
        
        show_preview = True
          
    enable_ui_elements = True
    
    spinner.delete()

def check_for_preview():
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)

    if global_variables.ui_move_roms_source_path_input.error != None:
        message = 'Cannot generate preview. Source path not valid'
        global_variables.logger.info(message)
        ui.notify(message)
        return False

    if global_variables.user_data.move_roms.use_different_folder:
        if global_variables.user_data.move_roms.destination_path == '':
            message = 'Cannot generate preview with "Use different folder" flag and no Destination file location'
            global_variables.logger.info(message)
            ui.notify(message)
            return False
        if global_variables.ui_move_roms_destination_path_input.error != None:
            message = 'Cannot generate preview. Destination path not valid'
            global_variables.logger.info(message)
            ui.notify(message)
            return False
    
    return True
    
async def run():
    global show_preview
    global enable_ui_elements
    
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    
    if len(global_variables.move_roms_tracing_list) == 0:
        return False

    enable_ui_elements = False
    
    # add the spinner to apply the ui enable change from enable_ui_elements and show the loading animation
    spinner = ui.spinner('dots', size='xl')
    moved_roms = await asyncio.to_thread(move_roms_worker.generate_M3U)

    if moved_roms > 0:
        message = 'Moved ' + str(moved_roms) + ' roms. Check log for details'
        ui.notify(message)
        global_variables.logger.info(message)
        
        show_preview = False
        global_variables.ui_move_roms_preview_table.rows.clear()
        global_variables.ui_move_roms_preview_table.update()

    enable_ui_elements = True
    
    spinner.delete()

