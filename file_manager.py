import json
import hashlib
import os
import constants

def get_file(target):
    with open(get_filename(target), 'rb') as file:
        file = json.load(file)
        return file

def get_hash(target):
    hasher = hashlib.sha256()
    with open(get_filename(target), 'rb') as file:
        hasher.update(file.read())
        return hasher.hexdigest()

def has_changed(hash, target):
    return get_hash(target) is not hash
    

def get_filename(target):
    if target is constants.TARGET_FILE_DATES:
        return 'Resources\\dates.json'
    elif target is constants.TARGET_FILE_CREATORS:
        return 'Resources\\creators.json'
    elif target is constants.TARGET_FILE_ROLES:
        return 'Resources\\roles.json'

def get_role(key):
    with open(get_filename(constants.TARGET_FILE_ROLES), 'rb') as file:
        pending = json.load(file)
        while pending:
            if pending[0]['key'] is key:
                return pending[0]
            pending.extend(pending[0]['childs'])
            pending.pop(0)
    return None

