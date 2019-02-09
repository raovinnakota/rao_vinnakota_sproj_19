import datetime
import ast
from configparser import ConfigParser
from pymongo import MongoClient

FILE_NAME = 'races.ini'

def section_to_dict(section, parser):
    #change path to your ini file if running locally
    parser.read('/home/robo-advisor/src/universe-config.ini')
    out_dict = {}
    for key in parser[section]:
        temp = ast.literal_eval(parser[section][key])
        out_dict[temp[-1]] = temp
    return out_dict

if __name__ == "__main__":
