#Sample python code that depicts the usage of bcrypt function  for hashing of the specified input text   
import bcrypt  
from typing import Optional,List,Any
  


def encrypt_the_string(string_to_encrypt : str ,number_of_rounds : int =16 )-> bytes :
    """encrypts the string or paswword"""
    string_to_encrypt = "{}".format(string_to_encrypt)  
    string_to_encrypt_bytes = string_to_encrypt.encode('utf-8')    
    salt_object = bcrypt.gensalt(rounds=number_of_rounds)  
    resultant_hashed_bytes = bcrypt.hashpw(string_to_encrypt_bytes, salt_object)  
    resultant_hashed_str = resultant_hashed_bytes.decode('utf-8')
    return resultant_hashed_str  




def check_the_encrypted_string(str_to_check : str ,hashed_str : bytes ,number_of_rounds : int=16) -> bool: 
    """checks if the entered password/string matches a """ 
    str_to_check = "{}".format(str_to_check)  
    str_to_check_bytes = str_to_check.encode('utf-8') 
    hashed_bytes =  hashed_str.encode('utf-8') 
    if bcrypt.checkpw(str_to_check_bytes, hashed_bytes):  
        return True  
    else:  
        return False  