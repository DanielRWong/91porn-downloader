# -*- coding: utf-8 -*-

import re

class Rewriter(object):
    """
    重写配置文件
    """
    @classmethod
    def rewrite_config(cls, config_file, old_config, new_config):
        with open(config_file, 'r+', encoding="utf-8") as f:
            old = f.read()
            f.seek(0)
            new = re.sub(old_config, new_config, old)
            f.write(new)