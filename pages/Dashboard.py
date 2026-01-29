from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
import pandas as pd
from datetime import datetime, timedelta
from .Cost_management import CostManagement
import os



csv_path = os.path.join('On_Licence_Housing_Data.xlsx')

class Dashboard:
    def __init__(self):
        self.data = pd.read_excel(csv_path)
        self.cost_manage = CostManagement()

    def get_pending_allocation(self):
        pending = self.data[self.data['Status'] == 'Pending'].shape[0]
        return pending
    

    def get_currently_allocated(self):
         allocated = self.data[self.data['Status'] == 'Allocated'].shape[0]
         return allocated
    
    def get_month_released(self):
        today = datetime.now()
        month = today + timedelta(days=30)
    
        self.data['Release_Date'] = pd.to_datetime(self.data['Release_Date'])
            
        releaseday = self.data[
                (self.data['Release_Date'] >= today) & 
                (self.data['Release_Date'] <= month)].shape[0]
            
        return releaseday
    
    def get_daily_cost(self):
        total_cost = self.cost_manage.RMU_Costs()
        return total_cost
    
    