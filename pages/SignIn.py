import streamlit as st
from utils.accounts import signin_handler,signup_handler 

if "username" not in st.session_state:
        st.session_state["username"]=""
if "password" not in st.session_state:
        st.session_state["password"]=""
if "signin_sucess" not in st.session_state:
        st.session_state["signin_sucess"]=False
def sign_in():
    res = signin_handler(st.session_state["username"], st.session_state["password"])
    if res["result"]:
        st.session_state["signin_sucess"]=True 
    else:
        st.text(res["error"])
def sign_up():
    if len(st.session_state["username"])> 3 and len(st.session_state["password"]) >3:
        #create a fresh account
        res = signup_handler(st.session_state["username"], st.session_state["password"])
        if res["result"]:
            st.session_state["signin_sucess"]=True 
        else:
            st.text(res["error"])
    else:
        if  len(st.session_state["username"])< 3:
            st.text("use longer username")
        if  len(st.session_state["password"])< 3:
            st.text("use longer password")

if not st.session_state["signin_sucess"]:
    #signin/signup
    username =  st.text_input('username')
    password =  st.text_input('password')

    if username and password:
        st.session_state["username"]  = username
        st.session_state["password"]  = password
    signin = st.button("sign in" ,on_click=sign_in)
    signup = st.button("create new account and signin",on_click=sign_up)
else:
     st.text("Sign in sucessful , make sure you dont loose the password, there is no recovery!!!")