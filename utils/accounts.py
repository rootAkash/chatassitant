from utils.utils import add_new_user,authorize_user
from typing import Optional,List,Any
import json

def signin_handler(username : str , password : str) -> dict:
    with open("./config.json", 'r') as f:
        config = json.load(f)
    try:
        res = authorize_user({"username": username,"password":password},config["users_path"])
        if res : 
            return {"result":True}
        else:
            return {"result":False,"error":"wrong password"}
    except Exception as err:
        return {"result":False,"error":err}

def signup_handler(username : str , password : str) -> dict:
    with open("./config.json", 'r') as f:
        config = json.load(f)
    try:
        data = add_new_user({"username": username,"password":password},config["users_path"])
        print(data)
        return {"result":True,"data":data}
    except Exception as err:
        return {"result":False,"error":err}
