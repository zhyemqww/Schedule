#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : zhyemqww
# @Time     : 2025/1/6 19:19
# @File     : Schedule
# @Project  : Schedule
# @Desc     :
import os
import sys

from PySide6.QtWidgets import QApplication

from main_window import MainWindow


os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
os.environ["QT_SCALE_FACTOR"] = "Auto"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())