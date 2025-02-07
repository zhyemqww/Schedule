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
from PySide6.QtWidgets import QVBoxLayout, QHeaderView, QHBoxLayout, QTableWidget
from qfluentwidgets import PushButton, ToggleButton, PrimaryPushButton, FluentIcon
from qfluentwidgets.components.widgets import TableWidget

from src.base_frameless_window import BaseFramelessWindow
from src.cell import Cell
from src.password_window import Passwords
from src.path_utils import PathUtils
from src.style import StyleMixIn


class MainWindow(StyleMixIn, BaseFramelessWindow):

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
        self.incomplete_button = None
        self.skipped_button = None
        self.finished_button = None

        self.back_data_dict = {}
        self.back_data = None
        self.index = 0

        self.setWindowTitle("Schedule v1.0.1")
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

        vertical_header = [f"Week {i}" for i in range(1, table.shape[0] + 1)]
        self.table_widget.setVerticalHeaderLabels(vertical_header)
        self.table_widget.setHorizontalHeaderLabels(["" if i == 0 else f"Person {i}" for i in range(1, table.shape[1]+ 1)])

        self.table_widget.setBorderVisible(True)
        self.table_widget.setBorderRadius(8)
        self.table_widget.setSelectionMode(QTableWidget.SelectionMode.NoSelection)

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
        self.this_button.setStyleSheet(self.generate_default_style("This Week"))

        self.next_button = ToggleButton(self)
        self.next_button.toggled.connect(self.highlight)
        self.next_button.setText("Next Week")
        self.next_button.setStyleSheet(self.generate_default_style("Next Week"))

        self.week_after_next_button = ToggleButton(self)
        self.week_after_next_button.toggled.connect(self.highlight)
        self.week_after_next_button.setText("Week After Next")
        self.week_after_next_button.setStyleSheet(self.generate_default_style("Week After Next"))

        self.incomplete_button = ToggleButton(self)
        self.incomplete_button.toggled.connect(self.highlight)
        self.incomplete_button.setText("Incomplete")
        self.incomplete_button.setStyleSheet(self.generate_default_style("Incomplete"))

        self.skipped_button = ToggleButton(self)
        self.skipped_button.toggled.connect(self.highlight)
        self.skipped_button.setText("Skipped")
        self.skipped_button.setStyleSheet(self.generate_default_style("Skipped"))

        # self.reset_button = ToggleButton(self)
        # self.reset_button.toggled.connect(self.highlight)
        # self.reset_button.setText("Reset")
        # self.reset_button.setStyleSheet(self.set_style("Reset"))

        self.finished_button = ToggleButton(self)
        self.finished_button.toggled.connect(self.highlight)
        self.finished_button.setText("Finished")
        self.finished_button.setStyleSheet(self.generate_default_style("Finished"))

        self.hlayout.addWidget(self.this_button)
        self.hlayout.addWidget(self.next_button)
        self.hlayout.addWidget(self.week_after_next_button)
        self.hlayout.addWidget(self.incomplete_button)
        self.hlayout.addWidget(self.skipped_button)
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

        # add next button
        next_push_button = PushButton(self)
        next_push_button.setText("Next")
        next_push_button.setIcon(FluentIcon.RIGHT_ARROW)
        next_push_button.clicked.connect(self.next)

        # add back button
        back_push_button = PushButton(self)
        back_push_button.setText("Back")
        back_push_button.setIcon(FluentIcon.LEFT_ARROW)
        back_push_button.clicked.connect(self.back)

        self.btn_hlayout.addWidget(reset_push_button)
        self.btn_hlayout.addWidget(back_push_button)
        self.btn_hlayout.addWidget(next_push_button)
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

        for btn in [self.this_button, self.next_button, self.week_after_next_button, self.incomplete_button, self.skipped_button, self.finished_button]:
            if btn != sender:
                state = btn.text()
                if sender.isChecked():
                    style = self.generate_downplay_style(state)
                    btn.setStyleSheet(style)
                else:
                    style = self.generate_default_style(state)
                    btn.setStyleSheet(style)

    def generate_default_style(self, state) -> str:

        state_highlight = f"{state}_highlight"
        state_downplay = f"{state}_downplay"

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
            background: {self.COLOR_MAP[state_downplay]};
            border-bottom: 1px solid rgba(0, 0, 0, 0.073);
            }}
            ToggleButton:checked,
            ToggleToolButton:checked {{
                color: black;
                background-color: {self.COLOR_MAP[state_highlight]};
            }}
        """
        return style

    def generate_downplay_style(self, state) -> str:

        state_highlight = f"{state}_highlight"
        state_downplay = f"{state}_downplay"

        style = f"""
            PushButton, ToolButton, ToggleButton, ToggleToolButton {{
            color: black;
            background: {self.COLOR_MAP[state_downplay]};
            border: 1px solid rgba(0, 0, 0, 0.073);
            border-bottom: 1px solid rgba(0, 0, 0, 0.183);
            border-radius: 5px;
            /* font: 14px 'Segoe UI', 'Microsoft YaHei'; */
            padding: 5px 12px 6px 12px;
            outline: none;
            }}

            PushButton:pressed, ToolButton:pressed, ToggleButton:pressed, ToggleToolButton:pressed {{
            color: rgba(0, 0, 0, 0.63);
            background: {self.COLOR_MAP[state_downplay]};
            border-bottom: 1px solid rgba(0, 0, 0, 0.073);
            }}
            ToggleButton:checked,
            ToggleToolButton:checked {{
                color: black;
                background-color: {self.COLOR_MAP[state_highlight]};
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

    def next(self):
        """
        Update the state of the table.
        """
        # get the current state and find the cells that need to be updated
        finishing = []
        next_this_week = []
        next_next_week = []
        next_week_after_next = []
        data = pd.DataFrame(self.get_state())

        self.back_data = data.copy()
        self.back_data_dict[self.index] = self.back_data
        self.index += 1

        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data.iloc[row, col] == "This Week":
                    finishing.append((row, col))
                elif data.iloc[row, col] == "Next Week":
                    next_this_week.append((row, col))
                elif data.iloc[row, col] == "Week After Next":
                    next_next_week.append((row, col))
                    if row + 1 < data.shape[0]:
                        next_week_after_next.append((row+1, col))

        # update the state
        next_data = data.copy()
        for row, col in finishing:
            next_data.iloc[row, col] = "Finished"
        for row, col in next_this_week:
            next_data.iloc[row, col] = "This Week"
        for row, col in next_next_week:
            next_data.iloc[row, col] = "Next Week"
        for row, col in next_week_after_next:
            next_data.iloc[row, col] = "Week After Next"

        # update the table
        for row in range(self.table_widget.rowCount()):
            for col in range(self.table_widget.columnCount()):
                cell = self.table_widget.cellWidget(row, col)
                if not pd.isna(cell.text):
                    cell.cell.state = next_data.iloc[row, col]
                    cell.cell.recover()

    def back(self):
        # update the table
        if self.index != 0:
            back_data = self.back_data_dict[self.index - 1]
            self.index -= 1
            for row in range(self.table_widget.rowCount()):
                for col in range(self.table_widget.columnCount()):
                    cell = self.table_widget.cellWidget(row, col)
                    if not pd.isna(cell.text):
                        cell.cell.state = back_data.iloc[row, col]
                        cell.cell.recover()
