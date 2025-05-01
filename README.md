# Tolo Distribution Desktop Application - Development Plan

## 1. Project Overview
Develop a standalone offline desktop application for Tolo Distribution, located in Baco Djicoroni, Mali. The application will manage daily shop operations including product management, sales, clients, stock, suppliers, orders, billing, reporting, and user security.

## 2. Technology Stack
- Language: Python
- UI Framework: Tkinter (or PyQt as alternative)
- Database: SQLite (local file-based)
- PDF/Printing: FPDF, ReportLab, win32print
- Packaging: PyInstaller for Windows executable
- OS Target: Windows 10 (8GB RAM minimum)

## 3. Database Schema (High-level)
- Products: id, category, reference, purchase_price, sale_price, stock_quantity, profit_per_unit
- Sales: id, date, total_amount, payment_method, client_id (nullable), profit
- Clients: id, name, contact_number, purchase_history, credit_balance
- StockEntries: id, product_id, quantity, date, supplier_id
- Suppliers: id, name, contact_info, delivery_history
- Orders: id, client_id, order_details, status, date
- Users: id, username, password_hash, role (Admin, Seller)
- Transactions: id, sale_id, payment_type, amount, date

## 4. UI Design and Main Screens
- Login Screen (with role-based access)
- Dashboard (key metrics: sales, debts, stock levels, profits)
- Product Management (add/edit/delete, categories)
- Sales Management (record sales, print tickets, payment options)
- Client Management (add/edit, credit tracking)
- Stock Management (entries, alerts for low stock)
- Supplier Management (add/edit, delivery tracking)
- Order Management (record orders, delivery status)
- Billing (generate invoices, proforma, quotes, export PDF)
- Reports (daily, weekly, monthly, yearly sales, export PDF/Excel, charts)

## 5. Core Functionalities
- Unique product references and categorization
- Sales recording with multiple payment methods
- Credit sales and client debt tracking
- Stock entry and low stock alerts
- Supplier and order tracking
- Invoice and ticket generation with printing support
- Reporting with export and visualization
- User authentication and role-based permissions
- Local backup and export options

## 6. Security
- Password-protected login
- Role-based access control (Admin and Seller)
- Secure password storage (hashing)

## 7. Packaging and Deployment
- Use PyInstaller to create a Windows executable installer
- Include SQLite database file with initial schema
- Provide backup/export folder for data safety

## 8. Deliverables
- Windows installable executable
- SQLite database file with schema
- Basic user manual (PDF)
- Backup/export folder structure

## 9. Follow-up Steps
- Confirm UI framework choice (Tkinter or PyQt)
- Design database schema in detail
- Develop UI mockups for user approval
- Implement core modules iteratively
- Test on Windows 10 environment
- Prepare packaging and documentation

Please confirm if you approve this plan or if you want to suggest any changes before I start implementation.
