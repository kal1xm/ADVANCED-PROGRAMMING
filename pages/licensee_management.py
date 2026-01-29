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
            self.data['Prison_Role_ID'].astype(str).str.lower().str.contains(SearchData, na=False),
            self.data['Name'].astype(str).str.lower().str.contains(SearchData, na=False),
            self.data['Male'].astype(str).str.lower().str.contains(SearchData, na=False),
            self.data['Women'].astype(str).str.lower().str.contains(SearchData, na=False),
            self.data['Category'].astype(str).str.lower().str.contains(SearchData, na=False),
            self.data['Release_Date'].astype(str).str.lower().str.contains(SearchData, na=False),
            self.data['Expected_End_of_License'].astype(str).str.lower().str.contains(SearchData, na=False),
            self.data['Current_Location'].astype(str).str.lower().str.contains(SearchData, na=False),
            self.data['Nighttime_Curfew_Restrictions'].astype(str).str.lower().str.contains(SearchData, na=False),
            self.data['Weekend_Curfew_Restrictions'].astype(str).str.lower().str.contains(SearchData, na=False),
            self.data['Male'].astype(str).str.lower().str.contains(SearchData, na=False),