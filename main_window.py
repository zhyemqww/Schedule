#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : zhyemqww
# @Time     : 2025/1/6 19:19
# @File     : main_window
# @Project  : Schedule
# @Desc     :
import pandas as pd
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QVBoxLayout, QHeaderView, QHBoxLayout
from qfluentwidgets import PushButton, ToggleButton, PrimaryPushButton
from qfluentwidgets.components.widgets import TableWidget

from base_frameless_window import BaseFramelessWindow
from cell import Cell
from password_window import Passwords
from path_utils import PathUtils


class MainWindow(BaseFramelessWindow):

    COLOR_MAP = {
        "Reset": "rgba(255, 255, 255, 0.7)",
        "This Week": "rgba(237, 125, 49, 0.7)",
        "Next Week": "rgba(255, 217, 102, 0.7)",
        "Week After Next": "rgba(197, 224, 180, 0.7)",
        "Missing": "rgba(207, 213, 234, 0.7)",
        "Skip": "rgba(68, 114, 196, 0.7)",
        "Finished": "rgba(65, 200, 40, 0.7)",
    }

    def __init__(self):
        super().__init__()
        self.btn_hlayout = None
        self.last_btn = None
        self.passwords = None
        self.layout = None
        self.table_widget = None
        self.hlayout = None
        self.this_button = None
        self.next_button = None
        self.week_after_next_button = None
        self.missing_button = None
        self.skip_button = None
        self.finished_button = None

        self.setWindowTitle("Schedule")
        self.setWindowIcon(QIcon(PathUtils.get_resource_path("asset/icon_1.svg")))
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.resize(800, 760)
        self.setup_ui()

    def setup_ui(self):
        table = pd.read_csv(PathUtils.get_resource_path("asset/table.csv"), header=None)
        state = pd.read_csv(PathUtils.get_resource_path("asset/state.csv"), header=None)

        self.layout = QVBoxLayout()

        self.table_widget = TableWidget(self)

        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.table_widget.setRowCount(table.shape[0])
        self.table_widget.setColumnCount(table.shape[1])

        vertical_header = [f"第{i}周" for i in range(1, table.shape[0] + 1)]
        self.table_widget.setVerticalHeaderLabels(vertical_header)
        self.table_widget.setHorizontalHeaderLabels(["" if i == 0 else f"Person {i}" for i in range(1, table.shape[1]+ 1)])

        self.table_widget.setBorderVisible(True)
        self.table_widget.setBorderRadius(8)

        # fill the table with data
        for row_index, row in table.iterrows():
            for col_index, value in enumerate(row):
                cell = Cell(self, value, state.iloc[row_index, col_index])
                self.table_widget.setCellWidget(row_index, col_index, cell)

        self.layout.addWidget(self.table_widget)

        # add buttons
        self.hlayout = QHBoxLayout()

        self.this_button = ToggleButton(self)
        self.this_button.toggled.connect(self.highlight)
        self.this_button.setText("This Week")
        self.this_button.setStyleSheet(self.set_style("This Week"))

        self.next_button = ToggleButton(self)
        self.next_button.toggled.connect(self.highlight)
        self.next_button.setText("Next Week")
        self.next_button.setStyleSheet(self.set_style("Next Week"))

        self.week_after_next_button = ToggleButton(self)
        self.week_after_next_button.toggled.connect(self.highlight)
        self.week_after_next_button.setText("Week After Next")
        self.week_after_next_button.setStyleSheet(self.set_style("Week After Next"))

        self.missing_button = ToggleButton(self)
        self.missing_button.toggled.connect(self.highlight)
        self.missing_button.setText("Missing")
        self.missing_button.setStyleSheet(self.set_style("Missing"))

        self.skip_button = ToggleButton(self)
        self.skip_button.toggled.connect(self.highlight)
        self.skip_button.setText("Skip")
        self.skip_button.setStyleSheet(self.set_style("Skip"))

        # self.reset_button = ToggleButton(self)
        # self.reset_button.toggled.connect(self.highlight)
        # self.reset_button.setText("Reset")
        # self.reset_button.setStyleSheet(self.set_style("Reset"))

        self.finished_button = ToggleButton(self)
        self.finished_button.toggled.connect(self.highlight)
        self.finished_button.setText("Finished")
        self.finished_button.setStyleSheet(self.set_style("Finished"))

        self.hlayout.addWidget(self.this_button)
        self.hlayout.addWidget(self.next_button)
        self.hlayout.addWidget(self.week_after_next_button)
        self.hlayout.addWidget(self.missing_button)
        self.hlayout.addWidget(self.skip_button)
        # self.hlayout.addWidget(self.reset_button)
        self.hlayout.addWidget(self.finished_button)

        self.layout.addLayout(self.hlayout)

        self.btn_hlayout = QHBoxLayout()
        # add save button
        save_push_button = PrimaryPushButton(self)
        save_push_button.setText("Save")
        save_push_button.clicked.connect(self.save)

        # add reset button
        reset_push_button = PushButton(self)
        reset_push_button.setText("Reset")
        reset_push_button.clicked.connect(self.reset)

        self.btn_hlayout.addWidget(reset_push_button)
        self.btn_hlayout.addWidget(save_push_button)

        self.layout.addLayout(self.btn_hlayout)

        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(20)

        self.setLayout(self.layout)

    @Slot()
    def highlight(self, is_checked):
        """
        Highlight the selected cell.
        """
        sender = self.sender()

        # only one button can be checked at a time
        if self.last_btn and self.last_btn != sender:
            self.last_btn.setChecked(False)
            self.last_btn = sender
        else:
            self.last_btn = sender

        state = sender.text()

        for cell in self.table_widget.findChildren(Cell):
            if is_checked:
                if cell.cell.state == state:
                    cell.cell.highlight()
                else:
                    cell.cell.downplay()
            else:
                cell.cell.recover()

    def set_style(self, state) -> str:

        style = f"""
            PushButton, ToolButton, ToggleButton, ToggleToolButton {{
            color: black;
            background: {self.COLOR_MAP[state]};
            border: 1px solid rgba(0, 0, 0, 0.073);
            border-bottom: 1px solid rgba(0, 0, 0, 0.183);
            border-radius: 5px;
            /* font: 14px 'Segoe UI', 'Microsoft YaHei'; */
            padding: 5px 12px 6px 12px;
            outline: none;
            }}
            
            PushButton:pressed, ToolButton:pressed, ToggleButton:pressed, ToggleToolButton:pressed {{
            color: rgba(0, 0, 0, 0.63);
            background: rgba(249, 249, 249, 0.3);
            border-bottom: 1px solid rgba(0, 0, 0, 0.073);
            }}
            ToggleButton:checked,
            ToggleToolButton:checked {{
                color: {self.COLOR_MAP[state]};
                background-color: white;
            }}
        """
        return style

    def save(self):
        """
        Save the state of the table.
        """
        data = pd.DataFrame(self.get_state())
        self.passwords = Passwords(data)
        self.passwords.closed.connect(self.close)  # Connect the child window close signal to the main window close
        self.passwords.show()

    def reset(self):
        """
        Reset the state of the table.
        """
        for cell in self.table_widget.findChildren(Cell):
            cell.cell.state = "Reset"
            cell.cell.recover()

    def get_state(self) -> list:
        """Get the state of the table."""
        state = []
        for row in range(self.table_widget.rowCount()):
            row_state = []
            for col in range(self.table_widget.columnCount()):
                cell = self.table_widget.cellWidget(row, col)
                row_state.append(cell.cell.state)
            state.append(row_state)
        return state
