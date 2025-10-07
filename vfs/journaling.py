# vfs/journaling.py
from .utils import get_timestamp

class Journal:
    def __init__(self):
        self.entries = []

    def log(self, action, target, user):
        timestamp = get_timestamp()
        entry = f"{timestamp} | {user} | {action} | {target}"
        self.entries.append(entry)

    def show(self):
        for e in self.entries:
            print(e)
