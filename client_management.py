import tkinter as tk
from tkinter import ttk, messagebox
import database

class ClientManagement(tk.Toplevel):
    def __init__(self, master=None, language=None):
        super().__init__(master)
        self.language = language or {}
        self.title(self.language.get("client_management_title", "Client Management"))
        self.geometry("800x500")
        self.conn = database.create_connection()
        self.create_widgets()
        self.load_clients()

    def create_widgets(self):
        # Client form
        form_frame = tk.Frame(self)
        form_frame.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(form_frame, text=self.language.get("name_label", "Name:")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(form_frame, textvariable=self.name_var)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text=self.language.get("contact_number_label", "Contact Number:")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.contact_var = tk.StringVar()
        self.contact_entry = tk.Entry(form_frame, textvariable=self.contact_var)
        self.contact_entry.grid(row=1, column=1, padx=5, pady=5)

        # Buttons
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

        self.add_btn = tk.Button(btn_frame, text=self.language.get("add_client_btn", "Add Client"), command=self.add_client)
        self.add_btn.pack(side=tk.LEFT, padx=5)

        self.update_btn = tk.Button(btn_frame, text=self.language.get("update_client_btn", "Update Client"), command=self.update_client, state=tk.DISABLED)
        self.update_btn.pack(side=tk.LEFT, padx=5)

        self.delete_btn = tk.Button(btn_frame, text=self.language.get("delete_client_btn", "Delete Client"), command=self.delete_client, state=tk.DISABLED)
        self.delete_btn.pack(side=tk.LEFT, padx=5)

        # Client list
        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Contact Number", "Credit Balance"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=30)
        self.tree.heading("Name", text=self.language.get("name_label", "Name"))
        self.tree.heading("Contact Number", text=self.language.get("contact_number_label", "Contact Number"))
        self.tree.heading("Credit Balance", text=self.language.get("credit_balance_label", "Credit Balance"))
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def load_clients(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, contact_number, credit_balance FROM clients")
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

    def add_client(self):
        name = self.name_var.get()
        contact = self.contact_var.get()

        if not name:
            messagebox.showerror(self.language.get("error", "Error"), self.language.get("error_name_required", "Name is required."))
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO clients (name, contact_number)
                VALUES (?, ?)
            """, (name, contact))
            self.conn.commit()
            messagebox.showinfo(self.language.get("success", "Success"), self.language.get("success_client_added", "Client added successfully."))
            self.load_clients()
            self.clear_form()
        except Exception as e:
            messagebox.showerror(self.language.get("error", "Error"), self.language.get("error_failed_add_client", f"Failed to add client: {e}"))

    def update_client(self):
        name = self.name_var.get()
        contact = self.contact_var.get()

        if not name:
            messagebox.showerror(self.language.get("error", "Error"), self.language.get("error_name_required", "Name is required."))
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE clients
                SET name = ?, contact_number = ?
                WHERE id = ?
            """, (name, contact, self.selected_id))
            self.conn.commit()
            messagebox.showinfo(self.language.get("success", "Success"), self.language.get("success_client_updated", "Client updated successfully."))
            self.load_clients()
            self.clear_form()
        except Exception as e:
            messagebox.showerror(self.language.get("error", "Error"), self.language.get("error_failed_update_client", f"Failed to update client: {e}"))

    def delete_client(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM clients WHERE id = ?", (self.selected_id,))
            self.conn.commit()
            messagebox.showinfo(self.language.get("success", "Success"), self.language.get("success_client_deleted", "Client deleted successfully."))
            self.load_clients()
            self.clear_form()
        except Exception as e:
            messagebox.showerror(self.language.get("error", "Error"), self.language.get("error_failed_delete_client", f"Failed to delete client: {e}"))
</create_file>
