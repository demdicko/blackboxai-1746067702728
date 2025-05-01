import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import database
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

class ReportingManagement(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Reporting and Statistics")
        self.geometry("1000x700")
        self.conn = database.create_connection()
        self.create_widgets()

    def create_widgets(self):
        # Report type selection
        report_frame = tk.Frame(self)
        report_frame.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(report_frame, text="Select Report Type:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.report_type_var = tk.StringVar()
        self.report_type_combo = ttk.Combobox(report_frame, textvariable=self.report_type_var, state="readonly")
        self.report_type_combo['values'] = ("Daily Sales", "Weekly Sales", "Monthly Sales", "Yearly Sales", "Best Sellers")
        self.report_type_combo.grid(row=0, column=1, padx=5, pady=5)
        self.report_type_combo.current(0)

        self.generate_btn = tk.Button(report_frame, text="Generate Report", command=self.generate_report)
        self.generate_btn.grid(row=0, column=2, padx=5, pady=5)

        self.export_btn = tk.Button(report_frame, text="Export to Excel", command=self.export_to_excel)
        self.export_btn.grid(row=0, column=3, padx=5, pady=5)

        # Report display area
        self.report_text = tk.Text(self, height=15)
        self.report_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Chart area
        self.figure = plt.Figure(figsize=(8,4))
        self.ax = self.figure.add_subplot(111)
        self.chart_canvas = FigureCanvasTkAgg(self.figure, self)
        self.chart_canvas.get_tk_widget().pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def generate_report(self):
        report_type = self.report_type_var.get()
        cursor = self.conn.cursor()

        if report_type == "Daily Sales":
            cursor.execute("""
                SELECT date(date) as day, SUM(total_amount) FROM sales
                GROUP BY day ORDER BY day DESC LIMIT 30
            """)
            data = cursor.fetchall()
            self.display_report(data, "Date", "Total Sales")

        elif report_type == "Weekly Sales":
            cursor.execute("""
                SELECT strftime('%Y-%W', date) as week, SUM(total_amount) FROM sales
                GROUP BY week ORDER BY week DESC LIMIT 12
            """)
            data = cursor.fetchall()
            self.display_report(data, "Week", "Total Sales")

        elif report_type == "Monthly Sales":
            cursor.execute("""
                SELECT strftime('%Y-%m', date) as month, SUM(total_amount) FROM sales
                GROUP BY month ORDER BY month DESC LIMIT 12
            """)
            data = cursor.fetchall()
            self.display_report(data, "Month", "Total Sales")

        elif report_type == "Yearly Sales":
            cursor.execute("""
                SELECT strftime('%Y', date) as year, SUM(total_amount) FROM sales
                GROUP BY year ORDER BY year DESC
            """)
            data = cursor.fetchall()
            self.display_report(data, "Year", "Total Sales")

        elif report_type == "Best Sellers":
            cursor.execute("""
                SELECT p.reference, SUM(s.total_amount) as total_sales
                FROM sales s
                JOIN products p ON s.id = p.id
                GROUP BY p.reference
                ORDER BY total_sales DESC LIMIT 10
            """)
            data = cursor.fetchall()
            self.display_report(data, "Product", "Total Sales")

    def display_report(self, data, x_label, y_label):
        self.report_text.delete("1.0", tk.END)
        self.report_text.insert(tk.END, f"{x_label}\t{y_label}\n")
        x_vals = []
        y_vals = []
        for row in data:
            self.report_text.insert(tk.END, f"{row[0]}\t{row[1]:.2f}\n")
            x_vals.append(row[0])
            y_vals.append(row[1])

        self.ax.clear()
        self.ax.bar(x_vals, y_vals)
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        self.ax.set_title(f"{y_label} by {x_label}")
        self.figure.autofmt_xdate()
        self.chart_canvas.draw()

    def export_to_excel(self):
        report_type = self.report_type_var.get()
        cursor = self.conn.cursor()

        if report_type == "Daily Sales":
            cursor.execute("""
                SELECT date(date) as day, SUM(total_amount) FROM sales
                GROUP BY day ORDER BY day DESC LIMIT 30
            """)
        elif report_type == "Weekly Sales":
            cursor.execute("""
                SELECT strftime('%Y-%W', date) as week, SUM(total_amount) FROM sales
                GROUP BY week ORDER BY week DESC LIMIT 12
            """)
        elif report_type == "Monthly Sales":
            cursor.execute("""
                SELECT strftime('%Y-%m', date) as month, SUM(total_amount) FROM sales
                GROUP BY month ORDER BY month DESC LIMIT 12
            """)
        elif report_type == "Yearly Sales":
            cursor.execute("""
                SELECT strftime('%Y', date) as year, SUM(total_amount) FROM sales
                GROUP BY year ORDER BY year DESC
            """)
        elif report_type == "Best Sellers":
            cursor.execute("""
                SELECT p.reference, SUM(s.total_amount) as total_sales
                FROM sales s
                JOIN products p ON s.id = p.id
                GROUP BY p.reference
                ORDER BY total_sales DESC LIMIT 10
            """)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=["Category", "Total Sales"])
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Success", f"Report exported to {file_path}")
