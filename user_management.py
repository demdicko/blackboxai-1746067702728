import tkinter as tk
from tkinter import messagebox
import database
import hashlib

class LoginWindow(tk.Toplevel):
    def __init__(self, master=None, on_login_success=None, language=None):
        super().__init__(master)
        self.language = language or {}
        self.title(self.language.get("login_title", "Login - Tolo Distribution"))
        self.geometry("300x180")
        self.on_login_success = on_login_success
        self.conn = database.create_connection()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text=self.language.get("username_label", "Username:")).pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        tk.Label(self, text=self.language.get("password_label", "Password:")).pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        self.login_btn = tk.Button(self, text=self.language.get("login_btn", "Login"), command=self.login)
        self.login_btn.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror(self.language.get("error", "Error"), self.language.get("error_enter_credentials", "Please enter username and password."))
            return

        password_hash = hashlib.sha256(password.encode()).hexdigest()

        cursor = self.conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username = ? AND password_hash = ?", (username, password_hash))
        result = cursor.fetchone()

        if result:
            role = result[0]
            messagebox.showinfo(self.language.get("success", "Success"), self.language.get("welcome_message", "Login successful. Role: {role}").format(role=role))
            self.destroy()
            if self.on_login_success:
                self.on_login_success(role)
        else:
            messagebox.showerror(self.language.get("error", "Error"), self.language.get("error_invalid_credentials", "Invalid username or password."))

class UserManagement:
    def __init__(self, master=None):
        self.master = master
        self.conn = database.create_connection()

    def add_user(self, username, password, role):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", (username, password_hash, role))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Failed to add user: {e}")
            return False
