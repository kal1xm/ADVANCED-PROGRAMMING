#kallumleew24023993
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMainWindow, QStackedWidget)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import sys


from pages.DashboardWidget import DashboardWidget                      
from pages.licensee_managementWidget import LicenseeManagementWidget
from pages.rhu_management import RHUManagement
from pages.allocation_space import AllocationSpace
from pages.Release_managementWidget import ReleaseManagementWidget
from pages.Cost_managementWidget import CostManagementWidget


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("On-Licence Housing Allocation System")
        self.setMinimumSize(1800, 1200)
        
      
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        title = QLabel("Durham Allocation Office")
        title.setAlignment(Qt.AlignCenter)
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
        self.dashboard.logout.connect(QApplication.quit)   #logout button directly closes the program
        self.licensee_mgmt.logout.connect(QApplication.quit)
        self.rhu_mgmt.logout.connect(QApplication.quit)
        self.allocation.logout.connect(QApplication.quit)
        self.stacked_widget.addWidget(self.dashboard)          
        self.stacked_widget.addWidget(self.licensee_mgmt)    
        self.stacked_widget.addWidget(self.rhu_mgmt)           
        self.stacked_widget.addWidget(self.allocation)       
        self.stacked_widget.addWidget(self.release_mgmt)       
        self.stacked_widget.addWidget(self.cost_mgmt)         
        
        
        self.create_navigation_buttons(main_layout)
        

        self.stacked_widget.setCurrentIndex(0)
    
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