# vfs/utils.py
import hashlib
import datetime

def hash_password(password, salt):
    """Return SHA-256 hash of password + salt"""
    return hashlib.sha256((password + salt).encode()).hexdigest()

def get_timestamp():
    """Return current timestamp"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
