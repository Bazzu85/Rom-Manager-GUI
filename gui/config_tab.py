# standard and external libraries
import inspect
from nicegui import ui

# project libraries
import src.globals as globals
import src.configuration_manager as configuration_manager
import gui.extensions_for_file_move_dialogs as extensions_for_file_move_dialogs
import gui.extensions_for_M3U_dialogs as extensions_for_M3U_dialogs

# custom variables
# xxx = ""

def createConfigTab():
    globals.logger.debug(inspect.currentframe().f_code.co_name)
    with ui.card().classes('w-full items-center no-shadow'):
        with ui.row().classes('items-center'):
            globals.ui_config_debug_switch = ui.switch('Debug')
            globals.ui_config_redirect_logs_to_console_switch = ui.switch('Redirect logs to console')
        with ui.row().classes('items-center'):
            globals.ui_config_port_number = ui.number(label='Port number', min=0, max= 65353, format='%.0f')
        with ui.row().classes('items-center'):
            globals.ui_config_extensions_for_file_move_label = ui.label()
            ui.button('Edit', on_click=edit_extensions_for_file_move)
        with ui.row().classes('items-center'):
            globals.ui_config_extensions_for_M3U_label = ui.label()
            ui.button('Edit', on_click=edit_extensions_for_M3U)
        with ui.row():
            ui.button('Reload configuration from File', on_click=reload_configuration)
            ui.button('Save configuration', on_click=configuration_manager.write_configuration)

    # centralized function to apply bindings
    apply_bindings()
    set_labels()

def reload_configuration():
    globals.logger.debug(inspect.currentframe().f_code.co_name)
    configuration_manager.read_configuration()
    apply_bindings()
    set_labels()
    
def apply_bindings():
    globals.logger.debug(inspect.currentframe().f_code.co_name)
    globals.ui_config_debug_switch.bind_value(globals.configuration, 'debug')
    globals.ui_config_redirect_logs_to_console_switch.bind_value(globals.configuration, 'redirect_logs_to_console')
    globals.ui_config_port_number.bind_value(globals.configuration, 'port_number')
    
def set_labels():
    globals.logger.debug(inspect.currentframe().f_code.co_name)
    globals.ui_config_extensions_for_file_move_label.text = 'Extensions enabled for file move: '
    i = 0
    for item in globals.configuration.extensions_for_file_move:
        if i > 0:
            globals.ui_config_extensions_for_file_move_label.text += ', '
        globals.ui_config_extensions_for_file_move_label.text += item
        i += 1
        
    globals.logger.debug('Calculated ui_config_extensions_for_file_move_label: ' + globals.ui_config_extensions_for_file_move_label.text)
       
    globals.ui_config_extensions_for_M3U_label.text = 'Extensions enabled for M3U playlists: '
    i = 0
    for item in globals.configuration.extensions_for_M3U:
        if i > 0:
            globals.ui_config_extensions_for_M3U_label.text += ', '
        globals.ui_config_extensions_for_M3U_label.text += item
        i += 1
    globals.logger.debug('Calculated ui_config_extensions_for_M3U_label: ' + globals.ui_config_extensions_for_M3U_label.text)
        
async def edit_extensions_for_file_move():
     globals.logger.debug(inspect.currentframe().f_code.co_name)
     extensions_for_file_move_dialogs.edit_extensions_for_file_move_dialog()
     result = await globals.ui_config_extensions_for_file_move_dialog
     if result:
        # centralized function to apply bindings
        apply_bindings()
        set_labels()

async def edit_extensions_for_M3U():
     globals.logger.debug(inspect.currentframe().f_code.co_name)
     extensions_for_M3U_dialogs.edit_extensions_for_M3U_dialog()
     result = await globals.ui_config_extensions_for_M3U_dialog
     if result:
        # centralized function to apply bindings
        apply_bindings()
        set_labels()

