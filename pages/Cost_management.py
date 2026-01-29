from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
import pandas as pd
from datetime import datetime, timedelta

class CostManagement():
    def __init__(self):
        self.data = pd.read_csv('On_Licence_Housing_Data.csv')

        self.location_costs = {
            'Congleton Hostel': 45.00,
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

        
    
    