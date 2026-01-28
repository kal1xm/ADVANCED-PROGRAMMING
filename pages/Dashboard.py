from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

class DashboardWidget(QWidget):
   
    navigate_to_licensee = Signal()
    navigate_to_rhu = Signal()
    navigate_to_allocation = Signal()
    navigate_to_release = Signal()
    navigate_to_cost = Signal()
    navigate_to_dashboard = Signal()
    logout = Signal()
    
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 0)
        main_layout.setSpacing(20)
        
       
        header_layout = QHBoxLayout()
        title = QLabel("On-Licence Housing Allocation System")
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
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5d5d5d;
            }
        """)
        logout_btn.clicked.connect(self.logout.emit)
        header_layout.addWidget(logout_btn)
        
        main_layout.addLayout(header_layout)
        
       
        welcome = QLabel("Durham Allocation Office - Dashboard")
        welcome.setAlignment(Qt.AlignCenter)
        welcome_font = QFont()
        welcome_font.setPointSize(16)
        welcome.setFont(welcome_font)
        welcome.setStyleSheet("color: white;")
        main_layout.addWidget(welcome)
        
       
        stats_layout = QGridLayout()
        stats_layout.setSpacing(15)
        
        stats = [
            ("Pending Allocation", "23", "#332d36", "#cc6600"),      
            ("Currently Allocated", "87", "#332d36", "#cc6600"),     
            ("Due Release (7 days)", "12", "#332d36", "#cc6600"),    
            ("Daily Cost", "£3,240", "#332d36", "#cc6600")          
        ]
        
        for i, (label_text, value_text, bg_color, text_color) in enumerate(stats):
            stat_widget = QWidget()
            stat_layout = QVBoxLayout()
            stat_widget.setMinimumHeight(200)
            stat_widget.setStyleSheet(f"""
                QWidget {{
                    background-color: {bg_color};
                    border: 2px solid #cccccc;
                    border-radius: 10px;
                }}
            """)
            
            value_label = QLabel(value_text)
            value_label.setAlignment(Qt.AlignCenter)
            value_font = QFont()
            value_font.setPointSize(48)
            value_font.setBold(True)
            value_label.setFont(value_font)
            value_label.setStyleSheet(f"color: {text_color}; background-color: transparent;")
            
            label = QLabel(label_text)
            label.setAlignment(Qt.AlignCenter)
            label_font = QFont()
            label_font.setPointSize(14)
            label.setFont(label_font)
            label.setWordWrap(True)
            label.setStyleSheet(f"color: {text_color}; background-color: transparent;")
            
            stat_layout.addStretch()
            stat_layout.addWidget(value_label)
            stat_layout.addWidget(label)
            stat_layout.addStretch()
            stat_widget.setLayout(stat_layout)
            
            stats_layout.addWidget(stat_widget, 0, i)
        
        main_layout.addLayout(stats_layout)
        
      
        main_layout.addStretch()
        
    
        self.setStyleSheet("background-color: #2d2d2d;")
        
        self.setLayout(main_layout)