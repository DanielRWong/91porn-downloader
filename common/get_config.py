# -*- coding: utf-8 -*-

import re

def get_th_number():
    with open('.\config\config.py', 'r', encoding='utf-8') as f:
        config = f.read()
        return re.findall('th_number = (\d+)', config)[0]

def get_output_path():
    with open('.\config\config.py', 'r', encoding='utf-8') as f:
        config = f.read()
        return re.findall('output_path = \'(.+)\'', config)[0]