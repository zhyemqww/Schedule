#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : zhyemqww
# @Time     : 2024/9/15 14:43
# @File     : base_frameless_window
# @Project  : PELSA_Decipher_1.0
# @Desc     :
from PySide6.QtGui import QScreen
from PySide6.QtWidgets import QApplication
from qframelesswindow import StandardTitleBar
from qframelesswindow import FramelessWindow


class BaseFramelessWindow(FramelessWindow):
    """
    A base class for creating frameless windows with a custom title bar.
    """

    def __init__(self, parent=None, top_margin=30):
        """
        Initialize the BaseFramelessWindow.

        Args:
            parent (QObject, optional): The parent object. Defaults to None.
            top_margin (int, optional): The top margin for the window content. Defaults to 30.
        """
        super().__init__(parent=parent)
        # Set the top margin
        self.setContentsMargins(0, top_margin, 0, 0)
        # Add the custom title bar
        self.setTitleBar(StandardTitleBar(self))  # Initializes the custom title bar
        self.titleBar.raise_()  # Place the title bar at the top level

        # Set the style sheet
        self.setStyleSheet("""
        QWidget {
            background: rgb(249, 249, 249);
        }
        CaptionLabel {
            background: rgb(249, 249, 249);
        }
        BodyLabel {
            background: rgb(253, 253, 253);
        }
        StrongBodyLabel {
            background: rgb(253, 253, 253);
        }
        SubtitleLabel {
            background: rgb(253, 253, 253);
        }
        CheckBox {
            background: rgb(253, 253, 253);
        }        
        """)

    def showEvent(self, event):
        """
        Override the showEvent method to center the window when it is shown.
        """
        super().showEvent(event)
        self.center_window()

    def center_window(self):
        """
        Center the window on the screen.
        """
        # move window frame to center the window
        main_screen = QScreen.availableGeometry(QApplication.primaryScreen())
        x = (main_screen.width() - self.width()) // 2
        y = (main_screen.height() - self.height()) // 2
        self.move(x, y)
