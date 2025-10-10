# vfs/utils.py
import hashlib
import datetime


def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()


def get_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
