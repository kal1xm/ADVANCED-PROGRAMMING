#kallumleew24023993
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
import pandas as pd
from datetime import datetime, timedelta
import os

csv_path = os.path.join('On_Licence_Housing_Data.xlsx')

class ReleaseManagement:
    def __init__(self):
        self.csv_path = csv_path
        try:
            self.data = pd.read_excel(csv_path)
            if 'Release_Date' in self.data.columns:
                self.data['Release_Date'] = pd.to_datetime(self.data['Release_Date'], errors='coerce')
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            self.data = pd.DataFrame()
        
        self.previous_dates = {}
    
    def load_data(self):
        try:
            self.data = pd.read_excel(self.csv_path)
            if 'Release_Date' in self.data.columns:
                self.data['Release_Date'] = pd.to_datetime(self.data['Release_Date'], errors='coerce')
        except Exception as e:
            print(f"Error loading Excel file: {e}")
    
    def save_data(self):
        try:
            self.data.to_excel(self.csv_path, index=False)
            return True
        except Exception as e:
            print(f"Error saving Excel file: {e}")
            return False
    
    def get_upcoming_releases(self, days_ahead=90):
        if self.data.empty or 'Release_Date' not in self.data.columns:
            return pd.DataFrame()
        
        today = datetime.now()
        future_date = today + timedelta(days=days_ahead)
        
        upcoming = self.data[
            (self.data['Release_Date'] >= today) & 
            (self.data['Release_Date'] <= future_date)
        ].copy()
        
        upcoming['Days_Until_Release'] = (upcoming['Release_Date'] - today).dt.days
        upcoming = upcoming.sort_values('Release_Date')
        
        return upcoming
    
    def get_releases_by_rhu(self, rhu_name=None):
        upcoming = self.get_upcoming_releases()
        
        if upcoming.empty:
            return {}
        
        if rhu_name and rhu_name != "All RHUs":
            upcoming = upcoming[upcoming['Current_Location'] == rhu_name]
        
        # Group by RHU
        grouped = {}
        for location in upcoming['Current_Location'].unique():
            if pd.notna(location):
                rhu_releases = upcoming[upcoming['Current_Location'] == location]
                grouped[location] = rhu_releases
        
        return grouped
    
    def get_unique_rhus(self):
        if self.data.empty or 'Current_Location' not in self.data.columns:
            return []
        
        rhus = self.data['Current_Location'].dropna().unique().tolist()
        return sorted(rhus)
    
    def search_releases(self, search_text):
        upcoming = self.get_upcoming_releases()
        
        if upcoming.empty or not search_text:
            return upcoming
        
        search_lower = search_text.lower()
        
        mask = (
            upcoming['Name'].astype(str).str.lower().str.contains(search_lower, na=False) |
            upcoming['Prison_Role_ID'].astype(str).str.lower().str.contains(search_lower, na=False) |
            upcoming['Current_Location'].astype(str).str.lower().str.contains(search_lower, na=False)
        )
        
        return upcoming[mask]
    
    def update_release_date(self, prison_id, new_date):
        try:
            idx = self.data[self.data['Prison_Role_ID'].astype(str) == str(prison_id)].index
            
            if len(idx) == 0:
                return False, "Licensee not found"
            
            idx = idx[0]
            old_date = self.data.loc[idx, 'Release_Date']
            
            self.previous_dates[prison_id] = old_date
            
            self.data.loc[idx, 'Release_Date'] = pd.to_datetime(new_date)
            
            warning = ""
            if pd.notna(old_date) and new_date > old_date:
                days_increase = (new_date - old_date).days
                warning = f"WARNING: Release date increased by {days_increase} days. This is rare and should be verified."
            
            success = self.save_data()
            return success, warning
            
        except Exception as e:
            return False, f"Error updating date: {str(e)}"
    
    def get_licensee_details(self, prison_id):
        result = self.data[self.data['Prison_Role_ID'].astype(str) == str(prison_id)]
        
        if not result.empty:
            return result.iloc[0].to_dict()
        return None
    
    def get_rhu_contact_info(self, rhu_name):
       
        contact_info = {
            'Wolverine House': {'email': 'wolverine@rhu.gov.uk', 'phone': '07142643983'},
            'HMP Low Newton': {'email': 'lownewton@hmp.gov.uk', 'phone': '077152523834'},
            'Northumbria Facility': {'email': 'northumbria@rhu.gov.uk', 'phone': '07242985353'},
            'Congleton Hostel': {'email': 'congleton@hostel.gov.uk', 'phone': '07619525253'}
        }
        
        return contact_info.get(rhu_name, {'email': 'unknown@rhu.gov.uk', 'phone': 'N/A'})
    