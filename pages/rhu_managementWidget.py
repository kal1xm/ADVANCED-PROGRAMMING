#kallumleew24023993
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,  QPushButton, QLineEdit, QListWidget, QFrame, QScrollArea, QListWidgetItem)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont




class RHUManagementWidget(QWidget):
    add_rhu_clicked = Signal()
    rhu_selected = Signal(str)
    logout = Signal()
    def __init__(self):
        super().__init__()
        self.RHU_UI()

        
    def RHU_UI(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        header = QHBoxLayout()
        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.logout.emit)
        header.addWidget(logout_btn)

        left_panel = self.create_left_panel()    #left and right split, as per wireframe
        self.right_panel = self.create_right_panel()

        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(self.right_panel, 3)
        
        self.setLayout(main_layout)
        self.setStyleSheet("background-color: Black;")

    
    def create_left_panel(self):
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: Blkac;
                border-right: 1px solid #444;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        search_label = QLabel("Search:")    #label search bar
        search_label.setStyleSheet("color: White; font-size: 14px;")

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search RHUs")   #search bar
        self.search_box.setStyleSheet("""
            QLineEdit {
                background-color: White;
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-size: 13px;
            }
        """)
        self.search_box.textChanged.connect(self.filter_rhu_list)

        self.add_button = QPushButton("Add new RHU")
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #4a9eff;
                border: none;
                padding: 10px;
                text-align: left;
                font-size: 14px;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #6bb3ff;
            }
        """)
        self.add_button.clicked.connect(self.add_rhu_clicked.emit)
        
        self.rhu_list = QListWidget()
        self.rhu_list.setStyleSheet("""
            QListWidget {
                background-color: #2b2b2b;
                color: white;
                border: none;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 15px;
                border-bottom: 1px solid #3a3a3a;
            }
            QListWidget::item:selected {
                background-color: #3a3a3a;
            }
            QListWidget::item:hover {
                background-color: #333;
            }
        """)
        self.rhu_list.itemClicked.connect(self.on_rhu_selected)
        
        layout.addWidget(search_label)
        layout.addWidget(self.search_box)
        layout.addWidget(self.add_button)
        layout.addWidget(self.rhu_list)
        
        panel.setLayout(layout)
        return panel
    

    def create_right_panel(self):
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #1a1a1a;
            }
        """)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: #1a1a1a;
                border: none;
            }
        """)
        
        content = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)
        
        self.info_title = QLabel("Select an RHU to view details")
        self.info_title.setStyleSheet("""
            color: #888; 
            font-size: 20px;
            font-weight: bold;
        """)

        info_container = QWidget()
        info_layout = QHBoxLayout()
        info_layout.setSpacing(20)
        info_container.setLayout(info_layout)
        
        self.cost_card = self.create_info_card("Cost:", "£0/day")
        self.capacity_card = self.create_info_card("Capacity:", "0/0")
        
        info_layout.addWidget(self.cost_card)
        info_layout.addWidget(self.capacity_card)
        info_layout.addStretch()
        
        conflicts_label = QLabel("Conflicts:")
        conflicts_label.setStyleSheet("""
            color: white;
            font-size: 16px;
            font-weight: bold;
            margin-top: 10px;
        """)
        
        self.conflicts_display = QLabel("No conflicts")
        self.conflicts_display.setWordWrap(True)
        self.conflicts_display.setStyleSheet("""
            color: #4cd964;
            font-size: 14px;
            background-color: #2b2b2b;
            padding: 15px;
            border-radius: 4px;
        """)
        
        self.allocation_status = QLabel("")
        self.allocation_status.setStyleSheet("""
            color: #4a9eff;
            font-size: 14px;
            background-color: #2b2b2b;
            padding: 15px;
            border-radius: 4px;
            margin-top: 10px;
        """)
        
        prisoners_label = QLabel("Currently Allocated Licensees:")
        prisoners_label.setStyleSheet("""
            color: white;
            font-size: 16px;
            font-weight: bold;
            margin-top: 10px;
        """)
        
        self.prisoners_list = QListWidget()
        self.prisoners_list.setStyleSheet("""
            QListWidget {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #3a3a3a;
                border-radius: 4px;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #3a3a3a;
            }
            QListWidget::item:hover {
                background-color: #333;
            }
        """)
        
        layout.addWidget(self.info_title)
        layout.addWidget(info_container)
        layout.addWidget(conflicts_label)
        layout.addWidget(self.conflicts_display)
        layout.addWidget(self.allocation_status)
        layout.addWidget(prisoners_label)
        layout.addWidget(self.prisoners_list)
        layout.addStretch()
        
        content.setLayout(layout)
        scroll.setWidget(content)
        
        panel_layout = QVBoxLayout()
        panel_layout.setContentsMargins(0, 0, 0, 0)
        panel_layout.addWidget(scroll)
        panel.setLayout(panel_layout)
        
        return panel
        
    def create_info_card(self, label_text, value_text):
        """Create an info card widget (for Cost and Capacity)"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #2b2b2b;
                border: none;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        card.setFixedWidth(250)
        
        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        label = QLabel(label_text)
        label.setStyleSheet("""
            color: #888;
            font-size: 12px;
        """)
        
        value = QLabel(value_text)
        value.setObjectName("value_label")
        value.setStyleSheet("""
            color: #ff9500;
            font-size: 24px;
            font-weight: bold;
        """)
        value.setWordWrap(True)
        
        layout.addWidget(label)
        layout.addWidget(value)
        
        card.setLayout(layout)
        return card
        
    def on_rhu_selected(self, item):
        rhu_name = item.text()
        self.rhu_selected.emit(rhu_name)
        
    def filter_rhu_list(self, text):
        for i in range(self.rhu_list.count()):
            item = self.rhu_list.item(i)
            item.setHidden(text.lower() not in item.text().lower())
            
    def add_rhu_list(self, rhu_names):
        self.rhu_list.clear()
        for name in rhu_names:
            self.rhu_list.addItem(name)
            
    def update_rhu_details(self, name, cost, capacity, allocation, conflicts, prisoners, is_full=False):
        self.info_title.setText(name)
        self.info_title.setStyleSheet("""
            color: white; 
            font-size: 24px;
            font-weight: bold;
        """)
        
   
        cost_value = self.cost_card.findChild(QLabel, "value_label")
        if cost_value:
            cost_value.setText(f"£{cost}/day")
            
       
        capacity_value = self.capacity_card.findChild(QLabel, "value_label")
        if capacity_value:
            if is_full:
                capacity_value.setText(f"FULL ({allocation}/{capacity})")
                capacity_value.setStyleSheet("""
                    color: #ff3b30;
                    font-size: 24px;
                    font-weight: bold;
                """)
            else:
                capacity_value.setText(f"{allocation}/{capacity}")
                capacity_value.setStyleSheet("""
                    color: #ff9500;
                    font-size: 24px;
                    font-weight: bold;
                """)
        
        if conflicts:
            conflict_count = len(conflicts)
            conflict_text = f" {conflict_count} conflicts (" + ", ".join(conflicts) + ")"
            self.conflicts_display.setText(conflict_text)
            self.conflicts_display.setStyleSheet("""
                color: #ff9500;
                font-size: 14px;
                background-color: #2b2b2b;
                padding: 15px;
                border-radius: 4px;
            """)
        else:
            self.conflicts_display.setText("No conflicts")
            self.conflicts_display.setStyleSheet("""
                color: #4cd964;
                font-size: 14px;
                background-color: #2b2b2b;
                padding: 15px;
                border-radius: 4px;
            """)
            
        if is_full:
            self.allocation_status.setText("View Details Cannot Allocate - Full")
            self.allocation_status.setStyleSheet("""
                color: #ff3b30;
                font-size: 14px;
                background-color: #2b2b2b;
                padding: 15px;
                border-radius: 4px;
                margin-top: 10px;
            """)
        else:
            self.allocation_status.setText("View Details")
            self.allocation_status.setStyleSheet("""
                color: #4a9eff;
                font-size: 14px;
                background-color: #2b2b2b;
                padding: 15px;
                border-radius: 4px;
                margin-top: 10px;
            """)
            
        self.prisoners_list.clear()
        if prisoners:
            for prisoner in prisoners:
                self.prisoners_list.addItem(prisoner)
        else:
            self.prisoners_list.addItem("No licensees currently allocated")
            
    def clear_rhu_details(self):
        self.info_title.setText("Select an RHU to view details")
        self.info_title.setStyleSheet("""
            color: #888; 
            font-size: 20px;
            font-weight: bold;
        """)
        
        cost_value = self.cost_card.findChild(QLabel, "value_label")
        if cost_value:
            cost_value.setText("£0/day")
            
        capacity_value = self.capacity_card.findChild(QLabel, "value_label")
        if capacity_value:
            capacity_value.setText("0/0")
            capacity_value.setStyleSheet("""
                color: #ff9500;
                font-size: 24px;
                font-weight: bold;
            """)
            
        self.conflicts_display.setText("No conflicts")
        self.conflicts_display.setStyleSheet("""
            color: #4cd964;
            font-size: 14px;
            background-color: #2b2b2b;
            padding: 15px;
            border-radius: 4px;
        """)
        
        self.allocation_status.setText("")
        self.prisoners_list.clear()

