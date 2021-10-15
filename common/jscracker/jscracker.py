import execjs

class Cracker(object):
    def __init__(self):
        super().__init__()
        self.ctx = self.get_ctx()

    def get_ctx(self):
        js = self.get_js()
        return execjs.compile(js)

    def get_js(self):
        with open("./common/jscracker/m2.js", "r") as f:
            return f.read()

    def crack(self, code):
        return self.ctx.call('strencode2',code)