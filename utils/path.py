# -*- coding: utf-8 -*-

import os

from utils.log import logger
from config.config import output_path

log = logger()

def get_basedir_path():
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def check_output_path():
    if not os.path.exists(output_path):
        log.info(f'Make output dir {output_path}')
        make_path(output_path)

def make_path(path):
    path_tuple = os.path.split(path)
    if not os.path.exists(path_tuple[0]):
        make_path(path_tuple[0])
    os.mkdir(path)