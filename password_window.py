#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : zhyemqww
# @Time     : 2025/1/9 16:28
# @File     : password_window
# @Project  : Schedule
# @Desc     :
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout
from qfluentwidgets import BodyLabel, PasswordLineEdit, PushButton

from base_frameless_window import BaseFramelessWindow
from path_utils import PathUtils


class Passwords(BaseFramelessWindow):

    closed = Signal()

    def __init__(self, data=None):
        super().__init__()

        self.data = data
        self.layout = None
        self.hlayout = None
        self.passwords = None
        self.passwords_lineEdit = None
        self.save_push_button = None

        self.setWindowTitle("Verification Password")
        self.setWindowIcon(QIcon(PathUtils.get_resource_path("asset/icon_1.svg")))
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.resize(400, 200)
        self.setup_ui()


    def setup_ui(self):
        self.layout = QVBoxLayout()

        self.hlayout = QHBoxLayout()
        self.passwords = BodyLabel(self)
        self.passwords.setText("Password: ")
        self.hlayout.addWidget(self.passwords)

        self.passwords_lineEdit = PasswordLineEdit(self)
        self.hlayout.addWidget(self.passwords_lineEdit)

        self.layout.addLayout(self.hlayout)

        self.save_push_button = PushButton(self)
        self.save_push_button.setText("Save")
        self.save_push_button.clicked.connect(self.save)

        self.layout.addWidget(self.save_push_button)

        self.setLayout(self.layout)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

    def save(self):
        passwords = self.passwords_lineEdit.text()
        if passwords == "Dicp1809":
            self.data.to_csv(PathUtils.get_resource_path("asset/state.csv"), header=None, index=None)
            self.closed.emit()  # 发出关闭信号
            self.close()

    def closeEvent(self, event):
        super().closeEvent(event)
