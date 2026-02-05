#kallumleew24023993
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMainWindow, QStackedWidget)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import sys
from pages.Login import LoginPage
from pages.DashboardWidget import DashboardWidget                      
from pages.licensee_managementWidget import LicenseeManagementWidget
from pages.rhu_management import RHUManagement
from pages.allocation_space import AllocationSpace
from pages.Release_managementWidget import ReleaseManagementWidget
from pages.Cost_managementWidget import CostManagementWidget

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Allocation Login")
        self.setMinimumSize(1800, 1200)
        
        self.main_stacked = QStackedWidget()
        self.setCentralWidget(self.main_stacked)
        
        self.login_page = LoginPage()
        self.login_page.login_successful.connect(self.show_main_app)
        
        self.main_stacked.addWidget(self.login_page)
        
        self.main_app_widget = None
        
        self.main_stacked.setCurrentWidget(self.login_page)
    
    def show_main_app(self):
        if self.main_app_widget is None:
            self.main_app_widget = QWidget()
            main_layout = QVBoxLayout(self.main_app_widget)
            
            title = QLabel("Durham Allocation Office")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title_font = QFont()
            title_font.setPointSize(18)
            title_font.setBold(True)
            title.setFont(title_font)
            main_layout.addWidget(title)

            self.stacked_widget = QStackedWidget()
            main_layout.addWidget(self.stacked_widget)
            
            self.dashboard = DashboardWidget()
            self.licensee_mgmt = LicenseeManagementWidget()
            self.rhu_mgmt = RHUManagement()
            self.allocation = AllocationSpace()
            self.release_mgmt = ReleaseManagementWidget()
            self.cost_mgmt = CostManagementWidget(self.dashboard.dashboard.cost_manage)
            
            self.dashboard.logout.connect(self.handle_logout)
            self.licensee_mgmt.logout.connect(self.handle_logout)
            self.rhu_mgmt.logout.connect(self.handle_logout)
            self.allocation.logout.connect(self.handle_logout)
            
            self.stacked_widget.addWidget(self.dashboard)          
            self.stacked_widget.addWidget(self.licensee_mgmt)    
            self.stacked_widget.addWidget(self.rhu_mgmt)           
            self.stacked_widget.addWidget(self.allocation)       
            self.stacked_widget.addWidget(self.release_mgmt)       
            self.stacked_widget.addWidget(self.cost_mgmt)         
            
            self.create_navigation_buttons(main_layout)
            
            self.stacked_widget.setCurrentIndex(0)
            
            self.main_stacked.addWidget(self.main_app_widget)
        
        self.main_stacked.setCurrentWidget(self.main_app_widget)
    
    def handle_logout(self):
        self.login_page.username_input.clear()
        self.login_page.password_input.clear()
        
        self.main_stacked.setCurrentWidget(self.login_page)
    
    def create_navigation_buttons(self, layout):
        button_layout = QVBoxLayout()
        
        buttons = [
            ("Dashboard", 0),
            ("Licensee Management", 1),
            ("RHU Management", 2),
            ("Allocation Workspace", 3),
            ("Release Management", 4),
            ("Cost Management", 5),
        ]
        
        for button_text, page_index in buttons:
            btn = QPushButton(button_text)
            btn.setMinimumHeight(50)
            btn.clicked.connect(lambda checked, idx=page_index: self.switch_page(idx))
            button_layout.addWidget(btn)
        
        layout.addLayout(button_layout)
    
    def switch_page(self, page_index):
        self.stacked_widget.setCurrentIndex(page_index)
        print(f"Switched to page: {page_index}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())