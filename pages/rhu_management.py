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
                                                                                #all same code as other pages, used for searching and loading DB
    def all_rhus(self, SearchData):
        return self.RHU_DATA

    def Search_rhus(self, SearchData):
        if not SearchData:
            return self.RHU_DATA
        
        search_lower = SearchData.lower()           #search for the RHU
        filters = [
            rhu for rhu in self.RHU_DATA 
            if search_lower in rhu['name'].lower() or 
               any(search_lower in conflict.lower() for conflict in rhu['conflicts'])
        ]
        return filters



    def Search_licensees_by_location(self, SearchData):
        if not SearchData:
            return self.data
        
        filters1 = self.data[
            self.data['Current_Location'].astype(str).str.lower().str.contains(SearchData.lower(), na=False)     #same as in lciensee management, can search the location via licensee
        ]
        return filters1
    

    def is_rhu_full(self, rhu_name): 
        rhu = self.get_rhu_by_name(rhu_name)
        if rhu:
            return rhu['current_allocation'] >= rhu['capacity']
        return False
    




    def add_rhu(self, RHU_DATA):
        self.RHU_DATA.append(RHU_DATA)
        
    def update_rhu(self, rhu_name, updated_data):
        for i, rhu in enumerate(self.rhu_data):
            if rhu['name'] == rhu_name:
                for key, value in updated_data.items():
                    self.rhu_data[i][key] = value
                return True
        return False
        


    def get_rhu_by_name(self, rhu_name):
        for rhu in self.RHU_DATA:
            if rhu['name'] == rhu_name:
                return rhu
        return None
    
    def is_rhu_full(self, rhu_name):        #checking if RHU is at max capacity
        rhu = self.get_rhu_by_name(rhu_name)
        if rhu:
            return rhu['current_allocation'] >= rhu['capacity']
        return False


    def get_licensees_in_rhu(self, rhu_name):      #displaying licensees in the RHU
        if 'RHU_Name' in self.data.columns:
            rhu_prisoners = self.data[self.data['RHU_Name'] == rhu_name]
        elif 'Location' in self.data.columns:
            rhu_prisoners = self.data[self.data['Location'] == rhu_name]
        elif 'Current_Location' in self.data.columns:
            rhu_prisoners = self.data[self.data['Current_Location'] == rhu_name]
        else:
            return []
        
        prisoners = []
        if not rhu_prisoners.empty:
            if 'Name' in rhu_prisoners.columns and 'Prison_Role_ID' in rhu_prisoners.columns:
                prisoners = [
                    f"{row['Name']} - ID: {row['Prison_Role_ID']}" 
                    for _, row in rhu_prisoners.iterrows()
                ]
            elif 'Prisoner_Name' in rhu_prisoners.columns:
                prisoners = rhu_prisoners['Prisoner_Name'].tolist()
        
        return prisoners
    
    def reload_data(self):
        self.load_data()






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