import sys as sys
from configparser import ConfigParser

def section_to_dict(section):
    parser = ConfigParser()
    parser.read(PATH_TO_CONFIG_FILE)
    out_dict = {}
    for key in config[section]:
        out_dict[int(key)] = ast.literal_eval(parser[section][key])
    return(out_dict)

def find_keyword(datajson, keywords):
    datajson = json.loads(data)


def create_keywords(section):
    dict = section_to_list(section)
    keywords = []
    for i in dict:
        keywords.append(dict[i])

def choose_collection(datajson, dict, keywords):
    for keyword in keywords:
        if keyword in datajson['text']:
            word = keyword
            break
    for i in dict:
        if word in dict[i]:
            return i
            break
