from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
import pandas as pd
from datetime import datetime, timedelta

class Dashboard:
    def __init__(self):
        self.data = pd.read_csv('On_Licence_Housing_Data.csv')


    def get_pending_allocation(self):
        pending = self.data[self.data['Current_Location'] == 'Congleton Hostel'].shape[0]
        return pending
    

    def get_currently_allocated(self):
         allocated = self.data[self.data['Current_Location'].notna()].shape[0]
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
        #pull from cost management when the code is done