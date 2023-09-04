# standard and external libraries
import inspect
import logging
from typing import Any
import jsonpickle
from pathlib import Path

# project libraries
from obj.Configuration import Configuration
import src.globals as globals
import src.pathManager as pathManager
import src.log_manager as log_manager

def read_configuration():

    # the logging level is not yet setted so for test purpose we set forced here
    # comment after finish
    log_manager.setLogging(logging.DEBUG)
    globals.logger.debug(inspect.currentframe().f_code.co_name)
    
    # create config file directory if missing
    Path(globals.configuration_file).parent.mkdir(exist_ok=True)
    
    # if configuration file doesn't exist, create it and return the object used
    if Path(globals.configuration_file).exists() and Path(globals.configuration_file).is_file():
        pass
    else:
        write_configuration()
        message = 'Configuration file missing. A default file is been created at ' + globals.configuration_file
        print(message)
        globals.logger.info(message)
        exit()
    
    # if configuration file exist, read it from file
    with open(file=globals.configuration_file, mode='r') as file:
        jsonString = file.read()
        file.close
        newConfiguration = Configuration()
        newConfiguration = jsonpickle.decode(jsonString)
        newConfiguration.convert_port_number_to_int()
        newConfiguration = add_missing_attributes(newConfiguration)
        newConfiguration = remove_not_needed_attributes(newConfiguration)
        globals.configuration = newConfiguration
        
        # serialize returned object to compare to original one. if different save to file
        newConfigurationJsonString = jsonpickle.encode(newConfiguration)
        if newConfigurationJsonString != jsonString:
            write_configuration()
            
    # set logging level and the redirect to console
    if globals.configuration.debug:
        log_manager.setLogging(logging.DEBUG)
    else:
        log_manager.setLogging(logging.INFO)

           
def add_missing_attributes(newConfiguration):
    globals.logger.debug(inspect.currentframe().f_code.co_name)
    keys_to_add = []

    for basic_key, basic_value in globals.configuration.__dict__.items():
        # globals.logger.debug(' basic_key: ' + basic_key)
        # globals.logger.debug(' basic_value: ' + str(basic_value))

        basic_key_found = False
        for new_key, new_value in newConfiguration.__dict__.items():
            # globals.logger.debug(' new_key: ' + new_key)
            # globals.logger.debug(' new_key: ' + str(new_value))
            if new_key == basic_key:
                basic_key_found = True
                break
        if not basic_key_found:
            keys_to_add.append([basic_key, basic_value])
            
    for key, value in keys_to_add:
        setattr(newConfiguration, key, value)
        globals.logger.info('Added missing key: ' + key)
        globals.logger.info('Added missing value: ' + str(value))

    return newConfiguration
    
def remove_not_needed_attributes(newConfiguration):
    globals.logger.debug(inspect.currentframe().f_code.co_name)
    
    keys_to_remove = []
    for new_key, new_value in newConfiguration.__dict__.items():
        # globals.logger.debug(' new_key: ' + new_key)
        # globals.logger.debug(' new_key: ' + str(new_value))
        new_key_found = False
        for basic_key, basic_value in globals.configuration.__dict__.items():
            # globals.logger.debug(' basic_key: ' + basic_key)
            # globals.logger.debug(' basic_value: ' + str(basic_value))
            if basic_key == new_key:
                new_key_found = True
                break
        if not new_key_found:
            keys_to_remove.append([new_key, new_value])

    for key, value in keys_to_remove:
        delattr(newConfiguration, key)
        globals.logger.info('Removed not needed key: ' + key)
        globals.logger.info('Removed not needed value: ' + str(value))
        
    return newConfiguration


def write_configuration():
    globals.logger.debug(inspect.currentframe().f_code.co_name)
    
    # create config file directory if missing
    Path(globals.configuration_file).parent.mkdir(exist_ok=True)

    globals.configuration.convert_port_number_to_int()

    jsonString = jsonpickle.encode(globals.configuration)
    with open(file=globals.configuration_file, mode='w') as file:
        file.write(jsonString)
        file.close
        
    # set logging level and the redirect to console
    if globals.configuration.debug:
        log_manager.setLogging(logging.DEBUG)
    else:
        log_manager.setLogging(logging.INFO)
    