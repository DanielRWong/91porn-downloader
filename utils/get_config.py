# -*- coding: utf-8 -*-

import re

from utils.path import get_basedir_path

def get_th_number():
    with open(f'{get_basedir_path()}\config\config.py', 'r', encoding='utf-8') as f:
        config = f.read()
        return re.findall('th_number = (\d+)', config)[0]

def get_output_path():
    with open(f'{get_basedir_path()}\config\config.py', 'r', encoding='utf-8') as f:
        config = f.read()
        return re.findall('output_path = \'(.+)\'', config)[0]