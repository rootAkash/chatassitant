import json
import streamlit as st
from utils.utils import save_json,read_json,overwrite_json
#load config

path = "./config.json"

config = read_json("config","./")
new_config = config

def submit():
    overwrite_json(new_config,"config","./")

for k in config.keys():
    st.text("current "+ k +":")
    st.write(json.dumps(config[k]))
    data = st.text_input("edit "+ k ,key=k)
    if data:
        new_config[k]=json.loads(data)

st.button("submit",on_click=submit)
    
