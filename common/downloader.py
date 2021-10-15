# -*- coding: utf-8 -*-

import re
import os
import requests
from retrying import retry

from config.config import *
from utils.log import logger

log = logger()

class Downloader(object):
    def __init__(self, m3u8_url, video_name):
        self.m3u8_url = m3u8_url
        self.video_name = self.get_video_name(video_name)
        self.video_id = self.get_video_id()  # 91porn
        self.base_dir = self.get_base_dir()
        self.ts_dir = self.get_ts_dir_path()  # "D:\py\m3u8\91porn-downloader\tmp\66666\"
        self.output_name = self.get_output_name()

    def get_base_dir(self):
        return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    def get_video_name(self, video_name):
        return video_name.replace(" ","_")

    def get_output_name(self):
        global output_path
        output_path = (output_path if output_path.endswith("\\") else output_path + "\\")
        return f"{output_path}{self.video_name}.mp4"

    def get_ts_dir_path(self):
        return f"{self.base_dir}\\tmp\{self.video_id}\\"

    def get_video_id(self):
        re_res = re.findall("/(\d+)\.m3u8*", self.m3u8_url)
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
        return os.path.exists(self.output_name)

    def check_m3u8_url(self):
        """
        检查是否是m3u8链接
        :return:
        """
        return self.m3u8_url.find("m3u8") != -1

    def pre_check(self):
        return  self.check_m3u8_url() & self.check_output_exit()

    def transform(self, order):
        os.system(order)

    @classmethod
    @retry(stop_max_attempt_number=5)
    def get_content(self, url):
        return requests.get(url=url, headers=headers, timeout=30).content

    def log_succ(self, video_name):
        pass

    def run(self):
        log.info(f"Start download {self.video_name} {self.m3u8_url}")
        self.check_path()
        m3u8_file_str = fr"{self.base_dir}\tmp\{self.video_id}\download.m3u8"
        if not os.path.exists(m3u8_file_str):
            m3u8_content = requests.get(self.m3u8_url, headers=headers).text
            with open(m3u8_file_str, 'w') as m3u8_file:
                m3u8_file.write(m3u8_content)
        with open(m3u8_file_str, 'r') as m3u8_file:
            ts_ids = []
            for line in m3u8_file:
                if "#" not in line:
                    ts_id = line.replace('.ts\n', '')
                    ts_ids.append(ts_id)
        files = ""
        count = 0
        merge = False
        merge_id = 0
        merge_name_list = []
        for ts_id in ts_ids:
            ts_file = self.ts_dir + ts_id + ".ts"
            if not os.path.exists(ts_file):
                url = base_url + self.video_id + "/" + ts_id + ".ts"
                content = self.get_content(url)
                with open(ts_file, "wb") as f:
                    f.write(content)
            files += ts_file + "|"
            count += 1
            if count > 49:
                merge = True
                merge_name = fr"{self.base_dir}\tmp\{self.video_id}\merge{str(merge_id)}.ts"
                merge_name_list.append(merge_name)
                order_str = f"ffmpeg -i \"concat:{files}\"  -c copy {merge_name} -y"
                log.info(f"Merge viedeo {self.video_name} {str(merge_id)}")
                self.transform(order_str)
                count = 0
                files = ""
                merge_id += 1
        if merge == False:
            log.info(f"Out put video {self.video_name}")
            merge_order = f"ffmpeg -i \"concat:{files}\" -c copy {self.output_name}"
        else:
            if files != "":
                merge_name = fr"{self.base_dir}\tmp\{self.video_id}\merge{str(merge_id)}.ts"
                merge_name_list.append(merge_name)
                order_str = f"ffmpeg -i \"concat:{files}\" -c copy {merge_name} -y"
                log.info(f"Merge viedeo {self.video_name} {str(merge_id)}")
                self.transform(order_str)
            merge_name_str = "|".join(merge_name_list)
            log.info(f"Out put video {self.video_name}")
            merge_order = f"ffmpeg -i \"concat:{merge_name_str}\" -c copy {self.output_name}"
        self.transform(merge_order)

    def __del__(self):
        try:
            # shutil.rmtree(self.ts_dir)
            pass
        except Exception as e:
            print(e)




