#kallumleew24023993
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFrame)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont





class LoginPage(QWidget):
    login_successful = Signal()
    
    def __init__(self):
        super().__init__()
        self.Login_ui()
        
    def Login_ui(self):
        self.setWindowTitle("On-Licence Housing Allocation System - Login")
        self.setStyleSheet("background-color: #1a1a1a;")
    
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        login_container = QFrame()
        login_container.setStyleSheet("""
            QFrame {
                background-color: #2b2b2b;
                border-radius: 10px;
                padding: 40px;
            }
        """)
        login_container.setFixedWidth(400)
        
        container_layout = QVBoxLayout()
        container_layout.setSpacing(20)
        
        title = QLabel("Durham Allocation Office")
        title.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("Login to continue")
        subtitle.setStyleSheet("""
            color: #888;
            font-size: 14px;
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        username_label = QLabel("Username:")
        username_label.setStyleSheet("color: white; font-size: 14px;")
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: Greu;
                border: 1px solid #3a3a3a;
                border-radius: 4px;
                padding: 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #4a9eff;
            }
        """)
        
        password_label = QLabel("Password:")
        password_label.setStyleSheet("color: white; font-size: 14px;")
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: Grey;
                border: 1px solid #3a3a3a;
                border-radius: 4px;
                padding: 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #4a9eff;
            }
        """)
        self.password_input.returnPressed.connect(self.login)
        
        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #4a9eff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6bb3ff;
            }
            QPushButton:pressed {
                background-color: #3a8edf;
            }
        """)
        self.login_button.clicked.connect(self.login)
        
        container_layout.addWidget(title)
        container_layout.addWidget(subtitle)
        container_layout.addSpacing(20)
        container_layout.addWidget(username_label)
        container_layout.addWidget(self.username_input)
        container_layout.addWidget(password_label)
        container_layout.addWidget(self.password_input)
        container_layout.addSpacing(10)
        container_layout.addWidget(self.login_button)
        
        login_container.setLayout(container_layout)
        
        main_layout.addWidget(login_container)
        
        self.setLayout(main_layout)
        
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if username == "Admin" and password == "123456789":
            self.login_successful.emit()
        else:
            QMessageBox.warning(
                self,
                "Login Failed",
                "Invalid username or password. Please try again."
            )
            self.password_input.clear()
            self.password_input.setFocus()