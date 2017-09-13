import requests
import json
def read_html_content(url):
    #url = "https://apps.pnc.com/apps/servlet/ExternalPopup?page=http://www.sec.gov/rules/final/34-51983fr.pdf"
    res = requests.get(url)
    text = res.text
    return text
    #print(text)
def store_dictionary(dictionary, key, value):
    #aDict = {}
    dictionary[key] = value
              
def jason_save(json_file_name, dictionary):    
    with open(json_file_name, 'w') as fp:
        json.dump(dictionary, fp)