import json
import hashlib
import os

TARGET_FILE_CREATORS    = 2
TARGET_FILE_DATES       = 3

def get_file(target):
    with open(get_filename(target), 'rb') as file:
        return json.load(file)

def get_hash(target):
    hasher = hashlib.sha256()
    with open(get_filename(target), 'rb') as file:
        hasher.update(file.read())
        return hasher.hexdigest()

def has_changed(hash, target):
    if is_available(target):
        return get_hash(target) is not hash

def is_available(target):
    if get_filename(target) in os.listdir(os.path.dirname(__file__) + '\\Resources'):
        return True
    return False
    

def get_filename(target):
    if target is TARGET_FILE_DATES:
        return 'Resources\\dates.json'
    elif target is TARGET_FILE_CREATORS:
        return 'Resources\\creators.json'