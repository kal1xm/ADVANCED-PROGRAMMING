from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

class CostManagementWidget(QWidget):
    back_to_dashboard = Signal()
    logout = Signal()
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
       
        header = QHBoxLayout()
        back_btn = QPushButton("← Back to Dashboard")
        back_btn.clicked.connect(self.back_to_dashboard.emit)
        header.addWidget(back_btn)
        
        title = QLabel("Cost Management")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        header.addWidget(title)
        header.addStretch()
        
        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.logout.emit)
        header.addWidget(logout_btn)
        
        layout.addLayout(header)
        
       
        info = QLabel("Cost Management Content Goes Here")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)
        
        layout.addStretch()
        self.setLayout(layout)