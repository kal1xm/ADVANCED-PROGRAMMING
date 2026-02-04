#kallumleew24023993
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
import os
import pandas as pd



csv_path = os.path.join('On_Licence_Housing_Data.xlsx')

class licensee_management():
    def __init__(self):
        self.data = pd.read_excel(csv_path)
    

    def load_data(self):
        self.data = pd.read_excel(self.csv_path)

    def save_data(self):
        self.data.to_excel(self.csv_path, index=False)
        return True
    

    def all_licensees(self):
        return self.data
    

    def search_licensees(self, SearchData):
        if not SearchData:
            return self.data
        
        filters = self.data[
        self.data['Prison_Role_ID'].astype(str).str.lower().str.contains(SearchData, na=False) |
        self.data['Name'].astype(str).str.lower().str.contains(SearchData, na=False) |
        self.data['Home_Address'].astype(str).str.lower().str.contains(SearchData, na=False) |
        self.data['Gender'].astype(str).str.lower().str.contains(SearchData, na=False) |
        self.data['Category'].astype(str).str.lower().str.contains(SearchData, na=False) |
        self.data['Release_Date'].astype(str).str.lower().str.contains(SearchData, na=False) |
        self.data['Expected_End_of_Licence'].astype(str).str.lower().str.contains(SearchData, na=False) |
        self.data['Current_Location'].astype(str).str.lower().str.contains(SearchData, na=False) |
        self.data['Nighttime_Curfew_Restrictions'].astype(str).str.lower().str.contains(SearchData, na=False) |
        self.data['Weekend_Curfew_Restrictions'].astype(str).str.lower().str.contains(SearchData, na=False) |
        self.data['Exclusion_Zone_Victims'].astype(str).str.lower().str.contains(SearchData, na=False) |
        self.data['Exclusion_Zone_Schools'].astype(str).str.lower().str.contains(SearchData, na=False) |
        self.data['Exclusion_Zone_Other_Prisoners'].astype(str).str.lower().str.contains(SearchData, na=False) |
        self.data['General_Exclusion_Zone'].astype(str).str.lower().str.contains(SearchData, na=False) |
        self.data['Drug_Searches_Required'].astype(str).str.lower().str.contains(SearchData, na=False) |
        self.data['Proximity_to_Codefendants'].astype(str).str.lower().str.contains(SearchData, na=False) |
        self.data['Suitable_for_Young_Offenders'].astype(str).str.lower().str.contains(SearchData, na=False) |
        self.data['Access_to_Medical_Services'].astype(str).str.lower().str.contains(SearchData, na=False) |
        self.data['Transport_Links_Needed'].astype(str).str.lower().str.contains(SearchData, na=False) |
        self.data['Cultural_Religious_Needs'].astype(str).str.lower().str.contains(SearchData, na=False) |
        self.data['Mental_Health_Considerations'].astype(str).str.lower().str.contains(SearchData, na=False) |
        self.data['Gender_Preference'].astype(str).str.lower().str.contains(SearchData, na=False) |
        self.data['Access_to_Family'].astype(str).str.lower().str.contains(SearchData, na=False) |
        self.data['Prior_RHU_Experience'].astype(str).str.lower().str.contains(SearchData, na=False) |
        self.data['Employment_Training_Needs'].astype(str).str.lower().str.contains(SearchData, na=False) |
        self.data['Specific_Offending_Triggers'].astype(str).str.lower().str.contains(SearchData, na=False) |
        self.data['Period_of_Licence_Days'].astype(str).str.lower().str.contains(SearchData, na=False) |
        self.data['Notes_Misc'].astype(str).str.lower().str.contains(SearchData, na=False) |
        self.data['Status'].astype(str).str.lower().str.contains(SearchData, na=False)
            ]
        return filters
    
    def add_licensee(self, licensee_data):
        new_row = pd.DataFrame([licensee_data])
        self.data = pd.concat([self.data, new_row], ignore_index=True)
        return self.save_data()
    


    def remove_licensee(self, prison_id):
        self.data = self.data[self.data['Prison_Role_ID'].astype(str) != str(prison_id)]
        return self.save_data()
    
    def update_licensee(self, prison_id, updated_data):
        idx = self.data[self.data['Prison_Role_ID'].astype(str) == str(prison_id)].index
        if len(idx) > 0:
                for key, value in updated_data.items():
                    self.data.loc[idx[0], key] = value
                return self.save_data()
        return False

    def get_licensee_by_id(self, prison_id):
        result = self.data[self.data['Prison_Role_ID'].astype(str) == str(prison_id)]
        if not result.empty:
            return result.iloc[0].to_dict()
        return None
    def reload_data(self):
        self.reload_data()
    
    
    