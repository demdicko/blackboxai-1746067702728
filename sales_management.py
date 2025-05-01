import tkinter as tk
from tkinter import ttk, messagebox
import database
import datetime

class SalesManagement(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Sales Management")
        self.geometry("900x600")
        self.conn = database.create_connection()
        self.create_widgets()
        self.load_products()
        self.load_clients()

    def create_widgets(self):
        # Product selection
        product_frame = tk.Frame(self)
        product_frame.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(product_frame, text="Select Product:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.product_var = tk.StringVar()
        self.product_combo = ttk.Combobox(product_frame, textvariable=self.product_var, state="readonly")
        self.product_combo.grid(row=0, column=1, padx=5, pady=5)
        self.product_combo.bind("<<ComboboxSelected>>", self.on_product_selected)

        tk.Label(product_frame, text="Available Stock:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.stock_label = tk.Label(product_frame, text="0")
        self.stock_label.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(product_frame, text="Quantity:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.quantity_var = tk.IntVar(value=1)
        self.quantity_entry = tk.Entry(product_frame, textvariable=self.quantity_var)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        # Payment method
        tk.Label(product_frame, text="Payment Method:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.payment_var = tk.StringVar()
        self.payment_combo = ttk.Combobox(product_frame, textvariable=self.payment_var, state="readonly")
        self.payment_combo['values'] = ("Espèces", "Mobile Money", "Crédit")
        self.payment_combo.grid(row=2, column=1, padx=5, pady=5)
        self.payment_combo.current(0)

        # Client selection (optional for credit)
        tk.Label(product_frame, text="Client (for credit):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.client_var = tk.StringVar()
        self.client_combo = ttk.Combobox(product_frame, textvariable=self.client_var, state="readonly")
        self.client_combo.grid(row=3, column=1, padx=5, pady=5)

        # Total amount display
        tk.Label(product_frame, text="Total Amount:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.total_amount_var = tk.DoubleVar(value=0.0)
        self.total_amount_label = tk.Label(product_frame, textvariable=self.total_amount_var)
        self.total_amount_label.grid(row=4, column=1, padx=5, pady=5)

        # Buttons
        btn_frame = tk.Frame(product_frame)
        btn_frame.grid(row=5, column=0, columnspan=4, pady=10)

        self.add_sale_btn = tk.Button(btn_frame, text="Record Sale", command=self.record_sale)
        self.add_sale_btn.pack(side=tk.LEFT, padx=5)

        self.clear_btn = tk.Button(btn_frame, text="Clear", command=self.clear_form)
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        # Sales list
        self.tree = ttk.Treeview(self, columns=("ID", "Date", "Product", "Quantity", "Total Amount", "Payment Method", "Client", "Profit"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=30)
        self.tree.heading("Date", text="Date")
        self.tree.heading("Product", text="Product")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Total Amount", text="Total Amount")
        self.tree.heading("Payment Method", text="Payment Method")
        self.tree.heading("Client", text="Client")
        self.tree.heading("Profit", text="Profit")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.load_sales()

    def load_products(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, reference, sale_price, stock_quantity, purchase_price FROM products")
        self.products = cursor.fetchall()
        product_refs = [p[1] for p in self.products]
        self.product_combo['values'] = product_refs
        if product_refs:
            self.product_combo.current(0)
            self.on_product_selected()

    def load_clients(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name FROM clients")
        self.clients = cursor.fetchall()
        client_names = [c[1] for c in self.clients]
        self.client_combo['values'] = client_names
        if client_names:
            self.client_combo.current(0)

    def on_product_selected(self, event=None):
        selected_ref = self.product_var.get()
        product = next((p for p in self.products if p[1] == selected_ref), None)
        if product:
            self.stock_label.config(text=str(product[3]))
            self.update_total_amount()

    def update_total_amount(self):
        try:
            quantity = self.quantity_var.get()
            selected_ref = self.product_var.get()
            product = next((p for p in self.products if p[1] == selected_ref), None)
            if product and quantity > 0:
                total = product[2] * quantity
                self.total_amount_var.set(total)
            else:
                self.total_amount_var.set(0.0)
        except Exception:
            self.total_amount_var.set(0.0)

    def clear_form(self):
        if self.product_combo['values']:
            self.product_combo.current(0)
        if self.client_combo['values']:
            self.client_combo.current(0)
        self.quantity_var.set(1)
        self.payment_combo.current(0)
        self.total_amount_var.set(0.0)
        self.stock_label.config(text="0")

    def record_sale(self):
        selected_ref = self.product_var.get()
        quantity = self.quantity_var.get()
        payment_method = self.payment_var.get()
        client_name = self.client_var.get() if payment_method == "Crédit" else None

        product = next((p for p in self.products if p[1] == selected_ref), None)
        if not product:
            messagebox.showerror("Error", "Please select a valid product.")
            return

        if quantity <= 0:
            messagebox.showerror("Error", "Quantity must be greater than zero.")
            return

        if quantity > product[3]:
            messagebox.showerror("Error", "Insufficient stock for the selected product.")
            return

        client_id = None
        if client_name:
            client = next((c for c in self.clients if c[1] == client_name), None)
            if client:
                client_id = client[0]
            else:
                messagebox.showerror("Error", "Selected client not found.")
                return

        total_amount = product[2] * quantity
        profit = (product[2] - product[4]) * quantity
        date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO sales (date, total_amount, payment_method, client_id, profit)
                VALUES (?, ?, ?, ?, ?)
            """, (date_str, total_amount, payment_method, client_id, profit))

            # Update stock quantity
            new_stock = product[3] - quantity
            cursor.execute("""
                UPDATE products SET stock_quantity = ? WHERE id = ?
            """, (new_stock, product[0]))

            # Update client credit balance if payment is credit
            if payment_method == "Crédit" and client_id:
                cursor.execute("""
                    UPDATE clients SET credit_balance = credit_balance + ? WHERE id = ?
                """, (total_amount, client_id))

            self.conn.commit()
            messagebox.showinfo("Success", "Sale recorded successfully.")
            self.load_sales()
            self.load_products()
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to record sale: {e}")

    def load_sales(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT s.id, s.date, p.reference, s.total_amount / p.sale_price * s.total_amount, s.total_amount, s.payment_method, c.name, s.profit
            FROM sales s
            LEFT JOIN products p ON s.id = p.id
            LEFT JOIN clients c ON s.client_id = c.id
            ORDER BY s.date DESC
        """)
        rows = cursor.fetchall()
        for row in rows:
            self.tree.insert("", tk.END, values=row)
