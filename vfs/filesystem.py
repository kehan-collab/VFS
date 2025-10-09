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
        self.files = {}  # name -> File
        self.folders = {}  # name -> Folder


class FileSystem:
    def __init__(self):
        self.root = Folder("root")
        self.current_folder = self.root
        self.path_stack = [self.root]  # keeps track of current path

    # -------------------------------
    # Utility
    # -------------------------------
    def _resolve_path(self, path):
        """
        Returns folder object for the given path.
        Supports relative and absolute paths.
        """
        parts = [p for p in path.strip("/").split("/") if p]
        folder = self.root if path.startswith("/") else self.current_folder
        for part in parts:
            if part == "..":
                # Go up only if not already at root
                if folder != self.root:
                    # navigate one level up
                    folder = self._get_parent(folder)
            elif part in folder.folders:
                folder = folder.folders[part]
            else:
                return None
        return folder

    def _get_parent(self, target_folder):
        """Find the parent folder of a given folder (slow but simple)."""

        def _find_parent(folder, child):
            for sub in folder.folders.values():
                if sub is child:
                    return folder
                found = _find_parent(sub, child)
                if found:
                    return found
            return None

        return _find_parent(self.root, target_folder)

    def _get_current_path(self):
        names = []
        folder = self.current_folder
        while folder != self.root:
            parent = self._get_parent(folder)
            names.append(folder.name)
            folder = parent
        return "/" + "/".join(reversed(names))

    # -------------------------------
    # Commands
    # -------------------------------
    def mkdir(self, path):
        parts = [p for p in path.strip("/").split("/") if p]
        folder = self.root if path.startswith("/") else self.current_folder

        for part in parts[:-1]:
            if part not in folder.folders:
                folder.folders[part] = Folder(part)
            folder = folder.folders[part]

        name = parts[-1]
        if name in folder.folders:
            print("Folder already exists")
        else:
            folder.folders[name] = Folder(name)
            print(f"Folder '{path}' created")

    def create_file(self, path, content=""):
        parts = [p for p in path.strip("/").split("/") if p]
        folder = self.root if path.startswith("/") else self.current_folder

        for part in parts[:-1]:
            if part not in folder.folders:
                folder.folders[part] = Folder(part)
            folder = folder.folders[part]

        name = parts[-1]
        if name in folder.files:
            print("File already exists")
        else:
            folder.files[name] = File(name, content)
            print(f"File '{path}' created")

    def write_file(self, path, content):
        folder = self._resolve_path(os.path.dirname(path)) or self.current_folder
        name = os.path.basename(path)
        if name not in folder.files:
            print("File does not exist")
        else:
            f = folder.files[name]
            f.content = content
            f.modified_at = get_timestamp()
            print(f"Written to '{path}'")

    def read_file(self, path):
        folder = self._resolve_path(os.path.dirname(path)) or self.current_folder
        name = os.path.basename(path)
        if name not in folder.files:
            print("File does not exist")
        else:
            print(folder.files[name].content)

    def list_dir(self, path=None):
        folder = self._resolve_path(path) if path else self.current_folder
        if not folder:
            print("Path not found")
            return
        print(f"Contents of {self._get_current_path() if path is None else path}:")
        print("Folders:", list(folder.folders.keys()))
        print("Files:", list(folder.files.keys()))

    def cd(self, path):
        if path == "/":
            self.current_folder = self.root
            self.path_stack = [self.root]
            return
        target = self._resolve_path(path)
        if target:
            self.current_folder = target
            print(f"Changed directory to {self._get_current_path()}")
        else:
            print("Folder not found")

    # -------------------------------
    # Persistence
    # -------------------------------
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
