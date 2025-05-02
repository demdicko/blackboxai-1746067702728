import tkinter as tk
from tkinter import ttk, messagebox
import database
import datetime

class StockManagement(tk.Toplevel):
    def __init__(self, master=None, language=None):
        super().__init__(master)
        self.language = language or {}
        self.title(self.language.get("stock_management_title", "Stock Management"))
        self.geometry("900x600")
        self.conn = database.create_connection()
        self.create_widgets()
        self.load_products()
        self.load_suppliers()
        self.load_stock_entries()

    def create_widgets(self):
        # Stock entry form
        form_frame = tk.Frame(self)
        form_frame.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(form_frame, text=self.language.get("select_product_label", "Select Product:")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.product_var = tk.StringVar()
        self.product_combo = ttk.Combobox(form_frame, textvariable=self.product_var, state="readonly")
        self.product_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text=self.language.get("quantity_label", "Quantity:")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.quantity_var = tk.IntVar(value=1)
        self.quantity_entry = tk.Entry(form_frame, textvariable=self.quantity_var)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text=self.language.get("select_supplier_label", "Select Supplier:")).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.supplier_var = tk.StringVar()
        self.supplier_combo = ttk.Combobox(form_frame, textvariable=self.supplier_var, state="readonly")
        self.supplier_combo.grid(row=2, column=1, padx=5, pady=5)

        # Buttons
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        self.add_btn = tk.Button(btn_frame, text=self.language.get("add_stock_entry_btn", "Add Stock Entry"), command=self.add_stock_entry)
        self.add_btn.pack(side=tk.LEFT, padx=5)

        self.clear_btn = tk.Button(btn_frame, text=self.language.get("clear_btn", "Clear"), command=self.clear_form)
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        # Stock entries list
        self.tree = ttk.Treeview(self, columns=("ID", "Date", "Product", "Quantity", "Supplier"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=30)
        self.tree.heading("Date", text=self.language.get("date_label", "Date"))
        self.tree.heading("Product", text=self.language.get("product_label", "Product"))
        self.tree.heading("Quantity", text=self.language.get("quantity_label", "Quantity"))
        self.tree.heading("Supplier", text=self.language.get("supplier_label", "Supplier"))
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def load_products(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, reference FROM products")
        self.products = cursor.fetchall()
        product_refs = [p[1] for p in self.products]
        self.product_combo['values'] = product_refs
        if product_refs:
            self.product_combo.current(0)

    def load_suppliers(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name FROM suppliers")
        self.suppliers = cursor.fetchall()
        supplier_names = [s[1] for s in self.suppliers]
        self.supplier_combo['values'] = supplier_names
        if supplier_names:
            self.supplier_combo.current(0)

    def load_stock_entries(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT se.id, se.date, p.reference, se.quantity, s.name
            FROM stock_entries se
            LEFT JOIN products p ON se.product_id = p.id
            LEFT JOIN suppliers s ON se.supplier_id = s.id
            ORDER BY se.date DESC
        """)
        rows = cursor.fetchall()
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def clear_form(self):
        if self.product_combo['values']:
            self.product_combo.current(0)
        if self.supplier_combo['values']:
            self.supplier_combo.current(0)
        self.quantity_var.set(1)

    def add_stock_entry(self):
        product_ref = self.product_var.get()
        quantity = self.quantity_var.get()
        supplier_name = self.supplier_var.get()

        if not product_ref or quantity <= 0:
            messagebox.showerror(self.language.get("error", "Error"), self.language.get("error_select_product_quantity", "Please select a product and enter a valid quantity."))
            return

        product = next((p for p in self.products if p[1] == product_ref), None)
        supplier = next((s for s in self.suppliers if s[1] == supplier_name), None)

        if not product:
            messagebox.showerror(self.language.get("error", "Error"), self.language.get("error_product_not_found", "Selected product not found."))
            return

        supplier_id = supplier[0] if supplier else None

        date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO stock_entries (product_id, quantity, date, supplier_id)
                VALUES (?, ?, ?, ?)
            """, (product[0], quantity, date_str, supplier_id))

            # Update product stock quantity
            cursor.execute("SELECT stock_quantity FROM products WHERE id = ?", (product[0],))
            current_stock = cursor.fetchone()[0]
            new_stock = current_stock + quantity
            cursor.execute("UPDATE products SET stock_quantity = ? WHERE id = ?", (new_stock, product[0]))

            self.conn.commit()
            messagebox.showinfo(self.language.get("success", "Success"), self.language.get("success_stock_entry_added", "Stock entry added successfully."))
            self.load_stock_entries()
            self.clear_form()
        except Exception as e:
            messagebox.showerror(self.language.get("error", "Error"), f"{self.language.get('error')}: {e}")
</create_file>
