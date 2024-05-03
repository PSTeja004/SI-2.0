import os
import sys
import shutil
from PyInstaller.__main__ import run

if sys.platform == 'darwin':  # macOS
    # Build the executable
    run(['SI2.py', '--onefile', '--windowed','--hidden-import', 'numpy', '--hidden-import', 'PIL','--hidden-import', 'PIL.Image','--hidden-import', 'matplotlib', '--add-data', f"{os.getcwd()}:."])

        # Create the "config_new" folder in the "dist" directory if it doesn't exist
    dist_folder = 'dist'
    config_new_folder = os.path.join(dist_folder, 'config_new')
    os.makedirs(config_new_folder, exist_ok=True)

    # Copy the contents of the "config_new" folder (if exists) to the "dist/config_new" folder
    source_config_folder = 'config_new'
    if os.path.exists(source_config_folder):
        for item in os.listdir(source_config_folder):
            source_item = os.path.join(source_config_folder, item)
            destination_item = os.path.join(config_new_folder, item)
            if os.path.isfile(source_item):
                shutil.copy2(source_item, destination_item)
            elif os.path.isdir(source_item):
                shutil.copytree(source_item, destination_item)
elif sys.platform == 'win32':  # Windows
    # Get the list of Python files in the current directory, excluding setup.py
    current_directory = os.getcwd()
    python_files = [file for file in os.listdir(current_directory) if file.endswith(".py") and file != "setup.py"]

    # Build the executable
    run(['SI2.py', '--onefile', '--windowed', '--hidden-import', 'numpy', '--hidden-import', 'PIL', '--hidden-import', 'PIL.Image', '--hidden-import', 'matplotlib','--add-data', f"{os.getcwd()}:."])
    # Create the "config_new" folder in the "dist" directory if it doesn't exist
    dist_folder = 'dist'
    config_new_folder = os.path.join(dist_folder, 'config_new')
    os.makedirs(config_new_folder, exist_ok=True)

    # Copy the contents of the "config_new" folder (if exists) to the "dist/config_new" folder
    source_config_folder = 'config_new'
    if os.path.exists(source_config_folder):
        for item in os.listdir(source_config_folder):
            source_item = os.path.join(source_config_folder, item)
            destination_item = os.path.join(config_new_folder, item)
            if os.path.isfile(source_item):
                shutil.copy2(source_item, destination_item)
            elif os.path.isdir(source_item):
                shutil.copytree(source_item, destination_item)
else:
    print("error")
