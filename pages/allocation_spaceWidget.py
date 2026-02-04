from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                               QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QLineEdit)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
import pandas as pd
import os

class AllocationSpaceWidget(QWidget):
    back_to_dashboard = Signal()
    logout = Signal()
    licensee_selected = Signal(dict)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        header = self.create_header()
        content = self.create_content()
        
        main_layout.addWidget(header)
        main_layout.addWidget(content)
        
        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #1a1a1a;")
        
    def create_header(self):
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: #2b2b2b;
                border-bottom: 1px solid #444;
            }
        """)
        header.setFixedHeight(80)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 0, 20, 0)
        
        back_btn = QPushButton("← Back to Dashboard")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                padding: 10px;
                text-align: left;
                font-size: 14px;
            }
            QPushButton:hover {
                color: #4a9eff;
            }
        """)
        back_btn.clicked.connect(self.back_to_dashboard.emit)
        
        title = QLabel("Allocation Workspace")
        title.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
        """)
        
        center_title = QLabel("Durham Allocation Office")
        center_title.setStyleSheet("""
            color: white;
            font-size: 20px;
            font-weight: bold;
        """)
        center_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #3a3a3a;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
        """)
        logout_btn.clicked.connect(self.logout.emit)
        
        left_section = QHBoxLayout()
        left_section.addWidget(back_btn)
        left_section.addWidget(title)
        left_section.addStretch()
        
        layout.addLayout(left_section, 2)
        layout.addWidget(center_title, 3)
        layout.addWidget(logout_btn, 1)
        
        header.setLayout(layout)
        return header
        
    def create_content(self):
        content = QFrame()
        content.setStyleSheet("background-color: #1a1a1a;")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        page_title = QLabel("Prisoner Allocation")
        page_title.setStyleSheet("""
            color: white;
            font-size: 36px;
            font-weight: bold;
        """)
        
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        search_label.setStyleSheet("color: white; font-size: 14px;")
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter any column to search")
        self.search_input.setMinimumHeight(35)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #3a3a3a;
                padding: 5px;
                border-radius: 4px;
            }
        """)
        
        self.search_btn = QPushButton("Search")
        self.search_btn.setMinimumHeight(35)
        self.search_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a9eff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #6bb3ff;
            }
        """)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setMinimumHeight(35)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #4d4d4d;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #5d5d5d;
            }
        """)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)
        search_layout.addWidget(self.refresh_btn)
        
        instruction_label = QLabel("Select a licensee from the table below:")
        instruction_label.setStyleSheet("""
            color: white;
            font-size: 16px;
            margin-top: 10px;
        """)
        
        self.licensee_table = QTableWidget()
        self.licensee_table.setStyleSheet("""
            QTableWidget {
                background-color: #3d3d3d;
                color: white;
                gridline-color: #555555;
                border: 1px solid #555555;
            }
            QHeaderView::section {
                background-color: #4d4d4d;
                color: white;
                padding: 5px;
                border: 1px solid #555555;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #4a9eff;
            }
        """)
        self.licensee_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.licensee_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.licensee_table.itemSelectionChanged.connect(self.on_licensee_selected)
        
        self.selected_info_label = QLabel("No licensee selected")
        self.selected_info_label.setStyleSheet("""
            color: white;
            font-size: 18px;
            font-weight: bold;
            margin-top: 20px;
        """)
        
        ranked_label = QLabel("Ranked RHUs:")
        ranked_label.setStyleSheet("""
            color: white;
            font-size: 16px;
            font-weight: bold;
            margin-top: 10px;
        """)
        
        self.rhu_list_widget = QWidget()
        self.rhu_list_layout = QVBoxLayout()
        self.rhu_list_layout.setSpacing(20)
        self.rhu_list_widget.setLayout(self.rhu_list_layout)
        
        layout.addWidget(page_title)
        layout.addLayout(search_layout)
        layout.addWidget(instruction_label)
        layout.addWidget(self.licensee_table)
        layout.addWidget(self.selected_info_label)
        layout.addWidget(ranked_label)
        layout.addWidget(self.rhu_list_widget)
        layout.addStretch()
        
        content.setLayout(layout)
        return content
    
    def populate_table(self, data):
        if data.empty:
            self.licensee_table.setRowCount(0)
            self.licensee_table.setColumnCount(0)
            return
        
        self.licensee_table.setRowCount(len(data))
        self.licensee_table.setColumnCount(len(data.columns))
        self.licensee_table.setHorizontalHeaderLabels(data.columns.tolist())
        
        for row_idx, row in data.iterrows():
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.licensee_table.setItem(row_idx, col_idx, item)
        
        self.licensee_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    
    def on_licensee_selected(self):
        selected_row = self.licensee_table.currentRow()
        if selected_row < 0:
            return
        
        licensee_data = {}
        
        for col in range(self.licensee_table.columnCount()):
            header = self.licensee_table.horizontalHeaderItem(col).text()
            item = self.licensee_table.item(selected_row, col)
            if item:
                licensee_data[header] = item.text()
        
        name = licensee_data.get('Name', 'Unknown')
        release = licensee_data.get('Release_Date', 'Unknown')
        self.selected_info_label.setText(f"Selected: {name} - Release: {release}")
        
        self.licensee_selected.emit(licensee_data)
    
    def create_rhu_card(self, rank, rhu_data, available_capacity, conflicts, conflict_level, is_full=False):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #2b2b2b;
                border: 1px solid #3a3a3a;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        rank_name = QLabel(f"{rank}. {rhu_data['name']}")
        rank_name.setStyleSheet("""
            color: white;
            font-size: 18px;
            font-weight: bold;
        """)
        
        capacity_text = f"FULL ({rhu_data['current_allocation']}/{rhu_data['capacity']})" if is_full else f"{available_capacity}/{rhu_data['capacity']} Available"
        cost_capacity = QLabel(f"Cost: £{rhu_data['cost_per_day']}/day | Capacity: {capacity_text}")
        cost_capacity.setStyleSheet("""
            color: white;
            font-size: 14px;
        """)
        
        if conflicts:
            conflict_icon = "⚠⚠" if conflict_level == "major" else "⚠"
            conflict_count = len(conflicts)
            conflict_type = "major" if conflict_level == "major" else "minor"
            conflict_text = f"Conflicts: {conflict_icon} {conflict_count} {conflict_type} ({', '.join(conflicts)})"
            conflicts_label = QLabel(conflict_text)
            conflicts_label.setStyleSheet("""
                color: #ff9500;
                font-size: 14px;
            """)
            conflicts_label.setWordWrap(True)
        else:
            conflicts_label = QLabel("Conflicts: ✓ None")
            conflicts_label.setStyleSheet("""
                color: #4cd964;
                font-size: 14px;
            """)
        
        layout.addWidget(rank_name)
        layout.addWidget(cost_capacity)
        layout.addWidget(conflicts_label)
        
        card.setLayout(layout)
        return card
    
    def display_ranked_rhus(self, ranked_rhus):
        while self.rhu_list_layout.count():
            child = self.rhu_list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        for item in ranked_rhus[:3]:
            card = self.create_rhu_card(
                item['rank'],
                item['rhu'],
                item['available'],
                item['conflicts'],
                item['level'],
                item['is_full']
            )
            self.rhu_list_layout.addWidget(card)