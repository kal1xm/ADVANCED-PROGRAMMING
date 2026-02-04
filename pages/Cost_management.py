#kallumleew24023993
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
import pandas as pd
from datetime import datetime, timedelta
import os

csv_path = os.path.join('On_Licence_Housing_Data.xlsx')


class CostManagement:
    def __init__(self):
        self.csv_path = csv_path
        
        try:
            self.data = pd.read_excel(csv_path)
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            self.data = pd.DataFrame()
        
        self.location_costs = {
            'Congleton Hostel': 52.00,
            'HMP Low Newton': 38.00,
            'Northumbria facility': 58.00,
            'Wolverine House': 52.00,
        }
        
        self.monthly_budget = 0.0
        self.last_payment_date = None
        self.next_payment_date = None
    
    def RMU_Costs(self):
        total_cost = 0
        
        for index, row in self.data.iterrows():
            location = row['Current_Location']
            if pd.notna(location) and location in self.location_costs:
                total_cost += self.location_costs[location]
        
        return total_cost
    
    def get_cost_location(self, location):
        return self.location_costs.get(location, 0)
    
    def get_location_costs(self):
        return self.location_costs
    
    def get_location_summary(self):
        location_counts = {}
        
        for index, row in self.data.iterrows():
            location = row['Current_Location']
            if pd.notna(location) and location in self.location_costs:
                if location not in location_counts:
                    location_counts[location] = 0
                location_counts[location] += 1
        
        days = self.get_days_since_last_payment()
        summary = []
        
        for location, count in location_counts.items():
            cost_per_day = self.location_costs[location] * count
            summary.append({
                'name': location,
                'licensees': count,
                'cost_per_day': cost_per_day,
                'period_total': cost_per_day * days
            })
        
        return summary
    
    def get_total_daily_cost(self):
        return self.RMU_Costs()
    
    def get_days_since_last_payment(self):
        if self.last_payment_date is None:
            return 0
        return (datetime.now() - self.last_payment_date).days
    
    def get_current_period_total(self):
        days = self.get_days_since_last_payment()
        return self.get_total_daily_cost() * days
    
    def get_projected_monthly_cost(self):
        return self.get_total_daily_cost() * 30
    
    def is_over_budget(self):
        if self.monthly_budget <= 0:
            return False
        return self.get_projected_monthly_cost() > self.monthly_budget
    
    def get_budget_variance(self):
        return self.get_projected_monthly_cost() - self.monthly_budget
    
    def get_budget_percentage(self):
        if self.monthly_budget <= 0:
            return 0.0
        return (self.get_projected_monthly_cost() / self.monthly_budget) * 100
    
    def set_monthly_budget(self, budget):
        self.monthly_budget = budget
    
    def set_last_payment_date(self, date):
        self.last_payment_date = date
    
    def set_next_payment_date(self, date):
        self.next_payment_date = date
    
    def make_payment(self):
        amount = self.get_current_period_total()
        self.last_payment_date = datetime.now()
        self.next_payment_date = datetime.now() + timedelta(days=30)
        return amount
    
    def get_summary_data(self):
        return {
            'total_daily_cost': self.get_total_daily_cost(),
            'days_since_last_payment': self.get_days_since_last_payment(),
            'current_period_total': self.get_current_period_total(),
            'monthly_budget': self.monthly_budget,
            'projected_monthly': self.get_projected_monthly_cost(),
            'is_over_budget': self.is_over_budget(),
            'budget_variance': self.get_budget_variance(),
            'budget_percentage': self.get_budget_percentage(),
            'last_payment': self.last_payment_date.strftime('%d/%m/%Y') if self.last_payment_date else 'N/A',
            'next_payment': self.next_payment_date.strftime('%d/%m/%Y %H:%M') if self.next_payment_date else 'N/A',
            'rhu_summary': self.get_location_summary()
        }