# vfs/protection.py
from .utils import hash_password
import getpass


class ProtectionManager:
    def __init__(self):
        self.protected = {}

    def protect_folder(self, folder_path):
        pw = getpass.getpass(f"Set password for {folder_path}: ")
        salt = "folder_salt"
        self.protected[folder_path] = hash_password(pw, salt)
        print(f"Folder '{folder_path}' protected")

    def check_access(self, folder_path):
        if folder_path not in self.protected:
            return True
        pw = getpass.getpass(f"Enter password to access {folder_path}: ")
        salt = "folder_salt"
        return hash_password(pw, salt) == self.protected[folder_path]
