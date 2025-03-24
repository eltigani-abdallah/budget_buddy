'''this file will include functions relating to loading languages'''

import json
import os

def load_lang(langs):
    '''
    load language file
    '''
    with open (langs,"r", encoding="utf-8") as file:
        return json.load(file)
    
lang_dict=load_lang("./assets/lang.json") #languages file

def translate(lang, key):
    '''
    translates to lang by taking key and using the value associated
    '''
    return lang_dict.get(lang,{}).get(key,f"[{key} not found]")