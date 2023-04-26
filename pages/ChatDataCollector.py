import streamlit as st

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
    if st.session_state["chat_type"]  == "Prompt":
        text  = st.text_input('Enter intial Prompt')
        if text : 
            print(text)
            #call save fun() and it returns error if the prompt already exists 
    if st.session_state["chat_type"]  == "Continue":
        #load a random initial conversation tree
        
        text  = st.text_input('Continue from the previous conversation')
        if text : 
            print(text)
            #call save fun() and it returns error if the prompt already exists 
    
    restart = st.button("Restart")
    if restart:
        st.session_state["chat_type"]=None


