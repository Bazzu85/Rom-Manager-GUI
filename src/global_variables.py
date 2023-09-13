# standard and external libraries
import logging
import os
from nicegui import ui
from pathlib import *

# project libraries
import obj.configuration as conf
import obj.user_data as ud

configuration = conf.return_default_configuration()

configuration_file = os.path.join(str(Path.cwd()), 'configuration',  'configuration.json')

user_data = ud.return_default_user_data()
user_data_on_file_json = ''
user_data_json = ''

user_data_file = os.path.join(str(Path.cwd()), 'configuration',  'user_data.json')

# using a custom name prevent enabling other library logs
# for example enabling a default log, enable the watched files log of univcorn causing a log loop
# https://github.com/encode/uvicorn/discussions/1656
# https://stackoverflow.com/questions/35325042/python-logging-disable-logging-from-imported-modules
logger = logging.getLogger('custom_application_logger')

# ui elements
ui_config_debug_switch: ui.switch
ui_config_redirect_logs_to_console_switch: ui.switch
ui_config_run_in_native_mode_switch: ui.switch
ui_config_log_file_input: ui.input
ui_config_port_number: ui.number
ui_config_write_user_data_every: ui.number
ui_config_extensions_for_file_move_label: ui.label
ui_config_extensions_for_file_move_dialog: ui.dialog
ui_config_extensions_for_M3U_label: ui.label
ui_config_extensions_for_M3U_dialog: ui.dialog

ui_M3U_source_path_input: ui.input
ui_M3U_use_centralized_folder_switch: ui.switch
ui_M3U_destination_path_input: ui.input
ui_M3U_overwrite_switch: ui.switch
ui_M3U_preview_button: ui.button
ui_M3U_generate_button: ui.button
ui_M3U_preview_table: ui.table
M3U_tracing_list = []

# regex string to find if a file refer to a multidisc format
regex_multi_disc = r"(\(Disc .+?\)|\(Disk .+?\)|\(Bonus Disc\))"
# regex string to find part of filename to remove from the destination folder name
regex_string_to_remove_for_destination_folder = r"(\(Track .+?\))"

