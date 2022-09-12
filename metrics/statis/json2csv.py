from pathlib import Path
from pickle import FALSE, TRUE
from re import split
import sys
import os
import types
import json
import csv

def is_json_file(file_name):
     #check file_name postfix
    if file_name[-len('.json'):] != '.json':
        return FALSE
    return TRUE   

def load_jsonfile(file_name):
    json_path = Path(file_name)
    with json_path.open('r', encoding='utf-8') as data_f:
        data = json.loads(data_f.read())
    self.TestInfor.load_from_dict(data)

    self.load_from_dict(data['memory-footprint-inside-container'])
    return


