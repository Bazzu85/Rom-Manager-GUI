# standard and external libraries
import logging
from nicegui import ui, app

# project libraries
import global_variables as global_variables
import src.log_manager as log_manager
import src.configuration_manager as configuration_manager
import gui.main_gui as main_gui

log_manager.setLogging(logging.INFO)

# read the configuration from file and set the log level
configuration_manager.read_configuration()

main_gui.createGUI()
#ui.run(title='Rom Manager GUI', native=True, dark=True) #, reload=False)
icon = 'icon.png'

title = 'Rom Manager GUI'
if global_variables.configuration.run_in_native_mode:
    app.native.start_args['debug'] = global_variables.configuration.debug
    app.native.start_args['debug'] = False
    # the reload=False is needed to open in native open and close application when closing the window
    ui.run(title=title, dark=True, native=True, favicon=icon, reload=False)
else:
    ui.run(title=title, port=global_variables.configuration.port_number, show=False, dark=True, favicon=icon)