import os
import subprocess
from pathlib import Path
import nicegui

cmd = [
    'python',
    '-m', 'PyInstaller',
    'Rom Manager GUI.py', # your main file with ui.run()
    '--name', 'Rom Manager GUI', # name of your app
    '--icon', 'icon.png',
    '--onefile',
    '--windowed', # prevent console appearing, only use with ui.run(native=True, ...)
    '--add-data', f'{Path(nicegui.__file__).parent}{os.pathsep}nicegui'
]
subprocess.call(cmd)
input('Press enter to continue.')