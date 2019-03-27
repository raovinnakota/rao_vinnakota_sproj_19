import sys as sys
import ast
from configparser import ConfigParser

PATH_TO_CONFIG_FILE = '/root/rao_vinnakota_sproj_19/templates/races.ini'


def section_to_dict(section):
    parser = ConfigParser()
    parser.read(PATH_TO_CONFIG_FILE)
    out_dict = {}
    for key in parser[section]:
        list = ast.literal_eval(parser[section][key])
        out_dict[list[-1]] = list
    return(out_dict)

def find_keyword(datajson, keywords):
    datajson = json.loads(data)


def create_keywords(section):
    dict = section_to_dict(section)
    keywords = []
    for i in dict:
        keywords += (dict[i])
    return(dict, keywords)

def choose_collection(datajson, dict, keywords):
    word = ""
    collection = "misc"
    '''
    for keyword in keywords:
        for key in keyword.split(' '):
            print(key)
            if key in datajson['text']:
                word = key
    '''
    if(word != ""):
        for i in dict:
            if word in dict[i]:
                return i
                break
    print(collection)
    return(collection)
