# standard and external libraries
import inspect
import os
import re
from nicegui import ui
from pathlib import Path

# project libraries
import global_variables as global_variables
from obj.m3u_tracing import M3U_tracing

def generate_preview():
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    
    M3U_tracing_list: [M3U_tracing()] = []
    M3U_tracing_list.clear()
    
    source_path = global_variables.ui_M3U_source_path_input.value
    destination_path = global_variables.ui_M3U_destination_path_input.value
    global_variables.logger.debug('Working on ' + source_path + ' path')
    
    # using the os.walk instead of rglob because return in an entry the folder and all it's files
    for root, folders, files in os.walk(source_path):
        if len(files) == 0:
            continue

        root = Path(root).as_posix()
        global_variables.logger.debug('Working on folder ' + root)
        
        M3U_file_list = []
        
        for file in files:
            global_variables.logger.debug('Working on file ' + str(file))
        
            # check if the current file is allowed (extension)
            if not check_extesion(file):
                global_variables.logger.debug('Item is not ok [extension not allowed]')
            
            # check if the current file is allowed (multidisk pattern)
            if re.search(global_variables.regex_multi_disc, file, re.IGNORECASE):
                global_variables.logger.debug('Item is ok [multidisk pattern]')
                M3U_file_list.append(file)
            else:
                global_variables.logger.debug('Item is not ok [multidisk pattern]')
                continue
        
        # if for the folder we found some files for the M3U playlist, trace it
        if len(M3U_file_list) > 0:
            # calculate the M3U path
            M3U_file_name = str(Path(root).name) + '.m3u'

            if destination_path != '':
                M3U_path = Path(destination_path) / M3U_file_name
            else:
                M3U_path = Path(root) / M3U_file_name
                
            global_variables.logger.debug('Adding ' + str(M3U_file_list) + ' to M3U file ' + str(M3U_path))
            
            M3U_tracing_list.append(
                M3U_tracing(
                    M3U_path=M3U_path,
                    M3U_file_list=M3U_file_list
                )
            )
    return M3U_tracing_list
            
def check_extesion(file):
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    file_extension = Path(file).suffix
    foundExtension = False

    for extension in global_variables.configuration.extensions_for_M3U:
        if extension.upper() == file_extension.upper():
            foundExtension = True
            break

    if foundExtension:
        return True
    else:
        return False



        
