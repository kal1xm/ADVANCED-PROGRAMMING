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

