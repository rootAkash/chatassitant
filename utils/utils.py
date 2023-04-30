import os
from typing import Optional,List,Any 
from pathlib import Path
import json
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from utils.encryption import encrypt_the_string,check_the_encrypted_string
from pathlib import Path
def connect_to_gdrive()-> GoogleDrive:
    """connects to gdrive and initialises the folders and returns drive object"""
    """ uses google apis to get access to the gdrive for non colab"""
    """ not in use currently"""

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth() # client_secrets.json need to be in the same directory as the script
    drive = GoogleDrive(gauth)
    return drive

def save_conversation_json_colab(convo_text : str, id : str ,drive : GoogleDrive )-> None:
    """ saves a single converstaion step"""
    save_path = ""
    json_object = {}
    json_object[id] = convo_text
    convo_lst = os.listdir(save_path)
    json_path = str(len(convo_lst)) + ".json"
    with open(json_path, "w") as outfile:
        json.dump(json_object, outfile)

def add_new_user(userdict : dict , path_to_users_json : str) -> dict:
    """userdict : {"username": abc,"password":"ABXSSS"}"""
    path_to_users_json = Path(path_to_users_json)
    if not path_to_users_json.is_file():
        #if file doesnt exist then create a new one
        data = {}
        with open(path_to_users_json, 'w') as f:
            json.dump(data, f)
    with open(path_to_users_json, 'r') as f:
        data = json.load(f)
        if userdict["username"] not in data.keys():
            data[userdict["username"]] =  encrypt_the_string(userdict["password"])
        else:
            raise KeyError("username already exists")
    #rewrite the file with new user added
    os.remove(path_to_users_json)
    with open(path_to_users_json, 'w') as f:
        json.dump(data, f)

    return data

def authorize_user(userdict : dict , path_to_users_json : str) -> bool:
    """userdict : {"username": abc,"password":"ABXSSS"}"""
    path_to_users_json = Path(path_to_users_json)
    if path_to_users_json.is_file():
        with open(path_to_users_json, 'r') as f:
            data = json.load(f)
            if userdict["username"] not in data.keys():
                raise KeyError("username does not exists")
            else:
                return  check_the_encrypted_string(userdict["password"],data[userdict["username"]])
    else:
        raise KeyError("username does not exists")          