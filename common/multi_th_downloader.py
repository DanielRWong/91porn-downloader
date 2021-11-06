# -*- coding: utf-8 -*-

import threading
import multiprocessing

from utils.log import logger
from common.downloader import Downloader
from utils.get_config import get_th_number
from config.m3u8_list import m3u8_list as m3u8_list_file

log = logger()

def  worker():
    while True:
        with lock:
            try:
                task = download_list.pop()
            except IndexError:
                break
        proc = multiprocessing.Process(target=wrapper,args=(task,))
        proc.start()
        proc.join()

def wrapper(task):
    downloader = Downloader(task[0], task[1])
    if not downloader.pre_check():
        return
    downloader.run()

def download_multi_thread(m3u8_list=None):
    global download_list, lock
    download_list = m3u8_list if m3u8_list is not None else m3u8_list_file
    lock = threading.Lock()
    th_list = []
    th_number = get_th_number()
    for _ in range(int(th_number)):
        th = threading.Thread(target=worker)
        th.start()
        th_list.append(th)
    for th in th_list:
        th.join()


if __name__ == '__main__':
    download_multi_thread()  # 手动粘贴m3u8链接到m3u8_list后启动