import tkinter as tk
from tkinter import ttk, messagebox
import database

class ProductManagement(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Product Management")
        self.geometry("800x500")
        self.conn = database.create_connection()
        self.create_widgets()
        self.load_products()

    def create_widgets(self):
        # Product form
        form_frame = tk.Frame(self)
        form_frame.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(form_frame, text="Category:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.category_var = tk.StringVar()
        self.category_entry = ttk.Combobox(form_frame, textvariable=self.category_var)
        self.category_entry['values'] = ("Electroménager", "Téléphones", "Accessoires", "Divers")
        self.category_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Reference:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.reference_var = tk.StringVar()
        self.reference_entry = tk.Entry(form_frame, textvariable=self.reference_var)
        self.reference_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Purchase Price:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.purchase_price_var = tk.DoubleVar()
        self.purchase_price_entry = tk.Entry(form_frame, textvariable=self.purchase_price_var)
        self.purchase_price_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Sale Price:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.sale_price_var = tk.DoubleVar()
        self.sale_price_entry = tk.Entry(form_frame, textvariable=self.sale_price_var)
        self.sale_price_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Stock Quantity:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.stock_quantity_var = tk.IntVar()
        self.stock_quantity_entry = tk.Entry(form_frame, textvariable=self.stock_quantity_var)
        self.stock_quantity_entry.grid(row=4, column=1, padx=5, pady=5)

        # Buttons
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)

        self.add_btn = tk.Button(btn_frame, text="Add Product", command=self.add_product)
        self.add_btn.pack(side=tk.LEFT, padx=5)

        self.update_btn = tk.Button(btn_frame, text="Update Product", command=self.update_product, state=tk.DISABLED)
        self.update_btn.pack(side=tk.LEFT, padx=5)

        self.delete_btn = tk.Button(btn_frame, text="Delete Product", command=self.delete_product, state=tk.DISABLED)
        self.delete_btn.pack(side=tk.LEFT, padx=5)

        # Product list
        self.tree = ttk.Treeview(self, columns=("ID", "Category", "Reference", "Purchase Price", "Sale Price", "Stock Quantity", "Profit"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=30)
        self.tree.heading("Category", text="Category")
        self.tree.heading("Reference", text="Reference")
        self.tree.heading("Purchase Price", text="Purchase Price")
        self.tree.heading("Sale Price", text="Sale Price")
        self.tree.heading("Stock Quantity", text="Stock Quantity")
        self.tree.heading("Profit", text="Profit")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def load_products(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, category, reference, purchase_price, sale_price, stock_quantity, (sale_price - purchase_price) as profit FROM products")
        rows = cursor.fetchall()
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def clear_form(self):
        self.category_var.set("")
        self.reference_var.set("")
        self.purchase_price_var.set(0.0)
        self.sale_price_var.set(0.0)
        self.stock_quantity_var.set(0)
        self.add_btn.config(state=tk.NORMAL)
        self.update_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item['values']
            self.selected_id = values[0]
            self.category_var.set(values[1])
            self.reference_var.set(values[2])
            self.purchase_price_var.set(values[3])
            self.sale_price_var.set(values[4])
            self.stock_quantity_var.set(values[5])
            self.add_btn.config(state=tk.DISABLED)
            self.update_btn.config(state=tk.NORMAL)
            self.delete_btn.config(state=tk.NORMAL)
        else:
            self.clear_form()

    def add_product(self):
        category = self.category_var.get()
        reference = self.reference_var.get()
        purchase_price = self.purchase_price_var.get()
        sale_price = self.sale_price_var.get()
        stock_quantity = self.stock_quantity_var.get()
        profit = sale_price - purchase_price

        if not category or not reference:
            messagebox.showerror("Error", "Category and Reference are required.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO products (category, reference, purchase_price, sale_price, stock_quantity, profit_per_unit)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (category, reference, purchase_price, sale_price, stock_quantity, profit))
            self.conn.commit()
            messagebox.showinfo("Success", "Product added successfully.")
            self.load_products()
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add product: {e}")

    def update_product(self):
        category = self.category_var.get()
        reference = self.reference_var.get()
        purchase_price = self.purchase_price_var.get()
        sale_price = self.sale_price_var.get()
        stock_quantity = self.stock_quantity_var.get()
        profit = sale_price - purchase_price

        if not category or not reference:
            messagebox.showerror("Error", "Category and Reference are required.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE products
                SET category = ?, reference = ?, purchase_price = ?, sale_price = ?, stock_quantity = ?, profit_per_unit = ?
                WHERE id = ?
            """, (category, reference, purchase_price, sale_price, stock_quantity, profit, self.selected_id))
            self.conn.commit()
            messagebox.showinfo("Success", "Product updated successfully.")
            self.load_products()
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update product: {e}")

    def delete_product(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM products WHERE id = ?", (self.selected_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Product deleted successfully.")
            self.load_products()
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete product: {e}")
