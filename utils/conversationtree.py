from typing import Optional,List,Any,Tuple
import json
import os
from pathlib import Path
from utils.utils import save_json,read_json,overwrite_json
from utils.attachments import image_file_save

def store_conversation(prev_conv_history : List[dict] or None , input: str ,id :str, lang : str,user :str,attachments : List[Any] )->None:
    """stores a single node of conversation
        prev_conv_history : list of dicts contating data of previous conversations None if its an initial prompt
        input : current text input
        id : AI or HUMAN
        lang: language (english,hinglish,hindi,telegu,etc)
        user:username of the user that enetered the data

    """
    config = read_json("config","./")
    initial_prompt = True if prev_conv_history is None else False
    parent = None if prev_conv_history is None else prev_conv_history[-1]["file_name"]
    file_name = str(len(os.listdir(Path(config["data_path"]))))
    data ={ "id":id,
            "lang":lang,
            "root":initial_prompt,
            "parent": parent,
            "children": [],
            "data" : input,
            "user":user,
            "rank":None,
            "file_name":file_name,
            "attachment":image_file_save(attachments),
            "labels":[],
            }
    
    
    save_json(data,file_name,config["data_path"])
    if not initial_prompt:
        update_parents(prev_conv_history,file_name,config)

def update_parents(chat_trace:List[dict],child_file_name:str,config:dict)->None:
    """adds new child to parent"""
    parent = chat_trace[-1]
    parent["children"].append(child_file_name)
    overwrite_json(parent,parent["file_name"],config["data_path"])


def generate_tree_data(root:dict , all_data :dict)-> dict:
    """returns scores for all nodes īn  the  tree """
    data = {}
    def tree_search(node:dict,level:int)->None:
        """recursive dfs"""
        score = level+len(node["children"])
        data[node["file_name"]]=score
        for c in node["children"]:
            tree_search(all_data[c],level+1)
        
    tree_search(root,0)
    return data
def get_conv_trace(node_name:str)->List[dict] or None:
    """return the converstation path that leads from root to eneterd node"""
    config = read_json("config","./")
    data=[]
    while True:
        d = read_json(node_name,config["data_path"])
        data.append(d)
        node_name=d["parent"]
        if node_name ==None:
            break
    return data[::-1]
def sample_conversation() ->List[dict] :
    """ rank trees starting from initial prompt based on levels and nodes in each level
        select  a child node from smallest tree  having least ( children in level+level) 
        returns the entire conversation path trace
    """
    config = read_json("config","./")
    data_path = config["data_path"]
    #read all fresh data and get list of all initial prompts/roots
    full_data={}
    node_data=[]
    if len(os.listdir(Path(data_path))) ==0:
        return None
    for i in os.listdir(Path(data_path)):
        data = read_json(i,data_path,apply_extension=False)
        full_data[data["file_name"]] = data
    #call generate_tree_data to get scores of chat tree
    for d in full_data.values():
        if d["root"]:
            node_data.append(generate_tree_data(d,full_data))
    #take the shortest tree
    shortest_tree = min(node_data, key=len)
    minimum_score_node = min(shortest_tree, key=lambda k: shortest_tree[k])
    return get_conv_trace(minimum_score_node)
"""VQA utils """
def store_vqa(prev_conv_history : List[dict] or None , input: str ,id :str, lang : str,user :str,attachments : List[Any] )->None:
    """stores a single node of conversation
        prev_conv_history : list of dicts contating data of previous conversations None if its an initial prompt
        input : current text input
        id : AI or HUMAN
        lang: language (english,hinglish,hindi,telegu,etc)
        user:username of the user that enetered the data

    """
    config = read_json("config","./")
    initial_prompt = True if prev_conv_history is None else False
    parent = None if prev_conv_history is None else prev_conv_history[-1]["file_name"]
    file_name = str(len(os.listdir(Path(config["vqa_data_path"]))))
    data ={ "id":id,
            "lang":lang,
            "root":initial_prompt,
            "parent": parent,
            "children": [],
            "data" : input,
            "user":user,
            "rank":None,
            "file_name":file_name,
            "attachment":image_file_save(attachments),
            "labels":[],
            }
    
    
    save_json(data,file_name,config["vqa_data_path"])
    if not initial_prompt:
        update_vqa_parents(prev_conv_history,file_name,config)
def update_vqa_parents(chat_trace:List[dict],child_file_name:str,config:dict)->None:
    """adds new child to parent"""
    parent = chat_trace[-1]
    parent["children"].append(child_file_name)
    overwrite_json(parent,parent["file_name"],config["vqa_data_path"])
def sample_vqa(ctr) ->List[dict] :
    """ vqa is not a tree but a sequence of responses but stored as linked list /single branch tree
        input: counter value out of total coversations
        returns the entire conversation path trace and total number of roots
    """
    
    config = read_json("config","./")
    data_path = config["vqa_data_path"]
    #read all fresh data and get list of all initial prompts/roots
    root_data=[]
    root_names=[]
    if len(os.listdir(Path(data_path))) ==0:
        return None
    for i in os.listdir(Path(data_path)):
        data = read_json(i,data_path,apply_extension=False)
        if data["root"]:
            root_data.append(data)
            root_names.append(int(data["file_name"]))      
    #take the tree according to counter value
    root_names.sort()
    ctr = ctr% len(root_data)
    tree_root = str(root_names[ctr])
    return get_vqa_trace(tree_root)
def get_vqa_trace(node_name:str)->List[dict] or None:
    """return the converstation path that leads from root to final node"""
    config = read_json("config","./")
    data=[]
    while True:
        d = read_json(node_name,config["vqa_data_path"])
        data.append(d)
        node_name=None
        if len(d["children"]):
            node_name=d["children"][0]
        if node_name ==None:
            break
    return data