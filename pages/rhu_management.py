from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
import pandas as pd
from datetime import datetime, timedelta
import os

csv_path = os.path.join('On_Licence_Housing_Data.xlsx')

class rhu_management():
    def __init__(self):
        self.data = pd.read_excel(csv_path)
        self.RHU_DATA = RHU_DATA

    def load_data(self):
        self.data = pd.read_excel(self.csv_path)

    def all_rhus(self, SearchData):
        return self.RHU_DATA

    def Search_rhus(self, SearchData):   
        filters =self.data[
             self.data['Current_Location'].astype(str).str.lower().str.contains(SearchData, na=False)
        ]
        return filters

    def add_rhu(self, RHU_DATA):
        self.RHU_DATA.append(RHU_DATA)
        
    def update_rhu(self, rhu_name, updated_data):
        for i, rhu in enumerate(self.rhu_data):
            if rhu['name'] == rhu_name:
                for key, value in updated_data.items():
                    self.rhu_data[i][key] = value
                return True
        return False
        










RHU_DATA = [
    {
        'name': 'Wolverine House',
        'cost_per_day': 58,
        'capacity': 1500,
        'current_allocation': 0,
        'provides_nighttime_curfew': True,
        'provides_weekend_curfew': False,
        'near_schools': True,
        'has_drug_searches': True,
        'suitable_young_offenders': False,
        'has_medical_services': True,
        'has_transport_links': True,
        'supports_mental_health': True,
        'conflicts': ['Near school', 'No curfew monitoring']
    },
    {
        'name': 'HMP Low Newton',
        'cost_per_day': 65,
        'capacity': 1800,
        'current_allocation': 0,
        'provides_nighttime_curfew': True,
        'provides_weekend_curfew': True,
        'near_schools': False,
        'has_drug_searches': True,
        'suitable_young_offenders': True,
        'has_medical_services': True,
        'has_transport_links': True,
        'supports_mental_health': True,
        'conflicts': []
    },
    {
        'name': 'Northumbria Facility',
        'cost_per_day': 72,
        'capacity': 2000,
        'current_allocation': 0,
        'provides_nighttime_curfew': True,
        'provides_weekend_curfew': True,
        'near_schools': False,
        'has_drug_searches': True,
        'suitable_young_offenders': True,
        'has_medical_services': True,
        'has_transport_links': False,
        'supports_mental_health': True,
        'conflicts': ['Limited transport links']
    },
    {
        'name': 'Congleton Hostel',
        'cost_per_day': 45,
        'capacity': 1200,
        'current_allocation': 0,
        'provides_nighttime_curfew': False,
        'provides_weekend_curfew': True,
        'near_schools': True,
        'has_drug_searches': False,
        'suitable_young_offenders': False,
        'has_medical_services': False,
        'has_transport_links': True,
        'supports_mental_health': False,
        'conflicts': ['No night staff', 'No drug searches']
    }
]