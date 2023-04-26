import os
from typing import Optional,List,Any
from pathlib import Path
import json

def save_conversation_json(convo_text : str, id : str  )-> None:
    """ saves a single converstaion step"""
    save_path = ""
    json_object = {}
    json_object[id] = convo_text
    convo_lst = os.listdir(save_path)
    json_path = str(len(convo_lst)) + ".json"
    with open(json_path, "w") as outfile:
        json.dump(json_object, outfile)