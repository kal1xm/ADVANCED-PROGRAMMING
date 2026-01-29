from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
import pandas as pd
from datetime import datetime, timedelta
import os


csv_path = os.path.join('On_Licence_Housing_Data.xlsx')



class CostManagement():
    def __init__(self):
        self.data = pd.read_excel(csv_path)

        self.location_costs = {
            'Congleton Hostel': 52.00,
            'HMP Low Newton': 38.00,
            'Northumbria facility': 58.00,
            'Wolverine House': 52.00,
        }


    def RMU_Costs(self):
        total_cost = 0
        
        for index, row in self.data.iterrows():
            location = row['Current_Location']
            if pd.notna(location) and location in self.location_costs:
                total_cost += self.location_costs[location]
        
        return total_cost

        
    def get_cost_location(self, location):
        self.location_costs.get(location, 0)

    def location_costs(self):
        return self.location_costs
    
    