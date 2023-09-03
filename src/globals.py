# standard and external libraries
import logging
from nicegui import ui

# project libraries
import src.configuration_manager as configuration_manager

configuration = configuration_manager.Configuration()
configuration_folder = "configuration"
configuration_file = "configuration\configuration.json"

log_folder = "log"
log_file = "log\log.txt"
# using a custom name prevent enabling other library logs
# for example enabling a default log, enable the watched files log of univcorn causing a log loop
# https://github.com/encode/uvicorn/discussions/1656
# https://stackoverflow.com/questions/35325042/python-logging-disable-logging-from-imported-modules
logger = logging.getLogger("custom_application_logger")

# ui elements
ui_config_debug_switch: ui.switch
ui_config_redirect_logs_to_console_switch: ui.switch
ui_config_port_number: ui.number
ui_config_extensions_for_file_move_label: ui.label
ui_config_extensions_for_file_move_dialog: ui.dialog
ui_config_extensions_for_M3U_label: ui.label
ui_config_extensions_for_M3U_dialog: ui.dialog

