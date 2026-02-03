from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from pages.rhu_management import rhu_management
from pages.allocation_spaceWidget import AllocationSpaceWidget

class AllocationSpace(QWidget):
    back_to_dashboard = Signal()
    logout = Signal()
    
    def __init__(self):
        super().__init__()
        self.rhu_mgmt = rhu_management()
        self.selected_licensee = None
        self.Allo_ui()
        
    def Allo_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.allocation_widget = AllocationSpaceWidget()
        
        self.allocation_widget.back_to_dashboard.connect(self.back_to_dashboard.emit)
        self.allocation_widget.logout.connect(self.logout.emit)
        self.allocation_widget.view_details_clicked.connect(self.handle_view_details)
        self.allocation_widget.allocate_clicked.connect(self.handle_allocate)
        
        layout.addWidget(self.allocation_widget)
        self.setLayout(layout)
        
        self.load_ranked_rhus()
        
    def set_selected_licensee(self, licensee_data):
        self.selected_licensee = licensee_data
        
        if licensee_data:
            name = licensee_data.get('Name', 'Unknown')
            release_date = licensee_data.get('Release_Date', 'Unknown')
            
            flags = []
            if licensee_data.get('Nighttime_Curfew_Restrictions') == 'Yes':
                flags.append('needs curfew')
            if licensee_data.get('Weekend_Curfew_Restrictions') == 'Yes':
                flags.append('weekend curfew')
            if licensee_data.get('Category') == 'Sex Offender':
                flags.append('sex offender')
            if licensee_data.get('Exclusion_Zone_Schools') == 'Yes':
                flags.append('school exclusion')
            
            self.allocation_widget.update_licensee_info(name, release_date, flags)
            
            self.load_ranked_rhus(licensee_data)
        else:
            self.allocation_widget.update_licensee_info(None, None, [])
            
 #sorting functions out next