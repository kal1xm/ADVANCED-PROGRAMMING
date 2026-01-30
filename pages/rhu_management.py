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


    
    
