# vfs/filesystem.py
import pickle
import os
from .utils import get_timestamp

FS_FILENAME = "filesystem.bin"

class File:
    def __init__(self, name, content=""):
        self.name = name
        self.content = content
        self.created_at = get_timestamp()
        self.modified_at = get_timestamp()

class Folder:
    def __init__(self, name):
        self.name = name
        self.files = {}      # name -> File
        self.folders = {}    # name -> Folder

class FileSystem:
    def __init__(self):
        self.root = Folder("root")
        self.current_folder = self.root

    def mkdir(self, name):
        if name in self.current_folder.folders:
            print("Folder already exists")
        else:
            self.current_folder.folders[name] = Folder(name)
            print(f"Folder '{name}' created")

    def create_file(self, name, content=""):
        if name in self.current_folder.files:
            print("File already exists")
        else:
            self.current_folder.files[name] = File(name, content)
            print(f"File '{name}' created")

    def write_file(self, name, content):
        if name not in self.current_folder.files:
            print("File does not exist")
        else:
            f = self.current_folder.files[name]
            f.content = content
            f.modified_at = get_timestamp()
            print(f"Written to '{name}'")

    def read_file(self, name):
        if name not in self.current_folder.files:
            print("File does not exist")
        else:
            print(self.current_folder.files[name].content)

    def list_dir(self):
        print("Folders:", list(self.current_folder.folders.keys()))
        print("Files:", list(self.current_folder.files.keys()))

    def save(self):
        with open(FS_FILENAME, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load():
        if os.path.exists(FS_FILENAME):
            with open(FS_FILENAME, "rb") as f:
                return pickle.load(f)
        else:
            return FileSystem()
