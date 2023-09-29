# standard and external libraries
import inspect
from nicegui import ui
from random import randint

# project libraries
import src.global_variables as global_variables
import src.configuration_manager as configuration_manager

ui_extension_input: ui.input
ui_extension_table: ui.table
extensions_edited = False

def edit_extensions_for_M3U_dialog():
    global ui_extension_input
    global ui_extension_table
    global extensions_edited
    
    extensions_edited = False

    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    
    columns = [
        {'name': 'extension', 'label': 'Extension', 'field': 'extension', 'required': True, 'align': 'left'}
        # to hide a column add:
        #'classes': 'hidden', 'headerClasses': 'hidden'
    ]

    # 'w-full items-center'
    with ui.dialog() as global_variables.ui_extensions_for_M3U_dialog, ui.card().classes('w-full h-full'):
        with ui.scroll_area().classes('w-full h-full'):
            with ui.card().classes('no-shadow'):
                with ui.row().classes('items-center'):
                    ui_extension_input = ui.input(label='Extension to add',
                            placeholder='Insert the extension to add',
                            validation={'Extension not starting with .': lambda value: value.startswith('.')}
                        ).classes('w-64')
                    ui.button('Add', on_click=add_extension)
            with ui.card().classes('no-shadow'):
                with ui.row().classes('items-center'):
                    ui_extension_table = ui.table(columns=columns, 
                                                rows=[], 
                                                row_key='extension', 
                                                selection='multiple'
                                                )
                    reload_extensions_table_rows()
                    ui.button('Delete selected', on_click=delete_extensions)
            with ui.card().classes('no-shadow'):
                with ui.row():
                    ui.button('Close', on_click=lambda: close_dialog(extensions_edited))

def reload_extensions_table_rows():
    global ui_extension_table
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    ui_extension_table.rows.clear()
    ui_extension_table.selected.clear()
    
    for item in global_variables.configuration.extensions_for_M3U:
        ui_extension_table.rows.append({
            'extension': item,
        })
    ui_extension_table.update()

def add_extension():
    global ui_extension_input
    global extensions_edited
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    if ui_extension_input.error != None or ui_extension_input.value == '':
        return
    else:
        already_inserted = False
        for item in global_variables.configuration.extensions_for_M3U:
            if item == ui_extension_input.value:
                already_inserted = True
        if already_inserted:
            message = 'Extension ' + ui_extension_input.value + ' already in list. Nothing done'
            ui.notify(message)
            global_variables.logger.info(message)
            return
        else:
            global_variables.configuration.extensions_for_M3U.append(ui_extension_input.value)
            configuration_manager.write_configuration()
            message = 'Added extension ' + ui_extension_input.value + ' to list'
            global_variables.logger.info(message)
            ui.notify(message)
            extensions_edited = True
            reload_extensions_table_rows()
            
def delete_extensions():
    global ui_extension_table
    global extensions_edited
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    if len(ui_extension_table.selected) > 0:
        print(str(ui_extension_table.selected))
        for selected_row in ui_extension_table.selected:
            print(selected_row)
            print(type(selected_row))
            print(selected_row['extension'])
            extension_to_remove = selected_row['extension']
            # iterate from the bottom
            for i in range(len(global_variables.configuration.extensions_for_M3U) - 1, -1, -1):
                if global_variables.configuration.extensions_for_M3U[i] == extension_to_remove:
                    del global_variables.configuration.extensions_for_M3U[i]

            configuration_manager.write_configuration()
            message = 'Removed extension ' + extension_to_remove + ' from list'
            global_variables.logger.info(message)
            ui.notify(message)
            extensions_edited = True
            
        reload_extensions_table_rows()
                    
            
def close_dialog(result):
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    global_variables.ui_extensions_for_M3U_dialog.submit(result)
    