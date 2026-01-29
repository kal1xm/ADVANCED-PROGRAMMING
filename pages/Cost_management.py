from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
import pandas as pd
from datetime import datetime, timedelta

class CostManagement():
    def __init__(self):
        self.data = pd.read_csv('On_Licence_Housing_Data.csv')
    
    
