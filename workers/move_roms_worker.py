# standard and external libraries
import inspect
import os
import re
import time
from nicegui import ui
from pathlib import Path

# project libraries
import src.global_variables as global_variables
from obj.move_tracing import Move_Tracing

def generate_preview():
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    
    global_variables.logger.debug('Working on ' + global_variables.user_data.move_roms.source_path + ' path')
    
    if global_variables.user_data.move_roms.choice == global_variables.MOVE_ROMS_TO_SUBFOLDER:
        generate_preview_to_subfolder()
    elif global_variables.user_data.move_roms.choice == global_variables.MOVE_ROMS_TO_FOLDER:
        generate_preview_to_folder()

def generate_preview_to_subfolder():
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    
    global_variables.logger.debug('Generating preview moves to subfolders')

    # using the os.walk instead of rglob because return in an entry the folder and all it's files
    for root, folders, files in os.walk(global_variables.user_data.move_roms.source_path):
        if len(files) == 0:
            continue

        root = str(Path(root))
        global_variables.logger.debug('Working on folder ' + root)
        
        for file in files:
            global_variables.logger.debug('Working on file ' + str(file))
        
            # check if the current file is allowed (extension)
            if not check_extesion(file):
                global_variables.logger.debug('Item is not ok [extension not allowed]')
                continue
            
            if (re.search(global_variables.regex_multi_disc, file, re.IGNORECASE)) and global_variables.user_data.move_roms.use_same_folder_for_multidisc:
                generate_preview_to_subfolder_multidisc(file, root)
            else:
                generate_preview_to_subfolder_singledisc(file, root)
            
def generate_preview_to_subfolder_multidisc(file, root):
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    
    cleanedFileName = clean_file_name(file)

    regexResult = re.split(global_variables.regex_multi_disc, cleanedFileName, re.IGNORECASE)
    global_variables.logger.debug('Check multidisk regex result: ' + str(regexResult))
    
    # starts composing the destination folder
    global_variables.logger.debug('Folder calculated before loop is: ' + destination_folder)

    calculated_folder = ''
    for item in regexResult:
                            
        if re.search(global_variables.regex_multi_disc, item, re.IGNORECASE):
            global_variables.logger.debug('Multidisc pattern found in: ' + item + '. Breaking loop')
            break
        else:
            global_variables.logger.debug('Multidisc pattern not found in: ' + item + '. Appending')
            calculated_folder += item
    
    destination_folder = os.path.join(str(Path(global_variables.user_data.move_roms.source_path)), calculated_folder)
    destination_folder = destination_folder.rstrip()

    global_variables.logger.debug('New folder calculated after loop is: ' + destination_folder)

    if (Path(root) != Path(destination_folder)):
        global_variables.move_roms_tracing_list.append(
            Move_Tracing(
                source=os.path.join(root, file),
                destination=destination_folder
            )
        )
        
def generate_M3U():
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    
    created_m3u_files = 0
    for item in global_variables.m3u_tracing_list:
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
            
        global_variables.logger.info('Created M3U file ' + str(Path(item.M3U_path)) + ' with this discs into: ' + str(item.M3U_file_list))
        created_m3u_files += 1

    return created_m3u_files
        
    
def check_extesion(file):
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    file_extension = Path(file).suffix
    foundExtension = False

    for extension in global_variables.configuration.extensions_for_file_move:
        if extension.upper() == file_extension.upper():
            foundExtension = True
            break

    if foundExtension:
        return True
    else:
        return False

def clean_file_name(file):
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)

    global_variables.logger.debug("Checking if there's some text to remove from filename " + file)

    cleaned_file = ''
    
    regexResult = re.split(global_variables.regex_string_to_remove_for_destination_folder, file, re.IGNORECASE)
    for item in regexResult:
        if re.search(global_variables.regex_string_to_remove_for_destination_folder, item, re.IGNORECASE):
            pass
        else:
            cleaned_file += item

    global_variables.logger.debug('Cleaned file name ' + cleaned_file)
    return cleaned_file

        
