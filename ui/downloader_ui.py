# -*- coding: utf-8 -*-

import os
import shutil
from functools import partial

from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QDialog

from common.rewriter import Rewriter
from utils.path import make_path
from common.multi_th_downloader import download_multi_thread
from common.extracter import extrcat_url
from ui.mainwindow import Ui_MainWindow
from ui.dialog1 import Ui_Dialog as Ui_Dialog1
from ui.dialog2 import Ui_Dialog as Ui_Dialog2
from ui.dialog3 import Ui_Dialog as Ui_Dialog3
from ui.dialog4 import Ui_Dialog as Ui_Dialog4
from ui.dialog5 import Ui_Dialog as Ui_Dialog5
# from ui.dialog6 import Ui_Dialog as Ui_Dialog6
from config.config import th_number,output_path


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("./ui/icon.png"))
        self.pushButton.clicked.connect(self.onclick_direct_download)
        self.pushButton_2.clicked.connect(self.onclick_setting)
        self.pushButton_3.clicked.connect(self.onclick_part_download)
        self.pushButton_4.clicked.connect(self.onclick_clean_cache)
        self.pushButton_5.clicked.connect(self.onclick_help)
        self.pushButton_6.clicked.connect(self.onclick_exit)

    def onclick_setting(self):
        dialog = Dialog4(self)
        dialog.lineEdit.setText(str(th_number))
        dialog.lineEdit_2.setText(output_path)
        dialog.show()

    def onclick_clean_cache(self):
        tmp_dirs = os.listdir("./tmp/")
        base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        for dir in tmp_dirs:
            dir_path = os.path.join(base_path+"/tmp/", dir)
            shutil.rmtree(dir_path)
        dialog = Dialog5(self)
        dialog.show()

    def onclick_direct_download(self):
        # prompt = Dialog6(self)
        # prompt.show()
        input = self.textEdit.toPlainText()
        m3u8_list = extrcat_url(input)
        download_multi_thread(m3u8_list)
        # prompt.close()
        dialog = Dialog3(self)
        dialog.show()

    def onclick_help(self):
        dialog = Dialog2(self)
        dialog.show()

    def onclick_exit(self):
        self.close()

    def onclick_part_download(self):
        input = self.textEdit.toPlainText()
        m3u8_list = extrcat_url(input)
        dialog = Dialog1(parent=self, m3u8_list=m3u8_list)
        dialog.show()


class Dialog1(QDialog, Ui_Dialog1):
    def __init__(self, m3u8_list, parent=None):
        super(Dialog1, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("./ui/icon.png"))
        self.pushButton.clicked.connect(partial(self.start_download, m3u8_list))
        # self.setWindowFlags(Qt.FramelessWindowHint)

    def start_download(self, m3u8_list):
        self.close()
        # prompt = Dialog6(self)
        # prompt.show()
        download_multi_thread(m3u8_list)
        # prompt.close()
        dialog = Dialog3(self)
        dialog.show()


class Dialog2(QDialog, Ui_Dialog2):
    def __init__(self, parent=None):
        super(Dialog2, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("./ui/icon.png"))
        self.pushButton.clicked.connect(self.close)


class Dialog3(QDialog, Ui_Dialog3):
    def __init__(self, parent=None):
        super(Dialog3, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("./ui/icon.png"))
        self.pushButton.clicked.connect(self.close)


class Dialog4(QDialog, Ui_Dialog4):
    def __init__(self, parent=None):
        super(Dialog4, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("./ui/icon.png"))
        self.pushButton.clicked.connect(self.change_settings)
        self.pushButton_2.clicked.connect(self.close)

    def change_settings(self):
        new_th_number = self.lineEdit.text()
        new_output_path = self.lineEdit_2.text()
        global th_number,output_path
        if new_th_number != th_number:
            th_number_re1 = "(th_number =) \d+"
            th_number_re2 = "\\1 " + new_th_number
            Rewriter.rewrite_config("./config/config.py",th_number_re1, th_number_re2)
            th_number = new_th_number
        if new_output_path != output_path:
            output_path_re1 = "(output_path =) '\w:.*'"
            output_path_re2 = "\\1 '" + new_output_path.replace('\\','/') + "'"
            Rewriter.rewrite_config("./config/config.py", output_path_re1, output_path_re2)
            output_path = new_output_path
            make_path(new_output_path)
        self.close()


class Dialog5(QDialog, Ui_Dialog5):
    def __init__(self, parent=None):
        super(Dialog5, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("./ui/icon.png"))
        self.pushButton.clicked.connect(self.close)


# class Dialog6(QDialog, Ui_Dialog6):
#     def __init__(self, parent=None):
#         super(Dialog6, self).__init__(parent)
#         self.setupUi(self)
#         self.setWindowIcon(QtGui.QIcon("./ui/icon.png"))
        # self.setWindowFlags(Qt.FramelessWindowHint)
