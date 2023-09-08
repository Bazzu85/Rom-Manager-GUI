from pathlib import Path

class Configuration():
    def __init__(self, 
                 debug, 
                 redirect_logs_to_console, 
                 run_in_native_mode, 
                 log_file,
                 port_number,
                 extensions_for_file_move,
                 extensions_for_M3U
                 ):
        self.debug = debug
        self.redirect_logs_to_console = redirect_logs_to_console
        self.run_in_native_mode = run_in_native_mode
        self.log_file = log_file
        self.port_number = port_number
        self.extensions_for_file_move = extensions_for_file_move
        self.extensions_for_M3U = extensions_for_M3U
    def convert_port_number_to_int(self):
        self.port_number = int(self.port_number)
        
def return_default_configuration():
    configuration = Configuration(
        debug= False,
        redirect_logs_to_console= False,
        run_in_native_mode= False,
        log_file= Path.cwd().as_posix() + '/log/log.txt',
        port_number= 40000,
        extensions_for_file_move=['.bin' , '.cue'],
        extensions_for_M3U= ['.cue'],
    )
    return configuration
        
    