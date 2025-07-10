import requests
import json
import datetime
from datetime import timedelta
import time
import requests.cookies

#this function returns 24 last advertice in city and category given to it
def request_to_api(city_number , category_realname , inputtime , i):
    raw_header = {"Accept": "*/*",
               "Accept-Encoding": "deflate, gzip",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
               "Host": "api.divar.ir",
               "Content-Type": "application/json",
               "Content-Length": "444"}
    #current_time = datetime.datetime.utcnow().isoformat()+'Z'
    inputtime = inputtime - timedelta(hours=3 , minutes=30)
    T = inputtime.isoformat()+'Z'
    raw_data = {"city_ids":[city_number],"pagination_data":{"@type":"type.googleapis.com/post_list.PaginationData","last_post_date":T,"page":i,"layer_page":i,},"search_data":{"form_data":{"data":{"category":{"str":{"value":category_realname}}}},"server_payload":{"@type":"type.googleapis.com/widgets.SearchData.ServerPayload","additional_form_data":{"data":{"sort":{"str":{"value":"sort_date"}}}}}}}
    data = json.dumps(raw_data)
    api_address = 'https://api.divar.ir/v8/postlist/w/search'
    response = requests.post(url=api_address , data=data ,headers=raw_header)
    return response.json()
def get_data_by_token(token:str):
    raw_header = {"Accept": "*/*",
               "Accept-Encoding": "deflate, gzip",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
               "Host": "api.divar.ir",
               "Content-Type": "application/json",
               "Content-Length": "444"}
    api_url ='https://api.divar.ir/v8/posts-v2/web/'
    request_url = api_url + token
    response = requests.get(url=request_url)
    return response.text

def get_24(cityNumbers:list , category="ROOT" , page = 0):
    raw_data = {
        "city_ids": cityNumbers,
        "pagination_data": {
            "@type": "type.googleapis.com/post_list.PaginationData",
            "page": page,
            "layer_page": page
        },
        "disable_recommendation": False,
        "map_state": {
            "camera_info": {
                "bbox": {}
            }
        },
        "search_data": {
            "form_data": {
                "data": {
                    "category": {
                        "str": {
                            "value": category
                        }
                    }
                }
            },
            "server_payload": {
                "@type": "type.googleapis.com/widgets.SearchData.ServerPayload",
                "additional_form_data": {
                    "data": {
                        "sort": {
                            "str": {
                                "value": "sort_date"
                            }
                        }
                    }
                }
            }
        }
        }   
    header = {
            "Accept": "*/*",
            "Accept-Encoding": "deflate, gzip",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Host": "api.divar.ir",
            "Content-Type": "application/json",
            "Content-Length": "895"}
    data = json.dumps(raw_data)
    api_address = 'https://api.divar.ir/v8/postlist/w/search'
    responce = requests.post(api_address , headers=header , data=data)
    return responce.json()
