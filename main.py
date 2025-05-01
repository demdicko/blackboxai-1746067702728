import tkinter as tk
from tkinter import messagebox
from product_management import ProductManagement
from sales_management import SalesManagement
from client_management import ClientManagement
from stock_management import StockManagement
from supplier_management import SupplierManagement
from order_management import OrderManagement
from billing_management import BillingManagement
from reporting_management import ReportingManagement
from user_management import LoginWindow

class ToloDistributionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tolo Distribution Management")
        self.geometry("800x600")
        self.withdraw()  # Hide main window until login
        self.login_window = LoginWindow(self, self.on_login_success)
        self.login_window.grab_set()

    def on_login_success(self, role):
        self.deiconify()  # Show main window after successful login
        self.user_role = role
        self.create_widgets()

    def create_widgets(self):
        # Basic UI skeleton with a welcome label
        welcome_label = tk.Label(self, text=f"Welcome to Tolo Distribution Management System - Role: {self.user_role}", font=("Arial", 16))
        welcome_label.pack(pady=20)

        # Placeholder for future navigation buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        product_btn = tk.Button(btn_frame, text="Manage Products", width=20, command=self.manage_products)
        product_btn.grid(row=0, column=0, padx=5, pady=5)

        sales_btn = tk.Button(btn_frame, text="Manage Sales", width=20, command=self.manage_sales)
        sales_btn.grid(row=0, column=1, padx=5, pady=5)

        client_btn = tk.Button(btn_frame, text="Manage Clients", width=20, command=self.manage_clients)
        client_btn.grid(row=1, column=0, padx=5, pady=5)

        stock_btn = tk.Button(btn_frame, text="Manage Stock", width=20, command=self.manage_stock)
        stock_btn.grid(row=1, column=1, padx=5, pady=5)

        supplier_btn = tk.Button(btn_frame, text="Manage Suppliers", width=20, command=self.manage_suppliers)
        supplier_btn.grid(row=2, column=0, padx=5, pady=5)

        order_btn = tk.Button(btn_frame, text="Manage Orders", width=20, command=self.manage_orders)
        order_btn.grid(row=2, column=1, padx=5, pady=5)

        billing_btn = tk.Button(btn_frame, text="Billing & Invoicing", width=20, command=self.manage_billing)
        billing_btn.grid(row=3, column=0, padx=5, pady=5)

        reporting_btn = tk.Button(btn_frame, text="Reporting & Statistics", width=20, command=self.manage_reporting)
        reporting_btn.grid(row=3, column=1, padx=5, pady=5)

    def manage_products(self):
        ProductManagement(self)

    def manage_sales(self):
        SalesManagement(self)

    def manage_clients(self):
        ClientManagement(self)

    def manage_stock(self):
        StockManagement(self)

    def manage_suppliers(self):
        SupplierManagement(self)

    def manage_orders(self):
        OrderManagement(self)

    def manage_billing(self):
        BillingManagement(self)

    def manage_reporting(self):
        ReportingManagement(self)

if __name__ == "__main__":
    app = ToloDistributionApp()
    app.mainloop()
