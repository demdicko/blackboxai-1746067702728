import tkinter as tk
from tkinter import ttk, messagebox
import database
import datetime

class OrderManagement(tk.Toplevel):
    def __init__(self, master=None, language=None):
        super().__init__(master)
        self.language = language or {}
        self.title(self.language.get("order_management_title", "Order Management"))
        self.geometry("900x600")
        self.conn = database.create_connection()
        self.create_widgets()
        self.load_clients()
        self.load_orders()

    def create_widgets(self):
        # Order form
        form_frame = tk.Frame(self)
        form_frame.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(form_frame, text=self.language.get("select_client_label", "Select Client:")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.client_var = tk.StringVar()
        self.client_combo = ttk.Combobox(form_frame, textvariable=self.client_var, state="readonly")
        self.client_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text=self.language.get("order_details_label", "Order Details:")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.order_details_text = tk.Text(form_frame, height=5, width=50)
        self.order_details_text.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text=self.language.get("status_label", "Status:")).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.status_var = tk.StringVar()
        self.status_combo = ttk.Combobox(form_frame, textvariable=self.status_var, state="readonly")
        self.status_combo['values'] = (
            self.language.get("status_pending", "Pending"),
            self.language.get("status_in_progress", "In Progress"),
            self.language.get("status_delivered", "Delivered"),
            self.language.get("status_cancelled", "Cancelled"),
        )
        self.status_combo.grid(row=2, column=1, padx=5, pady=5)
        self.status_combo.current(0)

        # Buttons
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        self.add_btn = tk.Button(btn_frame, text=self.language.get("add_order_btn", "Add Order"), command=self.add_order)
        self.add_btn.pack(side=tk.LEFT, padx=5)

        self.update_btn = tk.Button(btn_frame, text=self.language.get("update_order_btn", "Update Order"), command=self.update_order, state=tk.DISABLED)
        self.update_btn.pack(side=tk.LEFT, padx=5)

        self.delete_btn = tk.Button(btn_frame, text=self.language.get("delete_order_btn", "Delete Order"), command=self.delete_order, state=tk.DISABLED)
        self.delete_btn.pack(side=tk.LEFT, padx=5)

        # Order list
        self.tree = ttk.Treeview(self, columns=("ID", "Client", "Order Details", "Status", "Date"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=30)
        self.tree.heading("Client", text=self.language.get("client_label", "Client"))
        self.tree.heading("Order Details", text=self.language.get("order_details_label", "Order Details"))
        self.tree.heading("Status", text=self.language.get("status_label", "Status"))
        self.tree.heading("Date", text=self.language.get("date_label", "Date"))
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def load_clients(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name FROM clients")
        self.clients = cursor.fetchall()
        client_names = [c[1] for c in self.clients]
        self.client_combo['values'] = client_names
        if client_names:
            self.client_combo.current(0)

    def load_orders(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT o.id, c.name, o.order_details, o.status, o.date
            FROM orders o
            LEFT JOIN clients c ON o.client_id = c.id
            ORDER BY o.date DESC
        """)
        rows = cursor.fetchall()
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def clear_form(self):
        if self.client_combo['values']:
            self.client_combo.current(0)
        self.order_details_text.delete("1.0", tk.END)
        self.status_combo.current(0)
        self.add_btn.config(state=tk.NORMAL)
        self.update_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item['values']
            self.selected_id = values[0]
            client_name = values[1]
            order_details = values[2]
            status = values[3]

            self.client_var.set(client_name)
            self.order_details_text.delete("1.0", tk.END)
            self.order_details_text.insert(tk.END, order_details)
            self.status_var.set(status)

            self.add_btn.config(state=tk.DISABLED)
            self.update_btn.config(state=tk.NORMAL)
            self.delete_btn.config(state=tk.NORMAL)
        else:
            self.clear_form()

    def add_order(self):
        client_name = self.client_var.get()
        order_details = self.order_details_text.get("1.0", tk.END).strip()
        status = self.status_var.get()

        if not client_name or not order_details:
            messagebox.showerror(self.language.get("error", "Error"), self.language.get("error_client_required", "Client and order details are required."))
            return

        client = next((c for c in self.clients if c[1] == client_name), None)
        if not client:
            messagebox.showerror(self.language.get("error", "Error"), self.language.get("error_client_not_found", "Selected client not found."))
            return

        date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO orders (client_id, order_details, status, date)
                VALUES (?, ?, ?, ?)
            """, (client[0], order_details, status, date_str))
            self.conn.commit()
            messagebox.showinfo(self.language.get("success", "Success"), self.language.get("success_order_added", "Order added successfully."))
            self.load_orders()
            self.clear_form()
        except Exception as e:
            messagebox.showerror(self.language.get("error", "Error"), f"{self.language.get('error')}: {e}")

    def update_order(self):
        client_name = self.client_var.get()
        order_details = self.order_details_text.get("1.0", tk.END).strip()
        status = self.status_var.get()

        if not client_name or not order_details:
            messagebox.showerror(self.language.get("error", "Error"), self.language.get("error_client_required", "Client and order details are required."))
            return

        client = next((c for c in self.clients if c[1] == client_name), None)
        if not client:
            messagebox.showerror(self.language.get("error", "Error"), self.language.get("error_client_not_found", "Selected client not found."))
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE orders
                SET client_id = ?, order_details = ?, status = ?
                WHERE id = ?
            """, (client[0], order_details, status, self.selected_id))
            self.conn.commit()
            messagebox.showinfo(self.language.get("success", "Success"), self.language.get("success_order_updated", "Order updated successfully."))
            self.load_orders()
            self.clear_form()
        except Exception as e:
            messagebox.showerror(self.language.get("error", "Error"), f"{self.language.get('error')}: {e}")

    def delete_order(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM orders WHERE id = ?", (self.selected_id,))
            self.conn.commit()
            messagebox.showinfo(self.language.get("success", "Success"), self.language.get("success_order_deleted", "Order deleted successfully."))
            self.load_orders()
            self.clear_form()
        except Exception as e:
            messagebox.showerror(self.language.get("error", "Error"), f"{self.language.get('error')}: {e}")
</create_file>
