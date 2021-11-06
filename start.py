# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication

from ui.downloader_ui import MainWindow
from utils.path import check_output_path

def run():
    check_output_path()
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()