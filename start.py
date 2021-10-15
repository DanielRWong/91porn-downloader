# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication

from ui.ui import MainWindow


def run():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()