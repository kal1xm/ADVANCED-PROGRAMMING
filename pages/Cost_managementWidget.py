from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,QDialog, QLineEdit, QFormLayout, QDialogButtonBox, QFrame)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor

class SetBudgetDialog(QDialog):
    
    def __init__(self, current_budget: float, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Set Monthly Budget")
        self.setModal(True)
        self.setMinimumWidth(300)
        
        layout = QFormLayout()
        
        self.budget_input = QLineEdit()
        self.budget_input.setText(str(current_budget))
        
        layout.addRow("Monthly Budget (£):", self.budget_input)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.validate_and_accept)
        buttons.rejected.connect(self.reject)
        
        layout.addRow(buttons)
        self.setLayout(layout)
    
    def validate_and_accept(self):
        try:
            budget = float(self.budget_input.text())
            if budget < 0:
                raise ValueError()
        except ValueError:
            QMessageBox.warning(self, "Please enter a valid budget amount.")
            return
        
        self.accept()
    
    def get_budget(self):
        return float(self.budget_input.text())


class CostManagementWidget(QWidget):
    
    logout_signal = Signal()
    back_to_dashboard_signal = Signal()
    
    def __init__(self, cost_management_system):
        super().__init__()
        self.system = cost_management_system
        self.Cost_ui()
        self.refresh_display()
    
    def Cost_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Cost Management")
        title_font = QFont()
        title_font.setPointSize(32)
        title_font.setBold(True)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        logout_btn = QPushButton("LOGOUT")
        logout_btn.setFixedSize(100, 40)
        logout_btn.clicked.connect(self.logout_signal.emit)
        header_layout.addWidget(logout_btn)
        
        main_layout.addLayout(header_layout)
        
        summary_label = QLabel("Current period summary")
        summary_font = QFont()
        summary_font.setPointSize(18)
        summary_font.setBold(True)
        summary_label.setFont(summary_font)
        main_layout.addWidget(summary_label)
        
        self.daily_cost_label = QLabel("Total daily cost:")
        self.days_since_label = QLabel("Days since last payment:")
        self.period_total_label = QLabel("Current Period Total:")
        self.monthly_budget_label = QLabel("Monthly budget:")
        self.projected_monthly_label = QLabel("Projected monthly:")
        
        main_layout.addWidget(self.daily_cost_label)
        main_layout.addWidget(self.days_since_label)
        main_layout.addWidget(self.period_total_label)
        main_layout.addWidget(self.monthly_budget_label)
        main_layout.addWidget(self.projected_monthly_label)

        button_layout = QHBoxLayout()
        
        set_budget_btn = QPushButton("Set Monthly Budget")
        set_budget_btn.clicked.connect(self.set_budget)
        button_layout.addWidget(set_budget_btn)
        
        paid_btn = QPushButton("Paid")
        paid_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 8px 16px;")
        paid_btn.clicked.connect(self.make_payment)
        button_layout.addWidget(paid_btn)
        
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line)
        
        table_header_label = QLabel("RHU Name                    Licensees       Cost/Day       Period Total")
        table_header_font = QFont()
        table_header_font.setPointSize(12)
        table_header_font.setBold(True)
        table_header_label.setFont(table_header_font)
        main_layout.addWidget(table_header_label)
        
        self.rhu_table = QTableWidget()
        self.rhu_table.setColumnCount(4)
        self.rhu_table.setHorizontalHeaderLabels([
            "RHU Name", "Licensees", "Cost/Day", "Period Total"
        ])
        self.rhu_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.rhu_table.setAlternatingRowColors(True)
        self.rhu_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.rhu_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        main_layout.addWidget(self.rhu_table)
        
        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line2)
        
        self.last_payment_label = QLabel("Last payment:")
        self.next_payment_label = QLabel("Next Payment due:")
        
        payment_font = QFont()
        payment_font.setPointSize(11)
        self.last_payment_label.setFont(payment_font)
        self.next_payment_label.setFont(payment_font)
        
        main_layout.addWidget(self.last_payment_label)
        main_layout.addWidget(self.next_payment_label)
        
        
        main_layout.addStretch()
        
        self.setLayout(main_layout)
    
    def refresh_display(self):
        summary = self.system.get_summary_data()
        
        self.daily_cost_label.setText(
            f"Total daily cost: £{summary['total_daily_cost']:.2f}"
        )
        self.days_since_label.setText(
            f"Days since last payment: {summary['days_since_last_payment']}"
        )
        self.period_total_label.setText(
            f"Current Period Total: £{summary['current_period_total']:.2f}"
        )
        self.monthly_budget_label.setText(
            f"Monthly budget: £{summary['monthly_budget']:.2f}"
        )
        
        projected_text = f"Projected monthly: £{summary['projected_monthly']:.2f}"
        if summary['is_over_budget']:
            projected_text += f" (OVER BUDGET by £{summary['budget_variance']:.2f})"
            self.projected_monthly_label.setStyleSheet("color: red; font-weight: bold;")
        else:
            self.projected_monthly_label.setStyleSheet("")
        self.projected_monthly_label.setText(projected_text)
        
        self.last_payment_label.setText(f"Last payment: {summary['last_payment']}")
        self.next_payment_label.setText(f"Next Payment due: {summary['next_payment']}")
        
        self.populate_rhu_table(summary['rhu_summary'])
    
    def populate_rhu_table(self, rhu_summary):
        self.rhu_table.setRowCount(len(rhu_summary))
        
        for row, rhu in enumerate(rhu_summary):
            name_item = QTableWidgetItem(rhu['name'])
            self.rhu_table.setItem(row, 0, name_item)
            
            licensees_item = QTableWidgetItem(str(rhu['licensees']))
            self.rhu_table.setItem(row, 1, licensees_item)
            
            cost_item = QTableWidgetItem(f"£{rhu['cost_per_day']:.2f}")
            self.rhu_table.setItem(row, 2, cost_item)
            
            total_item = QTableWidgetItem(f"£{rhu['period_total']:.2f}")
            self.rhu_table.setItem(row, 3, total_item)
    
    def set_budget(self):
        current_budget = self.system.monthly_budget if hasattr(self.system, 'monthly_budget') else 0.0
        dialog = SetBudgetDialog(current_budget, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            budget = dialog.get_budget()
            if hasattr(self.system, 'set_monthly_budget'):
                self.system.set_monthly_budget(budget)
            QMessageBox.information(self, "Success", f"Monthly budget set to £{budget:.2f}")
            self.refresh_display()
    
    def make_payment(self):
        if hasattr(self.system, 'get_current_period_total'):
            amount = self.system.get_current_period_total()
        else:
            amount = 0.0
        
        reply = QMessageBox.question(
            self,
            "Confirm Payment",
            f"Process payment of £{amount:.2f}?\n\nThis will reset the current period.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if hasattr(self.system, 'make_payment'):
                paid_amount = self.system.make_payment()
                QMessageBox.information(
                    self, 
                    "Payment Processed", 
                    f"Payment of £{paid_amount:.2f} has been recorded.\nPeriod has been reset."
                )
            self.refresh_display()


