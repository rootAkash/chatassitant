import os
from typing import Optional,List,Any 
from pathlib import Path
import json
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from utils.encryption import encrypt_the_string,check_the_encrypted_string

def connect_to_gdrive()-> GoogleDrive:
    """connects to gdrive and initialises the folders and returns drive object"""
    """ uses google apis to get access to the gdrive for non colab"""
    """ not in use currently"""

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth() # client_secrets.json need to be in the same directory as the script
    drive = GoogleDrive(gauth)
    return drive

def save_json(dict_to_save : dict, file_name : str ,save_folder : str  ,apply_extension :bool =True)-> None:
    """ saves a dict as json in specified folder with a given name"""
    json_path = Path(save_folder+ file_name)
    if apply_extension:
        json_path = Path(save_folder+ file_name + ".json")
    with open(json_path, "w") as outfile:
        json.dump(dict_to_save, outfile)

def overwrite_json(dict_to_save : dict, file_name : str ,save_folder : str  ,apply_extension :bool =True)-> None:
    """ overwrites a dict as json in specified folder with a given name"""
    json_path = Path(save_folder+ file_name)
    if apply_extension:
        json_path = Path(save_folder+ file_name + ".json")
    #rewrite the file with new user added
    os.remove(json_path)
    with open(json_path, "w") as outfile:
        json.dump(dict_to_save, outfile)

def read_json( file_name : str ,save_folder : str  ,apply_extension :bool =True)-> dict:
    """ reads a json as dict in specified folder with a given name"""
    json_path = Path(save_folder+ file_name)
    if apply_extension:
        json_path = Path(save_folder+ file_name + ".json")
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data

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