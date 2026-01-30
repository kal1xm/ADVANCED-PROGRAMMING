from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from .Dashboard import Dashboard

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
        self.dashboard = Dashboard()
       
        header_layout = QHBoxLayout()
        title = QLabel("On-Licence Housing Allocation System")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: white; background-color: #000000;")
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
        
        self.pending_label = None
        self.allocated_label = None
        self.get_month_label = None
        self.daily_cost_label = None


        stats_layout = QGridLayout()
        stats_layout.setSpacing(15)
        
        stats = [
            ("Pending Allocation", "", "#000000", "#cc6600"),      
            ("Currently Allocated", "", "#000000", "#cc6600"),     
            ("Due Release (1 month)", "", "#000000", "#cc6600"),    
            ("Daily Cost", "", "#000000", "#cc6600")          
        ]
        
        for i, (label_text, value_text, bg_color, text_color) in enumerate(stats):
            stat_widget = QWidget()
            stat_layout = QVBoxLayout()
            stat_widget.setMinimumHeight(200)
            stat_widget.setStyleSheet(f"""
                QWidget {{
                    background-color: {bg_color};
                    border: 2px solid #000000;
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

            if i == 0:
                self.pending_label = value_label
            elif i == 1:
                self.allocated_label = value_label
            elif i == 2:
                self.get_month_label = value_label
            elif i == 3:
                self.daily_cost_label = value_label

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

        self.update_metrics()

    def update_metrics(self):
        pending = self.dashboard.get_pending_allocation()
        allocated = self.dashboard.get_currently_allocated()
        due_release = self.dashboard.get_month_released()
        daily_cost = self.dashboard.get_daily_cost()
        print(f"Pending: {pending}")    #for debug, had an issue showing the correct values.
        print(f"Allocated: {allocated}")
        print(f"Due Release: {due_release}")
        print(f"Daily Cost: {daily_cost}")
        self.pending_label.setText(str(pending))
        self.allocated_label.setText(str(allocated))
        self.get_month_label.setText(str(due_release))
        self.daily_cost_label.setText(f"£{daily_cost:,.0f}")

        
        
        
