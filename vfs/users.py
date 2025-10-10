# vfs/users.py
import os
from .utils import hash_password

USERS_FILE = "users.bin"


class UserManager:
    def __init__(self):
        self.users = {}
        self.current_user = None
        self.load_users()

    def add_user(self, username, password):
        import os

        if username in self.users:
            print("User already exists")
            return False
        salt = os.urandom(8).hex()
        self.users[username] = (hash_password(password, salt), salt)
        self.save_users()
        print(f"User '{username}' added")
        return True

    def login(self, username, password):
        if username not in self.users:
            print("User does not exist")
            return False
        hashed, salt = self.users[username]
        if hash_password(password, salt) == hashed:
            self.current_user = username
            print(f"Logged in as {username}")
            return True
        else:
            print("Incorrect password")
            return False

    def save_users(self):
        import pickle

        with open(USERS_FILE, "wb") as f:
            pickle.dump(self.users, f)

    def load_users(self):
        import pickle

        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "rb") as f:
                self.users = pickle.load(f)
