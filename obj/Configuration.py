from pathlib import Path

class Configuration():
    def __init__(self):
        self.debug = True
        self.redirect_logs_to_console = True
        self.log_file = Path.cwd().as_posix() + '/log/log.txt'
        self.port_number = 40000
        self.extensions_for_file_move = ['.bin' , '.cue']
        self.extensions_for_M3U = ['.cue']
        self.last_used_rom_path = Path.cwd().as_posix() 
    def convert_port_number_to_int(self):
        self.port_number = int(self.port_number)
    