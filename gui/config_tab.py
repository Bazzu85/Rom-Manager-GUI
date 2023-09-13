# standard and external libraries
import inspect
from nicegui import ui

# project libraries
import src.global_variables as global_variables
import src.configuration_manager as configuration_manager
import gui.extensions_for_file_move_dialogs as extensions_for_file_move_dialogs
import gui.extensions_for_M3U_dialogs as extensions_for_M3U_dialogs

# custom variables
# xxx = ''

def createConfigTab():
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    with ui.card().classes('w-full items-center no-shadow'):
        with ui.row().classes('items-center'):
            global_variables.ui_config_debug_switch = ui.switch('Debug')
            global_variables.ui_config_redirect_logs_to_console_switch = ui.switch('Redirect logs to console')
            global_variables.ui_config_run_in_native_mode_switch = ui.switch('Run in native mode (app reboot required)')
        with ui.row().classes('items-center'):
            global_variables.ui_config_port_number = ui.number(label='Port number', min=0, max= 65353, format='%.0f')
        with ui.row().classes('items-center'):
            global_variables.ui_config_write_user_data_every = ui.number(label='Write user_data every x seconds (if something changes) (app reboot required)', min=0, max= 3600, format='%.0f')
        with ui.row().classes('w-96 items-center'):
            global_variables.ui_config_log_file_input = ui.input(label='Log file location', 
                                                        validation={'Insert something': lambda value: value != ''}).classes('w-full')
        with ui.row().classes('items-center'):
            global_variables.ui_config_extensions_for_file_move_label = ui.label()
            ui.button('Edit', on_click=edit_extensions_for_file_move)
        with ui.row().classes('items-center'):
            global_variables.ui_config_extensions_for_M3U_label = ui.label()
            ui.button('Edit', on_click=edit_extensions_for_M3U)
        with ui.row():
            ui.button('Reload configuration from File', on_click=reload_configuration)
            ui.button('Save configuration', on_click=save_configuration)

    # centralized function to apply bindings
    apply_bindings()
    set_labels()

def reload_configuration():
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    configuration_manager.read_configuration()
    message = 'Configuration reloaded.'
    global_variables.logger.info(message)
    ui.notify(message)
    apply_bindings()
    set_labels()
    
def save_configuration():
    if global_variables.ui_config_log_file_input.error != None:
        message = 'Cannot save configuration. Log file is not valid'
        global_variables.logger.info(message)
        ui.notify(message)
        return
    
    configuration_manager.write_configuration()
    message = 'Configuration saved. Reloading and applying modifications.'
    global_variables.logger.info(message)
    ui.notify(message)
    reload_configuration()

def apply_bindings():
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    global_variables.ui_config_debug_switch.bind_value(global_variables.configuration, 'debug')
    global_variables.ui_config_redirect_logs_to_console_switch.bind_value(global_variables.configuration, 'redirect_logs_to_console')
    global_variables.ui_config_run_in_native_mode_switch.bind_value(global_variables.configuration, 'run_in_native_mode')
    global_variables.ui_config_log_file_input.bind_value(global_variables.configuration, 'log_file')
    global_variables.ui_config_port_number.bind_value(global_variables.configuration, 'port_number')
    global_variables.ui_config_write_user_data_every.bind_value(global_variables.configuration, 'write_user_data_every')
    
def set_labels():
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    global_variables.ui_config_extensions_for_file_move_label.text = 'Extensions enabled for file move: '
    i = 0
    for item in global_variables.configuration.extensions_for_file_move:
        if i > 0:
            global_variables.ui_config_extensions_for_file_move_label.text += ', '
        global_variables.ui_config_extensions_for_file_move_label.text += item
        i += 1
        
    global_variables.logger.debug('Calculated ui_config_extensions_for_file_move_label: ' + global_variables.ui_config_extensions_for_file_move_label.text)
       
    global_variables.ui_config_extensions_for_M3U_label.text = 'Extensions enabled for M3U playlists: '
    i = 0
    for item in global_variables.configuration.extensions_for_M3U:
        if i > 0:
            global_variables.ui_config_extensions_for_M3U_label.text += ', '
        global_variables.ui_config_extensions_for_M3U_label.text += item
        i += 1
    global_variables.logger.debug('Calculated ui_config_extensions_for_M3U_label: ' + global_variables.ui_config_extensions_for_M3U_label.text)
        
async def edit_extensions_for_file_move():
     global_variables.logger.debug(inspect.currentframe().f_code.co_name)
     extensions_for_file_move_dialogs.edit_extensions_for_file_move_dialog()
     result = await global_variables.ui_config_extensions_for_file_move_dialog
     if result:
        # centralized function to apply bindings
        apply_bindings()
        set_labels()

async def edit_extensions_for_M3U():
     global_variables.logger.debug(inspect.currentframe().f_code.co_name)
     extensions_for_M3U_dialogs.edit_extensions_for_M3U_dialog()
     result = await global_variables.ui_config_extensions_for_M3U_dialog
     if result:
        # centralized function to apply bindings
        apply_bindings()
        set_labels()

