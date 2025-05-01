import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import database
import datetime
from fpdf import FPDF

class BillingManagement(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Billing and Invoicing")
        self.geometry("900x600")
        self.conn = database.create_connection()
        self.create_widgets()
        self.load_sales()

    def create_widgets(self):
        # Invoice list
        self.tree = ttk.Treeview(self, columns=("ID", "Date", "Client", "Total Amount", "Payment Method"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=30)
        self.tree.heading("Date", text="Date")
        self.tree.heading("Client", text="Client")
        self.tree.heading("Total Amount", text="Total Amount")
        self.tree.heading("Payment Method", text="Payment Method")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        self.generate_btn = tk.Button(btn_frame, text="Generate Invoice PDF", command=self.generate_invoice_pdf)
        self.generate_btn.pack(side=tk.LEFT, padx=5)

        self.export_btn = tk.Button(btn_frame, text="Export Invoice as PDF", command=self.export_invoice_pdf)
        self.export_btn.pack(side=tk.LEFT, padx=5)

    def load_sales(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT s.id, s.date, c.name, s.total_amount, s.payment_method
            FROM sales s
            LEFT JOIN clients c ON s.client_id = c.id
            ORDER BY s.date DESC
        """)
        rows = cursor.fetchall()
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def generate_invoice_pdf(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a sale to generate invoice.")
            return
        item = self.tree.item(selected[0])
        sale_id = item['values'][0]

        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT s.id, s.date, c.name, c.contact_number, s.total_amount, s.payment_method
            FROM sales s
            LEFT JOIN clients c ON s.client_id = c.id
            WHERE s.id = ?
        """, (sale_id,))
        sale = cursor.fetchone()
        if not sale:
            messagebox.showerror("Error", "Sale not found.")
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Tolo Distribution - Invoice", ln=True, align='C')
        pdf.ln(10)

        pdf.cell(100, 10, txt=f"Invoice ID: {sale[0]}", ln=True)
        pdf.cell(100, 10, txt=f"Date: {sale[1]}", ln=True)
        pdf.cell(100, 10, txt=f"Client: {sale[2]}", ln=True)
        pdf.cell(100, 10, txt=f"Contact: {sale[3]}", ln=True)
        pdf.cell(100, 10, txt=f"Total Amount: {sale[4]:.2f}", ln=True)
        pdf.cell(100, 10, txt=f"Payment Method: {sale[5]}", ln=True)

        pdf.ln(10)
        pdf.cell(200, 10, txt="Thank you for your business!", ln=True, align='C')

        pdf_file = f"invoice_{sale[0]}.pdf"
        pdf.output(pdf_file)
        messagebox.showinfo("Success", f"Invoice PDF generated: {pdf_file}")

    def export_invoice_pdf(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a sale to export invoice.")
            return
        item = self.tree.item(selected[0])
        sale_id = item['values'][0]

        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT s.id, s.date, c.name, c.contact_number, s.total_amount, s.payment_method
            FROM sales s
            LEFT JOIN clients c ON s.client_id = c.id
            WHERE s.id = ?
        """, (sale_id,))
        sale = cursor.fetchone()
        if not sale:
            messagebox.showerror("Error", "Sale not found.")
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Tolo Distribution - Invoice", ln=True, align='C')
        pdf.ln(10)

        pdf.cell(100, 10, txt=f"Invoice ID: {sale[0]}", ln=True)
        pdf.cell(100, 10, txt=f"Date: {sale[1]}", ln=True)
        pdf.cell(100, 10, txt=f"Client: {sale[2]}", ln=True)
        pdf.cell(100, 10, txt=f"Contact: {sale[3]}", ln=True)
        pdf.cell(100, 10, txt=f"Total Amount: {sale[4]:.2f}", ln=True)
        pdf.cell(100, 10, txt=f"Payment Method: {sale[5]}", ln=True)

        pdf.ln(10)
        pdf.cell(200, 10, txt="Thank you for your business!", ln=True, align='C')

        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            pdf.output(file_path)
            messagebox.showinfo("Success", f"Invoice PDF exported: {file_path}")
