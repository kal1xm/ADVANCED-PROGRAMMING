#kallumleew24023993
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView, QComboBox, QDialog, QFormLayout, QDateEdit, QDialogButtonBox)
from PySide6.QtCore import Signal, Qt, QDate
from PySide6.QtGui import QFont, QColor
from datetime import datetime, timedelta
from pages.Release_management import ReleaseManagement
import pandas as pd

class UpdateDateDialog(QDialog):
    def __init__(self, current_date, licensee_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Update Release Date")
        self.setModal(True)
        self.setMinimumWidth(400)
        
        layout = QFormLayout()
        
        info_label = QLabel(f"Updating release date for: {licensee_name}")
        info_label.setStyleSheet("font-weight: bold; margin-bottom: 10px;")
        layout.addRow(info_label)
        
        current_label = QLabel(f"Current Date: {current_date}")
        layout.addRow(current_label)
        
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("dd/MM/yyyy")
        
        self.date_edit.setMinimumDate(QDate.currentDate())
        

        try:
            if isinstance(current_date, str):
                date_obj = datetime.strptime(current_date, "%Y-%m-%d %H:%M:%S")
            else:
                date_obj = current_date
            qdate = QDate(date_obj.year, date_obj.month, date_obj.day)
            self.date_edit.setDate(qdate)
        except:
            self.date_edit.setDate(QDate.currentDate())
        
        layout.addRow("New Release Date:", self.date_edit)
        
        warning_label = QLabel("⚠️ Note: Increases to release dates are rare and will trigger a warning.")
        warning_label.setStyleSheet("color: #ff9500; font-size: 11px; margin-top: 10px;")
        warning_label.setWordWrap(True)
        layout.addRow(warning_label)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        layout.addRow(buttons)
        self.setLayout(layout)
    
    def get_date(self):
        qdate = self.date_edit.date()
        return datetime(qdate.year(), qdate.month(), qdate.day())


class ReleaseManagementWidget(QWidget):
    back_to_dashboard = Signal()
    logout = Signal()
    
    def __init__(self):
        super().__init__()
        self.release_mgmt = ReleaseManagement()
        self.setupUI()
        self.refresh_data()
        
    def setupUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        

        header_layout = QHBoxLayout()
        title = QLabel("Release Management")
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
        
    
        section_title = QLabel("Upcoming Releases:")
        section_font = QFont()
        section_font.setPointSize(14)
        section_font.setBold(True)
        section_title.setFont(section_font)
        section_title.setStyleSheet("color: white; margin-top: 20px; margin-bottom: 10px;")
        main_layout.addWidget(section_title)
        
        
        filter_layout = QHBoxLayout()
        
        
        rhu_label = QLabel("Filter by RHU:")
        rhu_label.setStyleSheet("color: white; font-size: 14px;")
        self.rhu_filter = QComboBox()
        self.rhu_filter.setMinimumHeight(35)
        self.rhu_filter.addItem("All RHUs")
        self.rhu_filter.setStyleSheet("""
            QComboBox {
                background-color: #3d3d3d;
                color: white;
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 5px;
            }
            QComboBox:hover {
                background-color: #4d4d4d;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #3d3d3d;
                color: white;
                selection-background-color: #4d4d4d;
            }
        """)
        self.rhu_filter.currentTextChanged.connect(self.filter_by_rhu)
        
        filter_layout.addWidget(rhu_label)
        filter_layout.addWidget(self.rhu_filter)
        
    
        search_label = QLabel("Search:")
        search_label.setStyleSheet("color: white; font-size: 14px; margin-left: 20px;")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, prison ID, or RHU")
        self.search_input.setMinimumHeight(35)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #3d3d3d;
                color: white;
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #6d6d6d;
            }
        """)
        self.search_input.textChanged.connect(self.search_releases)
        
        search_btn = QPushButton("Search")
        search_btn.setMinimumHeight(35)
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #4d4d4d;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #5d5d5d;
            }
        """)
        search_btn.clicked.connect(self.search_releases)
        
        filter_layout.addWidget(search_label)
        filter_layout.addWidget(self.search_input)
        filter_layout.addWidget(search_btn)
        filter_layout.addStretch()
        
        main_layout.addLayout(filter_layout)
        
        
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
                padding: 8px;
                border: 1px solid #555555;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #5d5d5d;
            }
        """)
        
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Name", "Prison ID", "RHU Name", "Release Date", "Days Until Release", "Info"
        ])
        

        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        for i in range(5):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
        
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.cellDoubleClicked.connect(self.on_cell_double_clicked)
        
        main_layout.addWidget(self.table)
        

        button_layout = QHBoxLayout()
        
        view_info_btn = QPushButton("View Details")
        view_info_btn.setMinimumHeight(40)
        view_info_btn.setStyleSheet("""
            QPushButton {
                background-color: #4d4d4d;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #5d5d5d;
            }
        """)
        view_info_btn.clicked.connect(self.view_details)
        
        update_date_btn = QPushButton("Update Release Date")
        update_date_btn.setMinimumHeight(40)
        update_date_btn.setStyleSheet("""
            QPushButton {
                background-color: #4d4d4d;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #5d5d5d;
            }
        """)
        update_date_btn.clicked.connect(self.update_release_date)
        
        contact_rhu_btn = QPushButton("Contact RHU")
        contact_rhu_btn.setMinimumHeight(40)
        contact_rhu_btn.setStyleSheet("""
            QPushButton {
                background-color: #4d4d4d;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #5d5d5d;
            }
        """)
        contact_rhu_btn.clicked.connect(self.contact_rhu)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setMinimumHeight(40)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #4d4d4d;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #5d5d5d;
            }
        """)
        refresh_btn.clicked.connect(self.refresh_data)

        
        button_layout.addWidget(view_info_btn)
        button_layout.addWidget(update_date_btn)
        button_layout.addWidget(contact_rhu_btn)
        button_layout.addWidget(refresh_btn)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        

        self.setStyleSheet("background-color: #2d2d2d;")
        self.setLayout(main_layout)
    
    def refresh_data(self):

        self.release_mgmt.load_data()
        upcoming = self.release_mgmt.get_upcoming_releases()
        self.populate_table(upcoming)
        self.update_rhu_filter()
    
    def populate_table(self, data):
        if data.empty:
            self.table.setRowCount(0)
            return
        
        self.table.setRowCount(len(data))
        
        for row_idx, (idx, row) in enumerate(data.iterrows()):
            
            name_item = QTableWidgetItem(str(row.get('Name', 'Unknown')))
            self.table.setItem(row_idx, 0, name_item)
            

            prison_id_item = QTableWidgetItem(str(row.get('Prison_Role_ID', 'N/A')))
            self.table.setItem(row_idx, 1, prison_id_item)
            

            rhu_item = QTableWidgetItem(str(row.get('Current_Location', 'N/A')))
            self.table.setItem(row_idx, 2, rhu_item)
            

            release_date = row.get('Release_Date')
            if pd.notna(release_date):
                date_str = release_date.strftime('%d/%m/%Y')
            else:
                date_str = 'N/A'
            date_item = QTableWidgetItem(date_str)
            self.table.setItem(row_idx, 3, date_item)
            

            days = row.get('Days_Until_Release', 0)
            days_item = QTableWidgetItem(str(int(days)) if pd.notna(days) else 'N/A')
            
            if pd.notna(days):
                if days <= 7:
                    days_item.setBackground(QColor("#8B0000"))  
                    days_item.setForeground(QColor("white"))
                elif days <= 14:
                    days_item.setBackground(QColor("#FF8C00"))  
                    days_item.setForeground(QColor("white"))
            
            self.table.setItem(row_idx, 4, days_item)
            
            
            info_item = QTableWidgetItem("(info)")
            info_item.setForeground(QColor("#4da6ff"))
            self.table.setItem(row_idx, 5, info_item)
    
    def update_rhu_filter(self):
        current_selection = self.rhu_filter.currentText()
        self.rhu_filter.clear()
        self.rhu_filter.addItem("All RHUs")
        
        rhus = self.release_mgmt.get_unique_rhus()
        self.rhu_filter.addItems(rhus)
        
        index = self.rhu_filter.findText(current_selection)
        if index >= 0:
            self.rhu_filter.setCurrentIndex(index)
    
    def filter_by_rhu(self):
        selected_rhu = self.rhu_filter.currentText()
        
        if selected_rhu == "All RHUs":
            upcoming = self.release_mgmt.get_upcoming_releases()
        else:
            upcoming = self.release_mgmt.get_upcoming_releases()
            upcoming = upcoming[upcoming['Current_Location'] == selected_rhu]
        
        self.populate_table(upcoming)
    
    def search_releases(self):
        search_text = self.search_input.text().strip()
        
        if not search_text:
            self.filter_by_rhu()
            return
        
        filtered = self.release_mgmt.search_releases(search_text)
        self.populate_table(filtered)
    
    def view_details(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a licensee to view details")
            return
        
        name = self.table.item(selected_row, 0).text()
        prison_id = self.table.item(selected_row, 1).text()
        rhu_name = self.table.item(selected_row, 2).text()
        release_date = self.table.item(selected_row, 3).text()
        days = self.table.item(selected_row, 4).text()
        
        details = f"""Name: {name}
Prison ID: {prison_id}
RHU: {rhu_name}
Release Date: {release_date}
Days Until Release: {days}"""
        
        QMessageBox.information(self, "Licensee Details", details)
    
    def on_cell_double_clicked(self, row, column):
        if column == 5:  
            self.view_details()
    
    def update_release_date(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a licensee to update release date")
            return
        
        name = self.table.item(selected_row, 0).text()
        prison_id = self.table.item(selected_row, 1).text()
        current_date = self.table.item(selected_row, 3).text()
        
        dialog = UpdateDateDialog(current_date, name, self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_date = dialog.get_date()
            
            success, warning = self.release_mgmt.update_release_date(prison_id, new_date)
            
            if success:
                message = f"Release date updated successfully for {name}."
                if warning:
                    message += f"\n\n{warning}"
                    QMessageBox.warning(self, "Date Updated with Warning", message)
                else:
                    QMessageBox.information(self, "Success", message)
                
                self.refresh_data()
            else:
                QMessageBox.critical(self, "Error", f"Failed to update release date:\n{warning}")
    
    def contact_rhu(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a licensee")
            return
        
        rhu_name = self.table.item(selected_row, 2).text()
        contact_info = self.release_mgmt.get_rhu_contact_info(rhu_name)
        
        message = f"""Contact information for {rhu_name}:

Email: {contact_info['email']}
Phone: {contact_info['phone']}

You can use this information to contact the RHU regarding upcoming releases."""
        


    def load_more(self):
        self.release_mgmt.load_data()
        data = self.release_mgmt.data
        
        if data.empty or 'Release_Date' not in data.columns:
            return
        
        today = datetime.now()
        future_date = today + timedelta(days=180)
        
        upcoming = data[
            (data['Release_Date'] >= today) & 
            (data['Release_Date'] <= future_date)
        ].copy()
        
        upcoming['Days_Until_Release'] = (upcoming['Release_Date'] - today).dt.days
        upcoming = upcoming.sort_values('Release_Date')
        
        self.populate_table(upcoming)
        QMessageBox.information(self, "Extended View", "Now showing releases for the next 180 days")