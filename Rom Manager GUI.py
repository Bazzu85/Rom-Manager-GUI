# standard and external libraries
import logging
import sys
from nicegui import ui, app

# project libraries
import src.global_variables as global_variables
import src.instance_manager as instance_manager
import src.log_manager as log_manager
import src.configuration_manager as configuration_manager
import src.user_data_manager as user_data_manager
import gui.main_gui as main_gui

def startup():
    global_variables.logger.info('Starting up application')
    
def shutdown():
    global_variables.logger.info('Shutting down application')
    user_data_manager.write_user_data()
    
def connect():
    global_variables.logger.info('Client connecting')
    
def disconnect():
    global_variables.logger.info('Client disconnecting')
    
log_manager.setLogging(logging.INFO)

# read the configuration from file and set the log level
configuration_manager.read_configuration()

# to use the instance manager the ui.run need to be started with reload=False
me = instance_manager.SingleInstance()

# read the user_data from file and set the log level
user_data_manager.read_user_data()

# schedule the user_data write to file every x seconds (default 60)
user_data_manager.schedule_write()


main_gui.createGUI()

app.on_startup(startup)
app.on_shutdown(shutdown)
app.on_connect(connect)
app.on_disconnect(disconnect)

title = 'Rom Manager GUI'
icon = 'icon.png'

if global_variables.configuration.run_in_native_mode:
    app.native.start_args['debug'] = global_variables.configuration.debug
    app.native.start_args['debug'] = False
    # the reload=False is needed to open in native open and close application when closing the window
    ui.run(title=title, dark=True, native=True, favicon=icon, reload=False)
else:
    ui.run(title=title, port=global_variables.configuration.port_number, show=False, dark=True, favicon=icon, reload=False)
    
