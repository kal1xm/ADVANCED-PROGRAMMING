from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QScrollArea)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

class AllocationSpaceWidget(QWidget):
    back_to_dashboard = Signal()
    logout = Signal()
    view_details_clicked = Signal(str)  
    allocate_clicked = Signal(str)  
    
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
        """Create the top header with title and buttons"""
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
        """Create the main content area"""
        content = QFrame()
        content.setStyleSheet("background-color: #1a1a1a;")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)
        
        page_title = QLabel("Prisoner Allocation")
        page_title.setStyleSheet("""
            color: white;
            font-size: 36px;
            font-weight: bold;
        """)
        
        self.info_section = self.create_info_section()
        
        matches_label = QLabel("Best matches shown:")
        matches_label.setStyleSheet("""
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
        

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
        """)
        
        self.rhu_list_widget = QWidget()
        self.rhu_list_layout = QVBoxLayout()
        self.rhu_list_layout.setSpacing(20)
        self.rhu_list_widget.setLayout(self.rhu_list_layout)
        
        scroll.setWidget(self.rhu_list_widget)
        
        layout.addWidget(page_title)
        layout.addWidget(self.info_section)
        layout.addWidget(matches_label)
        layout.addWidget(ranked_label)
        layout.addWidget(scroll)
        layout.addStretch()
        
        content.setLayout(layout)
        return content
        
    def create_info_section(self):
        section = QFrame()
        section.setStyleSheet("""
            QFrame {
                background-color: transparent;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        self.licensee_label = QLabel("Selected licensee: _____")
        self.licensee_label.setStyleSheet("""
            color: white;
            font-size: 16px;
        """)
        
        self.release_label = QLabel("release: _ (needs curfew?) (sex offender, etc)")
        self.release_label.setStyleSheet("""
            color: #aaa;
            font-size: 14px;
        """)
        
        layout.addWidget(self.licensee_label)
        layout.addWidget(self.release_label)
        
        section.setLayout(layout)
        return section
        
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
        
        rank_name = QLabel(f"{rank} {rhu_data['name']}")
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
        
        button_layout = QHBoxLayout()
        
        view_details_btn = QPushButton("View Details")
        view_details_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #4a9eff;
                border: none;
                padding: 5px;
                text-align: left;
                font-size: 14px;
            }
            QPushButton:hover {
                color: #6bb3ff;
                text-decoration: underline;
            }
        """)
        view_details_btn.clicked.connect(lambda: self.view_details_clicked.emit(rhu_data['name']))
        
        if is_full:
            allocate_btn = QPushButton("Cannot Allocate - Full")
            allocate_btn.setEnabled(False)
            allocate_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #ff3b30;
                    border: none;
                    padding: 5px;
                    text-align: left;
                    font-size: 14px;
                }
            """)
        else:
            allocate_btn = QPushButton("Allocate to This RHU")
            allocate_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #4a9eff;
                    border: none;
                    padding: 5px;
                    text-align: left;
                    font-size: 14px;
                }
                QPushButton:hover {
                    color: #6bb3ff;
                    text-decoration: underline;
                }
            """)
            allocate_btn.clicked.connect(lambda: self.allocate_clicked.emit(rhu_data['name']))
        
        button_layout.addWidget(view_details_btn)
        button_layout.addWidget(allocate_btn)
        button_layout.addStretch()
        
        layout.addWidget(rank_name)
        layout.addWidget(cost_capacity)
        layout.addWidget(conflicts_label)
        layout.addLayout(button_layout)
        
        card.setLayout(layout)
        return card
        
    def update_licensee_info(self, name, release_date, flags):
        if name:
            self.licensee_label.setText(f"Selected licensee: {name}")
            
            release_text = f"release: {release_date}"
            if flags:
                release_text += f" ({', '.join(flags)})"
            
            self.release_label.setText(release_text)
        else:
            self.licensee_label.setText("Selected licensee: _____")
            self.release_label.setText("release: _ (licensee requirements")
            
    def display_ranked_rhus(self, ranked_rhus):
        while self.rhu_list_layout.count():
            child = self.rhu_list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        for item in ranked_rhus:
            card = self.create_rhu_card(
                item['rank'],
                item['rhu'],
                item['available'],
                item['conflicts'],
                item['level'],
                item['is_full']
            )
            self.rhu_list_layout.addWidget(card)