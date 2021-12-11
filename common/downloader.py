# -*- coding: utf-8 -*-

import re
import os
import copy
import requests
import threading
from retrying import retry
from urllib.parse import urlparse

from utils.log import logger
from config.config import headers
from utils.path import get_basedir_path
from utils.get_config import get_output_path, get_th_number

log = logger()

class Downloader(object):
    def __init__(self, m3u8_url, video_name):
        self.m3u8_url = m3u8_url
        self.video_name = self.get_video_name(video_name)
        self.video_id = self.get_video_id()
        self.base_dir = get_basedir_path()
        self.ts_dir = self.get_ts_dir_path()
        self.ts_url = self.get_ts_url()
        self.output_name = self.get_output_name()

    def get_ts_url(self):
        result = urlparse(self.m3u8_url)
        return f'{result.scheme}://{result.hostname}//m3u8/{self.video_id}/'

    def get_video_name(self, video_name):
        return video_name.replace(' ','_').replace('&','_').replace(':', '_').replace('：', '_')

    def get_output_name(self):
        output_dir = get_output_path()
        output_path = output_dir if output_dir.endswith('\\') else output_dir + '\\'
        return f'{output_path}{self.video_name}.mp4'

    def get_ts_dir_path(self):
        return f'{self.base_dir}\\tmp\{self.video_id}\\'

    def get_video_id(self):
        re_res = re.findall('/(\d+)\.m3u8*', self.m3u8_url)
        return re_res[0]

    def check_path(self):
        """
        检查ts文件夹是否存在
        :return:
        """
        if not os.path.exists(self.ts_dir):
            os.mkdir(self.ts_dir)

    def check_output_exit(self):
        """
        检查输出结果文件是否存在
        :return:
        """
        if os.path.exists(self.output_name):
            log.warning(f'文件 “{self.video_name}” 已存在！')
            return False
        else:
            return True

    def check_m3u8_url(self):
        """
        检查是否是m3u8链接
        :return:
        """
        if self.m3u8_url.find('m3u8') != -1:
            return True
        else:
            log.warning(f'文件 “{self.video_name}” {self.m3u8_url} 链接格式不正确！')
            return False

    def pre_check(self):
        """
        True: 没有问题
        False: 有问题
        :return:
        """
        return  self.check_m3u8_url() & self.check_output_exit()

    def transform(self, order):
        os.system(order)

    @classmethod
    @retry(stop_max_attempt_number=5)
    def get_content(self, url):
        return requests.get(url=url, headers=headers, timeout=30).content

    def log_succ(self, video_name):
        pass

    def get_ts_file(self, ts_id):
        ts_file = self.ts_dir + ts_id + '.ts'
        if not os.path.exists(ts_file):
            url = self.ts_url + ts_id + '.ts'
            content = self.get_content(url)
            with open(ts_file, 'wb') as f:
                f.write(content)

    def worker(self):
        while True:
            with downloaderlock:
                try:
                    ts_id = ts_ids.pop()
                except IndexError:
                    break
            self.get_ts_file(ts_id)

    def run(self):
        log.info(f'Start download {self.video_name} {self.m3u8_url}')
        self.check_path()
        m3u8_file_str = fr'{self.base_dir}\tmp\{self.video_id}\download.m3u8'
        if not os.path.exists(m3u8_file_str):
            m3u8_content = requests.get(self.m3u8_url, headers=headers).text
            with open(m3u8_file_str, 'w') as m3u8_file:
                m3u8_file.write(m3u8_content)
        global ts_ids
        with open(m3u8_file_str, 'r') as m3u8_file:
            ts_ids = []
            for line in m3u8_file:
                if '#' not in line:
                    ts_id = line.replace('.ts\n', '')
                    ts_ids.append(ts_id)
        th_list = []
        ts_ids_copy = copy.copy(ts_ids)
        global downloaderlock
        downloaderlock = threading.Lock()
        for _ in range(int(get_th_number())):
            th = threading.Thread(target=self.worker)
            th.start()
            th_list.append(th)
        for th in th_list:
            th.join()
        ts_ids_len = len(ts_ids_copy)
        files = os.listdir(self.ts_dir)
        ts_file_count = 0
        ts_files = []
        for file in files:
            if file[0].isdigit():
                ts_file_count += 1
                ts_files.append(file)
        assert ts_ids_len == ts_file_count
        start = 0
        end = 50
        ts_files = sorted(os.listdir(self.ts_dir))
        merge_count = 0
        while start < ts_ids_len:
            split = ts_files[start:end]
            ts_files_str = ''
            for ts in split:
                ts_files_str += self.ts_dir + ts + '|'
            merge_name = fr'{self.base_dir}\tmp\{self.video_id}\merge{str(merge_count)}.ts'
            order_str = f'ffmpeg -i \"concat:{ts_files_str}\"  -c copy {merge_name} -y'
            # log.info(f'Merge viedeo {self.video_name} {str(merge_count)}')
            merge_count += 1
            self.transform(order_str)
            start += 50
            end += 50
        merge_files = ''
        if merge_count > 0:
            for merge_id in range(merge_count):
                merge_files += fr'{self.base_dir}\tmp\{self.video_id}\merge{merge_id}.ts|'
        else:
            merge_files += fr'{self.base_dir}\tmp\{self.video_id}\merge0.ts'
        order_str = f'ffmpeg -i \"concat:{merge_files}\"  -c copy {self.output_name} -y'
        log.info(f'Out put video {self.video_name}')
        self.transform(order_str)