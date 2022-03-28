import os
import json
from datetime import datetime
import random
import string

def rand_str(N=10):
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase 
    return ''.join(random.choice(chars) for _ in range(N))

def remove_file(filename):
    os.remove(filename)

def get_dir_path():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))).replace('\\', '/')


def does_dir_exist(path):
    return os.path.exists(path)


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def generate_run_id():
    return datetime.now().strftime('%Y%m%d%H%M%S')


def get_list_from_str(s):
    item_list = list(map(lambda x: x.strip(), s.split(',')))
    print(item_list)


def read_json(path):
	with open(path) as f:
		d = json.load(f)
	return d


def get_str_from_list(item_list):
    s = ''
    for i, item in enumerate(item_list):
        if i != len(item_list) - 1:
            s += item + ','
        else:
            s += item
    return s
