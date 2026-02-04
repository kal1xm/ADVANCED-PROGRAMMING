#kallumleew24023993
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Signal

from pages.rhu_management import rhu_management
from pages.licensee_management import licensee_management
from pages.allocation_spaceWidget import AllocationSpaceWidget

class AllocationSpace(QWidget):
    back_to_dashboard = Signal()
    logout = Signal()
    
    def __init__(self):
        super().__init__()
        self.rhu_mgmt = rhu_management()
        self.licensee_mgmt = licensee_management()
        self.selected_licensee = None
        self.Allo_ui()
        
    def Allo_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.allocation_widget = AllocationSpaceWidget()
        
        self.allocation_widget.back_to_dashboard.connect(self.back_to_dashboard.emit)
        self.allocation_widget.logout.connect(self.logout.emit)
        self.allocation_widget.search_btn.clicked.connect(self.search_licensees)
        self.allocation_widget.refresh_btn.clicked.connect(self.refresh_data)
        
        
        layout.addWidget(self.allocation_widget)
        self.setLayout(layout)
        
        self.refresh_data()
        
    def refresh_data(self):
        data = self.licensee_mgmt.all_licensees()
        self.allocation_widget.populate_table(data)
    
    def search_licensees(self):
        search_text = self.allocation_widget.search_input.text().strip()
        filtered_data = self.licensee_mgmt.search_licensees(search_text)
        self.allocation_widget.populate_table(filtered_data)
    
    def on_licensee_selected(self, licensee_data):
        self.selected_licensee = licensee_data
        self.load_ranked_rhus(licensee_data)

    def load_ranked_rhus(self, licensee_data):
        rhus = self.rhu_mgmt.all_rhus('')
        
        if not rhus:
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
            
            conflicts.extend(rhu.get('conflicts', []))
            
            available = rhu.get('capacity', 0) - rhu.get('current_allocation', 0)
            is_full = self.rhu_mgmt.is_rhu_full(rhu.get('name', ''))
            
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
        
        self.allocation_widget.display_ranked_rhus(ranked_rhus[:3])
        
    def determine_conflict_level(self, conflicts):
        if not conflicts:
            return None
        
        major_keywords = ['near school', 'no curfew', 'no drug searches', 'not suitable']
        
        for conflict in conflicts:
            if any(keyword in conflict.lower() for keyword in major_keywords):
                return 'major'
        
        return 'minor'