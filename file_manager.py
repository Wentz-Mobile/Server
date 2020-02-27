import json
import hashlib
import os

TARGET_FILE_CREATORS    = 2
TARGET_FILE_ROLES       = 3
TARGET_FILE_DATES       = 4

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
    return False

def is_available(target):
    if get_filename(target) in os.listdir(os.path.dirname(__file__) + '\\Resources'):
        return True
    return False
    

def get_filename(target):
    if target is TARGET_FILE_DATES:
        return 'Resources\\dates.json'
    elif target is TARGET_FILE_CREATORS:
        return 'Resources\\creators.json'
    elif target is TARGET_FILE_ROLES:
        return 'Resources\\roles.json'

def get_role(key):
    if is_available(TARGET_FILE_ROLES):
        with open(get_filename(TARGET_FILE_ROLES), 'rb') as file:
            for role in json.load(file):
                if role['key'] is key:
                    return role
    return None
