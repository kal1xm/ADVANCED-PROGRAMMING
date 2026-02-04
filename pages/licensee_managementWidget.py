#kallumleew24023993
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView)
from PySide6.QtCore import Signal
from PySide6.QtGui import QFont
from pages.licensee_management import licensee_management

class LicenseeManagementWidget(QWidget):
    back_to_dashboard = Signal()
    logout = Signal()
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.licensee_mgmt = licensee_management()
        self.licenseeUI(self)


    def licenseeUI(self, *args):
            main_layout = QVBoxLayout()
            main_layout.setContentsMargins(20, 20, 20, 20)
            
           
            header_layout = QHBoxLayout()
            title = QLabel("Licensee Management")
            title_font = QFont()
            title_font.setPointSize(18)
            title_font.setBold(True)
            title.setFont(title_font)
            title.setStyleSheet("color: white;")
            header_layout.addWidget(title)
            
            logout_btn = QPushButton("Logout")
            logout_btn.setMaximumWidth(120)
            logout_btn.setMinimumHeight(40)
            logout_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4d4d4d;
                    color: white;
                    border: none;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #5d5d5d;
                }
            """)
            logout_btn.clicked.connect(self.logout.emit)
            header_layout.addWidget(logout_btn)
            main_layout.addLayout(header_layout)
            
          
            search_layout = QHBoxLayout()
            search_label = QLabel("Search:")
            search_label.setStyleSheet("color: white; font-size: 14px;")
            self.search_input = QLineEdit()
            self.search_input.setPlaceholderText("Enter any column to search")
            self.search_input.setMinimumHeight(35)
            self.search_input.textChanged.connect(self.search_licensees)
            
            search_btn = QPushButton("Search")
            search_btn.setMinimumHeight(35)
            search_btn.clicked.connect(self.search_licensees)
            
            search_layout.addWidget(search_label)
            search_layout.addWidget(self.search_input)
            search_layout.addWidget(search_btn)
            main_layout.addLayout(search_layout)
            
           
            self.table = QTableWidget()
            self.table.setStyleSheet("""
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
            """)
            main_layout.addWidget(self.table)
            
           
            button_layout = QHBoxLayout()
            
            add_btn = QPushButton("Add Licensee")
            add_btn.setMinimumHeight(40)
            add_btn.clicked.connect(self.add_licensee)
            
            remove_btn = QPushButton("Remove Selected")
            remove_btn.setMinimumHeight(40)
            remove_btn.clicked.connect(self.remove_licensee)
            
            refresh_btn = QPushButton("Refresh")
            refresh_btn.setMinimumHeight(40)
            refresh_btn.clicked.connect(self.refreshdata)
            
            button_layout.addWidget(add_btn)
            button_layout.addWidget(remove_btn)
            button_layout.addWidget(refresh_btn)
            button_layout.addStretch()
            
            main_layout.addLayout(button_layout)
            
            self.setStyleSheet("background-color: #2d2d2d;")
            self.setLayout(main_layout)
            
          
            

    def remove_licensee(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "none added", "Select a licensee to remove")
            return
        prison_id = self.table.item(selected_row, 0).text()
        reply = QMessageBox.question(self, "Confirm",
                                    f"Are you sure you want to remove licensee {prison_id}?", QMessageBox.Yes | QMessageBox.No)

    def refreshdata(self):
        data = self.licensee_mgmt.all_licensees()
        self.populate_table(data)

    def search_licensees(self):
        search_text = self.search_input.text().strip()
        filtered_data = self.licensee_mgmt.search_licensees(search_text)
        self.populate_table(filtered_data)

    def populate_table(self, data):
        if data.empty:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            return
        
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(data.columns))
        self.table.setHorizontalHeaderLabels(data.columns.tolist())
        
        for row_idx, row in data.iterrows():
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row_idx, col_idx, item)

    def add_licensee(self):
        QMessageBox(self,'add info')