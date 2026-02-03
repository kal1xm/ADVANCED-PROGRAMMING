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
            

    def load_ranked_rhus(self, licensee_data=None):
        rhus = self.rhu_mgmt.all_rhus()
        if not licensee_data:
            ranked_rhus = []
            for i, rhu in enumerate(rhus):
                available = rhu['capacity'] - rhu['current_allocation']
                is_full = self.rhu_mgmt.is_rhu_full(rhu['name'])
                
                ranked_rhus.append({
                    'rank': i + 1,
                    'rhu': rhu,
                    'available': available,
                    'conflicts': rhu.get('conflicts', []),
                    'level': self.determine_conflict_level(rhu.get('conflicts', [])),
                    'is_full': is_full
                })
            
            self.allocation_widget.display_ranked_rhus(ranked_rhus)
            return
        ranked_rhus = []
        
        for rhu in rhus:
            score = 0
            conflicts = []
            if licensee_data.get('Nighttime_Curfew_Restrictions') == 'Yes':
                if rhu.get('provides_nighttime_curfew'):
                    score += 10
                else:
                    conflicts.append('No nighttime curfew monitoring')
            
            if licensee_data.get('Weekend_Curfew_Restrictions') == 'Yes':
                if rhu.get('provides_weekend_curfew'):
                    score += 10
                else:
                    conflicts.append('No weekend curfew')
            
            if licensee_data.get('Exclusion_Zone_Schools') == 'Yes':
                if not rhu.get('near_schools'):
                    score += 15
                else:
                    conflicts.append('Near school')
            
            if licensee_data.get('Drug_Searches_Required') == 'Yes':
                if rhu.get('has_drug_searches'):
                    score += 8
                else:
                    conflicts.append('No drug searches')
            
            if licensee_data.get('Suitable_for_Young_Offenders') == 'Yes':
                if rhu.get('suitable_young_offenders'):
                    score += 10
                else:
                    conflicts.append('Not suitable for young offenders')
            
            if licensee_data.get('Access_to_Medical_Services') == 'Yes':
                if rhu.get('has_medical_services'):
                    score += 8
                else:
                    conflicts.append('Limited medical services')
            
            if licensee_data.get('Transport_Links_Needed') == 'Yes':
                if rhu.get('has_transport_links'):
                    score += 5
                else:
                    conflicts.append('Limited transport links')
            
            if licensee_data.get('Mental_Health_Considerations') == 'Yes':
                if rhu.get('supports_mental_health'):
                    score += 10
                else:
                    conflicts.append('Limited mental health support')
            
            conflicts.extend(rhu.get('conflicts', []))
            
            available = rhu['capacity'] - rhu['current_allocation']
            is_full = self.rhu_mgmt.is_rhu_full(rhu['name'])
            
            if is_full:
                score -= 100
            
            ranked_rhus.append({
                'score': score,
                'rhu': rhu,
                'available': available,
                'conflicts': conflicts,
                'level': self.determine_conflict_level(conflicts),
                'is_full': is_full
            })
        
        ranked_rhus.sort(key=lambda x: x['score'], reverse=True)
        
        for i, item in enumerate(ranked_rhus):
            item['rank'] = i + 1
        
        self.allocation_widget.display_ranked_rhus(ranked_rhus)
        
    def determine_conflict_level(self, conflicts):
        if not conflicts:
            return None
        
        major_keywords = ['near school', 'no curfew', 'no drug searches', 'not suitable']
        
        for conflict in conflicts:
            if any(keyword in conflict.lower() for keyword in major_keywords):
                return 'major'
        
        return 'minor'
        
    def handle_view_details(self, rhu_name):
        print(f"View details for: {rhu_name}")
        #add details from excel file here
    def handle_allocate(self, rhu_name):
        if not self.selected_licensee:
            print("No licensee selected")
            return
        
        print(f"Allocate {self.selected_licensee.get('Name')} to {rhu_name}")