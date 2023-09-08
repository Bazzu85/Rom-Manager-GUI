# standard and external libraries
import inspect
import os
import re
from nicegui import ui
from pathlib import Path

# project libraries
import src.global_variables as global_variables
from obj.m3u_tracing import M3U_tracing

def generate_preview():
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    
    global_variables.logger.debug('Working on ' + global_variables.user_data.create_m3u.source_path + ' path')
    
    # using the os.walk instead of rglob because return in an entry the folder and all it's files
    for root, folders, files in os.walk(global_variables.user_data.create_m3u.source_path):
        if len(files) == 0:
            continue

        root = str(Path(root))
        global_variables.logger.debug('Working on folder ' + root)
        
        M3U_file_list = []
        
        for file in files:
            global_variables.logger.debug('Working on file ' + str(file))
        
            # check if the current file is allowed (extension)
            if not check_extesion(file):
                global_variables.logger.debug('Item is not ok [extension not allowed]')
                continue
            
            # check if the current file is allowed (multidisk pattern)
            if re.search(global_variables.regex_multi_disc, file, re.IGNORECASE):
                global_variables.logger.debug('Item is ok [multidisk pattern]')
                
                # using a unique folder for the M3U files take to the full rom path in destination file
                if global_variables.user_data.create_m3u.use_centralized_folder:
                    path_to_append = os.path.join(str(Path(global_variables.user_data.create_m3u.destination_path)), file)
                    M3U_file_list.append(path_to_append)
                else:
                    M3U_file_list.append(file)
            else:
                global_variables.logger.debug('Item is not ok [multidisk pattern]')
                continue
        
        M3U_file_list = sorted(M3U_file_list)
        # if for the folder we found some files for the M3U playlist, trace it
        if len(M3U_file_list) > 0:
            # calculate the M3U path
            M3U_file_name = str(Path(root).name) + '.m3u'
            
            if global_variables.user_data.create_m3u.use_centralized_folder:
                M3U_path = Path(global_variables.user_data.create_m3u.destination_path) / M3U_file_name
            else:
                M3U_path = Path(root) / M3U_file_name
            
            if Path(M3U_path).exists() and Path(M3U_path).is_file() and not global_variables.user_data.create_m3u.overwrite:
                global_variables.logger.debug(str(Path(M3U_path).name) + ' already exist. Not overwriting')
                continue

            global_variables.logger.debug('Adding ' + str(M3U_file_list) + ' to M3U file ' + str(M3U_path))
            
            global_variables.M3U_tracing_list.append(
                M3U_tracing(
                    M3U_path=M3U_path,
                    M3U_file_list=M3U_file_list
                )
            )
            

def generate_M3U():
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    
    created_m3u_files = 0
    for item in global_variables.M3U_tracing_list:
        item: M3U_tracing
        if Path(item.M3U_path).exists() and Path(item.M3U_path).is_file() and not global_variables.user_data.create_m3u.overwrite:
            global_variables.logger.info('M3U file ' + Path(item.M3U_path).name + ' already created and overwrite not selected. Skipping')
            continue
        
        with open(file=item.M3U_path, mode="w") as file:
            count = 0
            for element in item.M3U_file_list:
                if count != 0:
                    file.write("\n")
                file.write(element)
                count = count + 1
            file.close
            
        global_variables.logger.info('Created M3U file ' + str(Path(item.M3U_path)) + ' with this files into: ' + str(item.M3U_file_list))
        created_m3u_files += 1
    return created_m3u_files
        
    
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



        
