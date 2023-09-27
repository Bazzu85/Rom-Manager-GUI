# standard and external libraries
import inspect
import logging
from typing import Any
import jsonpickle
from pathlib import Path
from nicegui import ui

# project libraries
import obj.user_data as ud
import src.global_variables as global_variables

def read_user_data():

    # the logging level is not yet setted so for test purpose we set forced here
    # comment after finish
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    
    # create user_data file directory if missing
    Path(global_variables.user_data_file).parent.mkdir(exist_ok=True)
    
    # if user_data file doesn't exist, create it and return the object used
    if Path(global_variables.user_data_file).exists() and Path(global_variables.user_data_file).is_file():
        pass
    else:
        write_user_data()
        message = 'User_data file missing. A default file is been created at ' + global_variables.user_data_file
        print(message)
        global_variables.logger.info(message)
        return 
    
    # if user_data file exist, read it from file
    with open(file=global_variables.user_data_file, mode='r') as file:
        jsonString = file.read()
        file.close
        new_user_data = ud.return_default_user_data()
        new_user_data = jsonpickle.decode(jsonString)
        new_user_data = add_missing_attributes(new_user_data)
        new_user_data = remove_not_needed_attributes(new_user_data)
        global_variables.user_data = new_user_data
        
        # serialize returned object to compare to original one. if different save to file
        new_user_data_json_string = jsonpickle.encode(new_user_data)
        if new_user_data_json_string != jsonString:
            write_user_data()
        else:
            global_variables.user_data_on_file_json = new_user_data_json_string

            
           
def add_missing_attributes(new_user_data):
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    keys_to_add = []

    for basic_key, basic_value in global_variables.user_data.__dict__.items():
        # global_variables.logger.debug(' basic_key: ' + basic_key)
        # global_variables.logger.debug(' basic_value: ' + str(basic_value))

        basic_key_found = False
        for new_key, new_value in new_user_data.__dict__.items():
            # global_variables.logger.debug(' new_key: ' + new_key)
            # global_variables.logger.debug(' new_key: ' + str(new_value))
            if new_key == basic_key:
                basic_key_found = True
                break
        if not basic_key_found:
            keys_to_add.append([basic_key, basic_value])
            
    for key, value in keys_to_add:
        setattr(new_user_data, key, value)
        global_variables.logger.info('Added missing key: ' + key)
        global_variables.logger.info('Added missing value: ' + str(value))

    return new_user_data
    
def remove_not_needed_attributes(new_user_data):
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    
    keys_to_remove = []
    for new_key, new_value in new_user_data.__dict__.items():
        # global_variables.logger.debug(' new_key: ' + new_key)
        # global_variables.logger.debug(' new_key: ' + str(new_value))
        new_key_found = False
        for basic_key, basic_value in global_variables.user_data.__dict__.items():
            # global_variables.logger.debug(' basic_key: ' + basic_key)
            # global_variables.logger.debug(' basic_value: ' + str(basic_value))
            if basic_key == new_key:
                new_key_found = True
                break
        if not new_key_found:
            keys_to_remove.append([new_key, new_value])

    for key, value in keys_to_remove:
        delattr(new_user_data, key)
        global_variables.logger.info('Removed not needed key: ' + key)
        global_variables.logger.info('Removed not needed value: ' + str(value))
        
    return new_user_data


def write_user_data():
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)
    
    # check if current user_data differ from the one in the file
    global_variables.user_data_json = jsonpickle.encode(global_variables.user_data)
    if global_variables.user_data_json == global_variables.user_data_on_file_json:
        global_variables.logger.debug('Not writing to file. user_data_json and user_data_on_file_json are the same')
        return
    
    # create config file directory if missing
    Path(global_variables.user_data_file).parent.mkdir(exist_ok=True)

    global_variables.user_data_on_file_json = global_variables.user_data_json
    with open(file=global_variables.user_data_file, mode='w') as file:
        file.write(global_variables.user_data_json)
        global_variables.logger.debug('Saved user_data.')
        file.close
    
def schedule_write():
    global_variables.logger.debug(inspect.currentframe().f_code.co_name)

    ui.timer(global_variables.configuration.write_user_data_every, lambda: write_user_data())