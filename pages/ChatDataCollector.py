import streamlit as st
from utils.conversationtree import store_conversation,sample_conversation
import json
with open("./config.json", 'r') as f:
        config = json.load(f)
if  st.session_state["signin_sucess"]:
    if "chat_type" not in st.session_state:
            st.session_state["chat_type"]=None
    if st.session_state["chat_type"] is None:
        prompt_press = st.button("Enter new prompts!")
        continue_press = st.button("Continue from an existing chat!")

        if prompt_press:
            st.session_state["chat_type"] = "Prompt"
        if continue_press:
            st.session_state["chat_type"] = "Continue"
    #print(st.session_state["chat_type"])
    else:
        #put a drop down list for selecting languages
        lang = st.selectbox('select the language',config["languages"])
        if st.session_state["chat_type"]  == "Prompt":
            st.text("HUMAN:")
            text  = st.text_input('Enter intial Prompt')
            
        if st.session_state["chat_type"]  == "Continue":
            #load a random initial conversation tree
            history = sample_conversation()
            for i in history:
                st.text(i["id"]+":"+i["data"])
            text  = st.text_input('Continue from the previous conversation')
        submit =  st.button("submit")
        if submit:
            if st.session_state["chat_type"]  == "Prompt":
                #save the prompt
                store_conversation(None,text,"HUMAN",lang,st.session_state["username"])
                st.text("prompt saved :"+text)
            if st.session_state["chat_type"]  == "Continue":
                #save the recent reply
                if history[-1]["id"] == "HUMAN":
                     id = "AI"
                if history[-1]["id"] == "AI":
                     id = "HUMAN"
                store_conversation(history,text,id,lang,st.session_state["username"])
                st.text("conversation saved:"+text)

        restart = st.button("Restart")
        if restart:
            st.session_state["chat_type"]=None
else:
    st.text("sign in first to continue")

