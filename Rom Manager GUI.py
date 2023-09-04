# standard and external libraries
import logging
from nicegui import ui

# project libraries
import src.globals as globals
import src.log_manager as log_manager
import src.configuration_manager as configuration_manager
import gui.main_gui as main_gui

log_manager.setLogging(logging.INFO)

# read the configuration from file and set the log level
configuration_manager.read_configuration()

main_gui.createGUI()
#ui.run(title='Rom Manager GUI', native=True, dark=True) #, reload=False)
ui.run(title='Rom Manager GUI', port=globals.configuration.port_number, show=False, dark=True) #, reload=False)
