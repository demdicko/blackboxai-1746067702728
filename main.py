import tkinter as tk
from tkinter import messagebox, ttk
from product_management import ProductManagement
from sales_management import SalesManagement
from client_management import ClientManagement
from stock_management import StockManagement
from supplier_management import SupplierManagement
from order_management import OrderManagement
from billing_management import BillingManagement
from reporting_management import ReportingManagement
from user_management import LoginWindow
from language_resources import LANG_FR, LANG_EN

class ToloDistributionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.language = LANG_FR  # Langue par défaut
        self.title(self.language["app_title"])
        self.geometry("800x600")
        self.withdraw()  # Masquer la fenêtre principale jusqu'à la connexion
        self.login_window = LoginWindow(self, self.on_login_success)
        self.login_window.grab_set()

    def on_login_success(self, role):
        self.deiconify()  # Afficher la fenêtre principale après connexion réussie
        self.user_role = role
        self.create_widgets()

    def create_widgets(self):
        # UI de base avec un label de bienvenue
        self.welcome_label = tk.Label(self, text=self.language["welcome_message"].format(role=self.user_role), font=("Arial", 16))
        self.welcome_label.pack(pady=20)

        # Sélecteur de langue
        self.create_language_selector()

        # Boutons de navigation
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        self.product_btn = tk.Button(btn_frame, text=self.language["manage_products"], width=20, command=self.manage_products)
        self.product_btn.grid(row=0, column=0, padx=5, pady=5)

        self.sales_btn = tk.Button(btn_frame, text=self.language["manage_sales"], width=20, command=self.manage_sales)
        self.sales_btn.grid(row=0, column=1, padx=5, pady=5)

        self.client_btn = tk.Button(btn_frame, text=self.language["manage_clients"], width=20, command=self.manage_clients)
        self.client_btn.grid(row=1, column=0, padx=5, pady=5)

        self.stock_btn = tk.Button(btn_frame, text=self.language["manage_stock"], width=20, command=self.manage_stock)
        self.stock_btn.grid(row=1, column=1, padx=5, pady=5)

        self.supplier_btn = tk.Button(btn_frame, text=self.language["manage_suppliers"], width=20, command=self.manage_suppliers)
        self.supplier_btn.grid(row=2, column=0, padx=5, pady=5)

        self.order_btn = tk.Button(btn_frame, text=self.language["manage_orders"], width=20, command=self.manage_orders)
        self.order_btn.grid(row=2, column=1, padx=5, pady=5)

        self.billing_btn = tk.Button(btn_frame, text=self.language["manage_billing"], width=20, command=self.manage_billing)
        self.billing_btn.grid(row=3, column=0, padx=5, pady=5)

        self.reporting_btn = tk.Button(btn_frame, text=self.language["manage_reporting"], width=20, command=self.manage_reporting)
        self.reporting_btn.grid(row=3, column=1, padx=5, pady=5)

    def create_language_selector(self):
        lang_frame = tk.Frame(self)
        lang_frame.pack(pady=5)
        tk.Label(lang_frame, text=self.language["select_language"]).pack(side=tk.LEFT)
        self.lang_var = tk.StringVar(value="fr")
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.lang_var, state="readonly", width=10)
        lang_combo['values'] = ("fr", "en")
        lang_combo.pack(side=tk.LEFT)
        lang_combo.bind("<<ComboboxSelected>>", self.change_language)

    def change_language(self, event=None):
        lang_code = self.lang_var.get()
        if lang_code == "fr":
            self.language = LANG_FR
        else:
            self.language = LANG_EN
        self.update_ui_language()

    def update_ui_language(self):
        self.title(self.language["app_title"])
        self.welcome_label.config(text=self.language["welcome_message"].format(role=self.user_role))
        self.product_btn.config(text=self.language["manage_products"])
        self.sales_btn.config(text=self.language["manage_sales"])
        self.client_btn.config(text=self.language["manage_clients"])
        self.stock_btn.config(text=self.language["manage_stock"])
        self.supplier_btn.config(text=self.language["manage_suppliers"])
        self.order_btn.config(text=self.language["manage_orders"])
        self.billing_btn.config(text=self.language["manage_billing"])
        self.reporting_btn.config(text=self.language["manage_reporting"])

    def manage_products(self):
        ProductManagement(self, self.language)

    def manage_sales(self):
        SalesManagement(self, self.language)

    def manage_clients(self):
        ClientManagement(self, self.language)

    def manage_stock(self):
        StockManagement(self, self.language)

    def manage_suppliers(self):
        SupplierManagement(self, self.language)

    def manage_orders(self):
        OrderManagement(self, self.language)

    def manage_billing(self):
        BillingManagement(self, self.language)

    def manage_reporting(self):
        ReportingManagement(self, self.language)

if __name__ == "__main__":
    app = ToloDistributionApp()
    app.mainloop()
