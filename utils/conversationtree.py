from typing import Optional,List,Any
import json
import os
from pathlib import Path
from utils.utils import save_json,read_json,overwrite_json

def store_conversation(prev_conv_history : List[dict] or None , input: str ,id :str, lang : str,user :str )->None:
    """stores a single node of conversation
        prev_conv_history : list of dicts contating data of previous conversations None if its an initial prompt
        input : current text input
        id : AI or HUMAN
        lang: language (english,hinglish,hindi,telegu,etc)
        user:username of the user that enetered the data

    """
    with open("./config.json", 'r') as f:
        config = json.load(f)
    initial_prompt = True if prev_conv_history is None else False

    data ={ "id":id,
            "lang":lang,
            "root":initial_prompt,
            "children": [],
            "data" : input,
            "user":user,
            "rank":None
            }
    
    file_name = str(len(os.listdir(Path(config["data_path"]))))
    save_json(data,file_name,config["data_path"])
    if not initial_prompt:
        update_parents(prev_conv_history,file_name)
def update_parents():
    return
def generate_tree_data():
    return
def sample_conversations():
    """ rank trees starting from initial prompt based on levels and nodes in each level
        select  a child node from smallest tree  having least ( children in level+level) 
        returns the entire conversation path
    """
    return
