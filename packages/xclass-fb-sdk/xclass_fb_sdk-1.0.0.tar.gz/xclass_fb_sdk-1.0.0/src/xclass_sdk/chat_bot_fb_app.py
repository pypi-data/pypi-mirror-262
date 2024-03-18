import shutil
import os

def find_package_folder():
    # Get the path of the current script
    current_script_path = os.path.abspath(__file__)

    # Navigate to the parent directory (assuming your package folder is in the same directory as this script)
    package_folder_path = os.path.dirname(current_script_path)

    return package_folder_path

def copy_folder(source_folder, destination_folder):
    try:
        # Copy the entire contents of the source folder to the destination folder
        shutil.copytree(source_folder, destination_folder)
        print("Folder copied successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")


def copy_file(source_file, destination_file):
    try:
        shutil.copy(source_file, destination_file)
        print(
            f"File '{source_file}' copied to '{destination_file}' successfully.")
    except IOError as e:
        print(f"Unable to copy file. {e}")


def change_file_content(file_path, new_content):
    try:
        # Open the file in write mode
        with open(file_path, 'w') as file:
            # Write the new content to the file
            file.write(new_content)
        print("File content changed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")


class ChatBotFbApp:
    def __init__(self, isProd=True):
        self.isProd = isProd

    def build(self, filePath, destination_folder):
        absPath = os.path.abspath(filePath)
        absDestination = os.path.abspath(destination_folder)
        copy_folder(f"{find_package_folder()}/chat_bot_fb", absDestination)
        copy_file(absPath, f"{absDestination}/logic.py")
