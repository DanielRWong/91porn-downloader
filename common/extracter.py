# -*- coding: utf-8 -*-

import re
import threading

from lxml import etree

from utils.log import logger
from common.cfdownloader import CFDownloader
from common.jscracker.jscracker import Cracker

m3u8_list = []
log = logger()

def legal_url(url):
    """
    判断url格式是否正确
    :param url:
    :return:
    """
    return True if re.findall('https://www\.91porn\.com/view_video\.php\?viewkey=\w+', url)\
        else False


def worker(url):
    log.info(f'Get url: {url}')
    response = cfdownloader.cfdownload(url)
    page = etree.HTML(response)
    jscode = re.findall('document\.write\(strencode2\((.*?)\)', response)
    jsres = jscracker.crack(jscode)
    m3u8_url = re.findall('src=\'(.*?)\'', jsres)[0]
    video_name = ''.join(page.xpath('//div[@id="videodetails"][1]/h4/text()')).strip()
    log.info(f'url:{url} get \n\tm3u8 url: {m3u8_url}\n\t video name: {video_name}')
    m3u8_list.append((m3u8_url, video_name))

def extrcat_url(input_text):
    """
    提取m3u8url和视频名  放入m3u8_list [("m3u8", "视频名称"),("", "")]
    :return:
    """
    origin_url_list = input_text.split('\n')
    url_list = []
    for url in origin_url_list:
        if not legal_url(url):
            log.warning(f'Url: {url}格式不正确！')
            continue
        url_list.append(url)
    log.info(f'Get url list: {str(url_list)}')
    global cfdownloader,jscracker
    cfdownloader = CFDownloader()
    jscracker = Cracker()
    th_list = []
    for url in url_list:
        th = threading.Thread(target=worker,args=(url,))
        th.start()
        th_list.append(th)
    for th in th_list:
        th.join()
    log.info(f'Get m3u8 list: {str(m3u8_list)}')
    return m3u8_list