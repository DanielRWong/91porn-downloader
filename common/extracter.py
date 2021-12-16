# -*- coding: utf-8 -*-

import re
import threading

from lxml import etree

from utils.log import logger
from utils.get_config import get_th_number
from common.cfdownloader import CFDownloader
from common.jscracker.jscracker import Cracker

log = logger()

def legal_url(url):
    """
    判断url格式是否正确
    :param url:
    :return:
    """
    if re.findall('view_video\.php\?viewkey=\w+', url):
        return True
    else:
        log.warning(f'Url: {url} 格式不正确！')
        return False

def worker():
    while True:
        with lock:
            try:
                url = url_list.pop()
            except IndexError:
                break
        log.info(f'Get url: {url}')
        response = cfdownloader.cfdownload(url)
        page = etree.HTML(response)
        jscode = re.findall('document\.write\(strencode2\((.*?)\)', response)
        jsres = jscracker.crack(jscode)
        try:
            m3u8_url = re.findall('src=\'(.*?)\'', jsres)[0]
        except:
            log.info(f'Extract error: {url}')
            continue
        video_name = ''.join(page.xpath('//div[@id="videodetails"][1]/h4/text()')).strip()
        # log.info(f'url:{url} get \n\tm3u8 url: {m3u8_url}\n\tvideo name: {video_name}')
        m3u8_list.append((m3u8_url, video_name))

def extrcat_url(input_text):
    """
    提取m3u8url和视频名  放入m3u8_list [("m3u8", "视频名称"),("", "")]
    :return:
    """
    global  m3u8_list, url_list
    m3u8_list = []
    url_list = []
    origin_url_list = input_text.split('\n')
    for url in origin_url_list:
        if not legal_url(url):
            continue
        url_list.append(url)
    log.info(f'Get {len(url_list)} urls : {str(url_list)}')
    global cfdownloader, jscracker, lock
    lock = threading.Lock()
    cfdownloader = CFDownloader()
    jscracker = Cracker()
    th_list = []
    th_number = get_th_number()
    for _ in range(int(th_number)):
        th = threading.Thread(target=worker)
        th.start()
        th_list.append(th)
    for th in th_list:
        th.join()
    log.info(f'Get {len(m3u8_list)} m3u8 urls: {str(m3u8_list)}')
    return m3u8_list