import streamlit as st
from utils.conversationtree import store_conversation,sample_conversation
from utils.utils import save_json,read_json,overwrite_json,read_image
from utils.attachments import image_file_upload

config = read_json("config","./")
def restart():
    st.session_state["chat_type"]=None
def submit(history,text,lang,attachments):
    if st.session_state["chat_type"]  == "Prompt":
        #save the prompt
        store_conversation(None,text,"HUMAN",lang,st.session_state["username"],attachments)
        st.text("prompt saved :"+text)
    if st.session_state["chat_type"]  == "Continue":
        #save the recent reply
        if history:
            if history[-1]["id"] == "HUMAN":
                    id = "AI"
            if history[-1]["id"] == "AI":
                    id = "HUMAN"
            store_conversation(history,text,id,lang,st.session_state["username"],attachments)
            st.text("conversation saved:"+text)
        else:
            st.text("no chat history , enter prompts first")
        st.session_state["chat_type"]=None
def set_chatype_prompt():
    st.session_state["chat_type"] = "Prompt"
def set_chatype_conti():
    st.session_state["chat_type"] = "Continue"
if  st.session_state["signin_sucess"]:
    if "chat_type" not in st.session_state:
            st.session_state["chat_type"]=None
    if st.session_state["chat_type"] is None:
        st.button("Enter new prompts!",on_click=set_chatype_prompt)
        st.button("Continue from an existing chat!",on_click=set_chatype_conti)
    else:
        lang=config["default_language"]
        history=None
        text=None
        attachments=[]
        if st.session_state["chat_type"]  == "Prompt":
            #put a drop down list for selecting languages
            lang = st.selectbox('select the language',config["languages"],index=config["default_language"])
            st.text("HUMAN:")
            text  = st.text_input('Enter intial Prompt')
            attachments = image_file_upload()
        if st.session_state["chat_type"]  == "Continue":

            #load a random initial conversation tree
            history = sample_conversation()
            
            if history is not None:
                #put a drop down list for selecting languages default ot parent language
                default_lang=config["languages"].index(history[-1]["lang"])
                lang = st.selectbox('select the language',config["languages"],index=default_lang)
                for i in history:
                    st.text(i["id"]+":"+i["data"])
                    #display attached images
                    if i["attachment"]:
                        for img_attch in i["attachment"]:
                            image = read_image(img_attch)
                            st.image(image)
                text  = st.text_input('Continue from the previous conversation')
                attachments = image_file_upload()
            else:
                st.text("no prompts to build up on, start with writing some prompts first!!")
        st.button("submit",on_click=submit,args=(history,text,lang,attachments))
        st.button("Restart",on_click=restart)
            
else:
    st.text("sign in first to continue")

