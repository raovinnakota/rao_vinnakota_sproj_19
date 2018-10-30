import sys as sys
import ast
from configparser import ConfigParser

PATH_TO_CONFIG_FILE = 'races.ini'
SENATE = ["AZ"]

def section_to_dict(section):
    parser = ConfigParser()
    parser.read(PATH_TO_CONFIG_FILE)
    out_dict = {}
    for key in parser[section]:
        out_dict[int(key)] = ast.literal_eval(parser[section][key])
    out_dict = dict(zip(SENATE, out_dict.values()))
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
    word = "misc"
    for keyword in keywords:
        if keyword in datajson['text']:
            word = keyword
            break
    for i in dict:
        if word in dict[i]:
            return i
            break
