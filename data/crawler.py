from data.divar22 import request_to_api , get_data_by_token , get_24
import re
from data.feature_extractor import extract_features
from datetime import datetime , timedelta
import time
import json
import pandas as pd
import random
import os

def write_csv(li:list):
    with open("dataset.csv" , 'a' , encoding='utf-8') as tok:
        for item in li:
            tok.write(str(item))
            if li.index(item) != 4:
                tok.write(',')
        tok.write('\n')
    
def dump_csv_tokens(l:list , name = 'Tokens'):
    with open(f"{name}.csv" , 'a' , encoding='utf-8') as tok:
        for item in l:
            tok.write(str(item))
            tok.write('\n')
def Horof_to_numeric(string:str):
    if string == "یک":
        return 1
    elif string == "دو":
        return 2
    elif string == "سه":
        return 3
    elif string == "چهار":
        return 4
    elif string == "پنج" :
        return 5
    elif string == "شش":
        return 6
    elif string == "هفت":
        return 7
    elif string == "هشت" :
        return 8
    elif string == "نه":
        return 9
    elif string == "ده":
        return 10
    elif string == "یازده" :
        return 11
    elif string == "بدون اتاق":
        return 0

def scroll_and_save_tokens(citynumber,categoryName):
    alan = datetime.now()
    i = 0
    while True:
        test = get_24(cityNumbers=citynumber,category=categoryName , page=i)
        tokens = test["action_log"]['server_side_info']['info']['tokens']
        dump_csv_tokens(l=tokens,name=  f"{categoryName}_CID_{citynumber}")
        print(tokens[-1] , " Done.page = ",i)
        i+=1
        time.sleep(random.uniform(3 , 5))
def Clean_tokens(name , city):
    df = pd.read_csv(f"{name}_CID_{city}.csv")
    print(len(df))
    df = df.drop_duplicates()
    print(len(df))
    df.to_csv(f"Cleaned_{name}_CID_{city}.csv" , index=False)
def get_information(name , city):
    with open(f"Cleaned_{name}_CID_{city}.csv" , 'r') as tok:
        tokens = tok.read().split('\n')
        tokens.pop()
    r = len(tokens)
    for token in tokens:
        try:
            responce = json.loads(get_data_by_token(token))
            features = extract_features(responce)
            df_row = pd.DataFrame([features])
            first_write = False
            df_row.to_csv(f'CID_{city}.csv', mode='a', header=first_write, index=False, encoding='utf-8-sig')
            os.system('cls')
            r-=1
            timeremaining = f"({int(r*1.5/60)} ~ {int(r*2.5/60)})Minutes"
            print(token , " Done.",r , " items remaining",timeremaining)
            time.sleep(random.uniform(1.5, 2.5))
        except Exception as e:
            dump_csv_tokens([token],"lost")
            print(f"{e} for {token}")
            time.sleep(2)

