from pathlib import Path

class User_Data():
    def __init__(self, 
                 create_m3u
                 ):
        self.create_m3u = create_m3u

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
        create_m3u= Create_M3U(
            source_path=Path.cwd().as_posix(),
            use_centralized_folder= False,
            destination_path= ''
        )
    )
    return user_data
        
    