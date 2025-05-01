import tkinter as tk
from tkinter import ttk, messagebox
import database

class SupplierManagement(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Supplier Management")
        self.geometry("800x500")
        self.conn = database.create_connection()
        self.create_widgets()
        self.load_suppliers()

    def create_widgets(self):
        # Supplier form
        form_frame = tk.Frame(self)
        form_frame.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(form_frame, textvariable=self.name_var)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Contact Info:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.contact_var = tk.StringVar()
        self.contact_entry = tk.Entry(form_frame, textvariable=self.contact_var)
        self.contact_entry.grid(row=1, column=1, padx=5, pady=5)

        # Buttons
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

        self.add_btn = tk.Button(btn_frame, text="Add Supplier", command=self.add_supplier)
        self.add_btn.pack(side=tk.LEFT, padx=5)

        self.update_btn = tk.Button(btn_frame, text="Update Supplier", command=self.update_supplier, state=tk.DISABLED)
        self.update_btn.pack(side=tk.LEFT, padx=5)

        self.delete_btn = tk.Button(btn_frame, text="Delete Supplier", command=self.delete_supplier, state=tk.DISABLED)
        self.delete_btn.pack(side=tk.LEFT, padx=5)

        # Supplier list
        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Contact Info"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=30)
        self.tree.heading("Name", text="Name")
        self.tree.heading("Contact Info", text="Contact Info")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def load_suppliers(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, contact_info FROM suppliers")
        rows = cursor.fetchall()
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def clear_form(self):
        self.name_var.set("")
        self.contact_var.set("")
        self.add_btn.config(state=tk.NORMAL)
        self.update_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item['values']
            self.selected_id = values[0]
            self.name_var.set(values[1])
            self.contact_var.set(values[2])
            self.add_btn.config(state=tk.DISABLED)
            self.update_btn.config(state=tk.NORMAL)
            self.delete_btn.config(state=tk.NORMAL)
        else:
            self.clear_form()

    def add_supplier(self):
        name = self.name_var.get()
        contact = self.contact_var.get()

        if not name:
            messagebox.showerror("Error", "Name is required.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO suppliers (name, contact_info)
                VALUES (?, ?)
            """, (name, contact))
            self.conn.commit()
            messagebox.showinfo("Success", "Supplier added successfully.")
            self.load_suppliers()
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add supplier: {e}")

    def update_supplier(self):
        name = self.name_var.get()
        contact = self.contact_var.get()

        if not name:
            messagebox.showerror("Error", "Name is required.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE suppliers
                SET name = ?, contact_info = ?
                WHERE id = ?
            """, (name, contact, self.selected_id))
            self.conn.commit()
            messagebox.showinfo("Success", "Supplier updated successfully.")
            self.load_suppliers()
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update supplier: {e}")

    def delete_supplier(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM suppliers WHERE id = ?", (self.selected_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Supplier deleted successfully.")
            self.load_suppliers()
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete supplier: {e}")
