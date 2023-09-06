# standard and external libraries
import inspect
import logging
from nicegui import ui, app

# project libraries
import src.global_variables as global_variables
import gui.config_tab as config_tab
import gui.main_tab as main_tab


def createGUI():
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)

    # main tab with the elements
    #  Main
    #  Configuration
    with ui.tabs().classes('w-full') as tabs:
        main = ui.tab('Main')
        config = ui.tab('Configuration')
    with ui.tab_panels(tabs, value=main).classes('w-full'):
        with ui.tab_panel(main):
            main_tab.createMainTab()
        with ui.tab_panel(config):
            config_tab.createConfigTab()
            
    

