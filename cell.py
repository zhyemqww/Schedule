#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : zhyemqww
# @Time     : 2025/1/7 9:12
# @File     : cell
# @Project  : Schedule
# @Desc     :
import pandas as pd
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QHBoxLayout
from qfluentwidgets import LineEdit, RoundMenu, Action

from path_utils import PathUtils


class CellComponents(LineEdit):

    COLOR_MAP = {
        "Reset": "rgba(255, 255, 255, 0.7)",
        "This Week": "rgba(237, 125, 49, 0.7)",
        "Next Week": "rgba(255, 217, 102, 0.7)",
        "Week After Next": "rgba(197, 224, 180, 0.7)",
        "Missing": "rgba(207, 213, 234, 0.7)",
        "Skip": "rgba(68, 114, 196, 0.7)",
        "Finished": "rgba(65, 200, 40, 0.7)",

        "Reset_highlight": "rgba(255, 255, 255, 1)",
        "This Week_highlight": "rgba(237, 125, 49, 1)",
        "Next Week_highlight": "rgba(255, 217, 102, 1)",
        "Week After Next_highlight": "rgba(197, 224, 180, 1)",
        "Missing_highlight": "rgba(207, 213, 234, 1)",
        "Skip_highlight": "rgba(68, 114, 196, 1)",
        "Finished_highlight": "rgba(65, 200, 40, 1)",

        "Reset_downplay": "rgba(255, 255, 255, 0)",
        "This Week_downplay": "rgba(237, 125, 49, 0)",
        "Next Week_downplay": "rgba(255, 217, 102, 0)",
        "Week After Next_downplay": "rgba(197, 224, 180, 0)",
        "Missing_downplay": "rgba(207, 213, 234, 0)",
        "Skip_downplay": "rgba(68, 114, 196, 0)",
        "Finished_downplay": "rgba(65, 200, 40, 0)",
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.state = "Reset"
        # self.setEnabled(False)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.show_context_menu(event.globalPos())
        super().mousePressEvent(event)  # 保持正常行为

    def show_context_menu(self, pos):
        # create menu
        menu = RoundMenu(self)
        this_week_action = Action(QIcon(PathUtils.get_resource_path("asset/this_week.svg")), "This Week", self)
        next_week_action = Action(QIcon(PathUtils.get_resource_path("asset/next_week.svg")), "Next Week", self)
        week_after_next_action = Action(QIcon(PathUtils.get_resource_path("asset/nn_week.svg")), "Week After Next", self)
        missing_action = Action(QIcon(PathUtils.get_resource_path("asset/miss.svg")), "Missing", self)
        skip_action = Action(QIcon(PathUtils.get_resource_path("asset/skip.svg")), "Skip", self)
        reset_action = Action(QIcon(PathUtils.get_resource_path("asset/reset.svg")), "Reset", self)
        finished_action = Action(QIcon(PathUtils.get_resource_path("asset/finished.svg")), "Finished", self)

        this_week_action.triggered.connect(self._this_week)
        next_week_action.triggered.connect(self._next_week)
        week_after_next_action.triggered.connect(self._week_after_next)
        missing_action.triggered.connect(self._missing)
        skip_action.triggered.connect(self._skip)
        reset_action.triggered.connect(self._reset)
        finished_action.triggered.connect(self._finished)

        # add action
        menu.addAction(this_week_action)
        menu.addAction(next_week_action)
        menu.addAction(week_after_next_action)
        menu.addAction(missing_action)
        menu.addAction(skip_action)
        menu.addAction(reset_action)
        menu.addAction(finished_action)

        # display menu
        menu.exec(pos)

    def _this_week(self):
        self.state = "This Week"
        self.setStyleSheet(self.set_style(self.COLOR_MAP["This Week"]))

    def _next_week(self):
        self.state = "Next Week"
        self.setStyleSheet(self.set_style(self.COLOR_MAP["Next Week"]))

    def _week_after_next(self):
        self.state = "Week After Next"
        self.setStyleSheet(self.set_style(self.COLOR_MAP["Week After Next"]))

    def _missing(self):
        self.state = "Missing"
        self.setStyleSheet(self.set_style(self.COLOR_MAP["Missing"]))

    def _skip(self):
        self.state = "Skip"
        self.setStyleSheet(self.set_style(self.COLOR_MAP["Skip"]))

    def _reset(self):
        self.state = "Reset"
        self.setStyleSheet(self.set_style(self.COLOR_MAP["Reset"]))

    def _finished(self):
        self.state = "Finished"
        self.setStyleSheet(self.set_style(self.COLOR_MAP["Finished"]))

    def highlight(self):
        """
        Highlight the cell.
        """
        if self.state == "Finished":
            self.setStyleSheet(self.set_style(self.COLOR_MAP["Finished_highlight"]))
        elif self.state == "This Week":
            self.setStyleSheet(self.set_style(self.COLOR_MAP["This Week_highlight"]))
        elif self.state == "Next Week":
            self.setStyleSheet(self.set_style(self.COLOR_MAP["Next Week_highlight"]))
        elif self.state == "Week After Next":
            self.setStyleSheet(self.set_style(self.COLOR_MAP["Week After Next_highlight"]))
        elif self.state == "Missing":
            self.setStyleSheet(self.set_style(self.COLOR_MAP["Missing_highlight"]))
        elif self.state == "Skip":
            self.setStyleSheet(self.set_style(self.COLOR_MAP["Skip_highlight"]))
        elif self.state == "Reset":
            self.setStyleSheet(self.set_style(self.COLOR_MAP["Reset_highlight"]))
        else:
            pass

    def downplay(self):
        """
        Downplay the cell.
        """
        if self.state == "Finished":
            self.setStyleSheet(self.set_style(self.COLOR_MAP["Finished_downplay"]))
        elif self.state == "This Week":
            self.setStyleSheet(self.set_style(self.COLOR_MAP["This Week_downplay"]))
        elif self.state == "Next Week":
            self.setStyleSheet(self.set_style(self.COLOR_MAP["Next Week_downplay"]))
        elif self.state == "Week After Next":
            self.setStyleSheet(self.set_style(self.COLOR_MAP["Week After Next_downplay"]))
        elif self.state == "Missing":
            self.setStyleSheet(self.set_style(self.COLOR_MAP["Missing_downplay"]))
        elif self.state == "Skip":
            self.setStyleSheet(self.set_style(self.COLOR_MAP["Skip_downplay"]))
        elif self.state == "Reset":
            self.setStyleSheet(self.set_style(self.COLOR_MAP["Reset_downplay"]))
        else:
            pass

    def recover(self):
        """
        Recover the cell.
        """
        if self.state == "Finished":
            self.setStyleSheet(self.set_style(self.COLOR_MAP["Finished"]))
        elif self.state == "This Week":
            self.setStyleSheet(self.set_style(self.COLOR_MAP["This Week"]))
        elif self.state == "Next Week":
            self.setStyleSheet(self.set_style(self.COLOR_MAP["Next Week"]))
        elif self.state == "Week After Next":
            self.setStyleSheet(self.set_style(self.COLOR_MAP["Week After Next"]))
        elif self.state == "Missing":
            self.setStyleSheet(self.set_style(self.COLOR_MAP["Missing"]))
        elif self.state == "Skip":
            self.setStyleSheet(self.set_style(self.COLOR_MAP["Skip"]))
        elif self.state == "Reset":
            self.setStyleSheet(self.set_style(self.COLOR_MAP["Reset"]))
        else:
            pass

    def set_text(self, text, state):
        self.setText(text)
        self.state = state
        self.setStyleSheet(self.set_style(CellComponents.COLOR_MAP[state]))

    @staticmethod
    def set_style(color):
        style = f"""
                LineEdit, TextEdit, PlainTextEdit, TextBrowser {{
                color: black;
                background-color: {color};
                border: 1px solid rgba(0, 0, 0, 13);
                border-bottom: 1px solid rgba(0, 0, 0, 100);
                border-radius: 5px;
                /* font: 14px "Segoe UI", "Microsoft YaHei"; */
                padding: 0px 10px;
                selection-background-color: {color};
                }}

                TextEdit,
                PlainTextEdit,
                TextBrowser {{
                    padding: 2px 3px 2px 8px;
                }}

                LineEdit:hover, TextEdit:hover, PlainTextEdit:hover, TextBrowser:hover {{
                    background-color: {color};
                    border: 1px solid rgba(0, 0, 0, 13);
                    border-bottom: 1px solid rgba(0, 0, 0, 100);
                }}

                LineEdit:focus {{
                    border-bottom: 1px solid rgba(0, 0, 0, 13);
                    background-color: {color};
                }}

                TextEdit:focus,
                PlainTextEdit:focus,
                TextBrowser:focus {{
                    border-bottom: 1px solid #009faa;
                    background-color: {color};
                }}

                LineEdit:disabled, TextEdit:disabled,
                PlainTextEdit:disabled,
                TextBrowser:disabled {{
                    color: rgba(0, 0, 0, 92);
                    background-color: {color};
                    border: 1px solid rgba(0, 0, 0, 13);
                    border-bottom: 1px solid rgba(0, 0, 0, 13);
                }}

                #lineEditButton {{
                    background-color: {color};
                    border-radius: 4px;
                    margin: 0;
                }}

                #lineEditButton:hover {{
                    background-color: {color};
                }}

                #lineEditButton:pressed {{
                    background-color: {color};
                }}
                """
        return style


class Cell(QWidget):
    def __init__(self, parent, text="", state="Reset"):
        super().__init__(parent=parent)
        self.cell = None
        self.text = text
        self.state = state
        self.setup()

    def setup(self):
        self.cell = CellComponents(self)
        layout = QHBoxLayout()
        layout.addWidget(self.cell)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(self.cell, Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

        if not pd.isna(self.text):
            self.cell.set_text(str(self.text), self.state)
        else:
            self.cell.set_text("", self.state)

    def get_lineedit_item(self):
        return self.cell
