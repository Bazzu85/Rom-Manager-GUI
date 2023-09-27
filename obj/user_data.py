from pathlib import Path

class User_Data():
    def __init__(self, 
                 move_roms,
                 create_m3u
                 ):
        self.move_roms = move_roms
        self.create_m3u = create_m3u

class Move_Roms():
    def __init__(self, 
                 choice, 
                 source_path,
                 use_same_folder_for_multidisc,
                 use_different_folder, 
                 destination_path,
                 delete_empty_folders,
                 ):
        self.choice = choice
        self.source_path = source_path
        self.use_same_folder_for_multidisc = use_same_folder_for_multidisc
        self.use_different_folder = use_different_folder
        self.destination_path = destination_path
        self.delete_empty_folders = delete_empty_folders
        
class Create_M3U():
    def __init__(self, 
                 source_path, 
                 use_centralized_folder, 
                 destination_path,
                 overwrite
                 ):
        self.source_path = source_path
        self.use_centralized_folder = use_centralized_folder
        self.destination_path = destination_path
        self.overwrite = overwrite
        
def return_default_user_data():
    user_data = User_Data(
        move_roms= Move_Roms(
            choice=1,
            source_path=str(Path.cwd()),
            use_same_folder_for_multidisc=False,
            use_different_folder= False,
            destination_path= '',
            delete_empty_folders=False,
        ),
        create_m3u= Create_M3U(
            source_path=str(Path.cwd()),
            use_centralized_folder= False,
            destination_path= '',
            overwrite=False,
        )
    )
    return user_data
        
    