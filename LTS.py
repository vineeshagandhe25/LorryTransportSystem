import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

# Database connection function
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="empdb"
        )
        return connection
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error connecting to MySQL: {e}")
        return None

# Function to insert data into the database
def insert_data(date, lorry_number, amount):
    try:
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            query = "INSERT INTO lorry_transport (date, lorry_number, amount_collected) VALUES (%s, %s, %s)"
            cursor.execute(query, (date, lorry_number, amount))
            connection.commit()
            messagebox.showinfo("Success", "Data inserted successfully!")
    except Error as e:
        messagebox.showerror("Error", f"Error while inserting data: {e}")
    finally:
        if connection:
            connection.close()

# Submit button functionality
def submit_entry():
    date = date_entry.get()
    lorry_number = lorry_number_entry.get()
    amount = amount_entry.get()

    if date and lorry_number and amount:
        try:
            amount = float(amount)
            insert_data(date, lorry_number, amount)
            date_entry.delete(0, tk.END)
            lorry_number_entry.delete(0, tk.END)
            amount_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a valid number!")
    else:
        messagebox.showerror("Error", "All fields are required!")

# Open "More Options" Page
def open_more_options_page():
    options_window = tk.Toplevel(root)
    options_window.title("More Options")
    options_window.geometry("600x400")

    def query_data(query, params=()):
        try:
            connection = connect_to_db()
            if connection:
                cursor = connection.cursor()
                cursor.execute(query, params)
                result = cursor.fetchall()
                return result
        except Error as e:
            messagebox.showerror("Error", f"Error fetching data: {e}")
            return []
        finally:
            if connection:
                connection.close()

    # Display results in Treeview
    def display_results(results):
        tree.delete(*tree.get_children())
        for record in results:
            tree.insert("", "end", values=record)

    # Fetch all data
    def fetch_all():
        query = "SELECT * FROM lorry_transport"
        results = query_data(query)
        display_results(results)

    # Fetch data by date
    def fetch_by_date():
        date = date_entry_option.get()
        if date:
            query = "SELECT * FROM lorry_transport WHERE date = %s"
            results = query_data(query, (date,))
            display_results(results)
        else:
            messagebox.showerror("Error", "Please enter a date!")

    # Fetch data by lorry number
    def fetch_by_lorry():
        lorry_number = lorry_number_entry_option.get()
        if lorry_number:
            query = "SELECT * FROM lorry_transport WHERE lorry_number = %s"
            results = query_data(query, (lorry_number,))
            display_results(results)
        else:
            messagebox.showerror("Error", "Please enter a lorry number!")

    # Calculate total amount by date
    def calculate_total_by_date():
        date = date_entry_option.get()
        if date:
            query = "SELECT SUM(amount_collected) FROM lorry_transport WHERE date = %s"
            results = query_data(query, (date,))
            total = results[0][0] if results[0][0] else 0
            messagebox.showinfo("Total Amount", f"Total amount collected on {date}: {total}")
        else:
            messagebox.showerror("Error", "Please enter a date!")

    # Calculate total amount by lorry
    def calculate_total_by_lorry():
        lorry_number = lorry_number_entry_option.get()
        if lorry_number:
            query = "SELECT SUM(amount_collected) FROM lorry_transport WHERE lorry_number = %s"
            results = query_data(query, (lorry_number,))
            total = results[0][0] if results[0][0] else 0
            messagebox.showinfo("Total Amount", f"Total amount collected for lorry {lorry_number}: {total}")
        else:
            messagebox.showerror("Error", "Please enter a lorry number!")

    # Input fields 
    tk.Label(options_window, text="Enter Date (YYYY-MM-DD):").pack(pady=5)
    date_entry_option = tk.Entry(options_window)
    date_entry_option.pack(pady=5)

    tk.Label(options_window, text="Enter Lorry Number:").pack(pady=5)
    lorry_number_entry_option = tk.Entry(options_window)
    lorry_number_entry_option.pack(pady=5)

    # Buttons 
    tk.Button(options_window, text="View All Data", command=fetch_all).pack(pady=5)
    tk.Button(options_window, text="View Data by Date", command=fetch_by_date).pack(pady=5)
    tk.Button(options_window, text="View Data by Lorry Number", command=fetch_by_lorry).pack(pady=5)
    tk.Button(options_window, text="Calculate Total Amount by Date", command=calculate_total_by_date).pack(pady=5)
    tk.Button(options_window, text="Calculate Total Amount by Lorry", command=calculate_total_by_lorry).pack(pady=5)

    # Treeview for displaying results
    tree = ttk.Treeview(options_window, columns=("ID", "Date", "Lorry Number", "Amount Collected"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Date", text="Date")
    tree.heading("Lorry Number", text="Lorry Number")
    tree.heading("Amount Collected", text="Amount Collected")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

# Tkinter GUI for Input Page
root = tk.Tk()
root.title("Lorry Transport Management")
root.geometry("400x300")

# Input fields
tk.Label(root, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=10, sticky="w")
date_entry = tk.Entry(root)
date_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Lorry Number:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
lorry_number_entry = tk.Entry(root)
lorry_number_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Amount Collected:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
amount_entry = tk.Entry(root)
amount_entry.grid(row=2, column=1, padx=10, pady=10)

# Buttons
submit_button = tk.Button(root, text="Submit", command=submit_entry)
submit_button.grid(row=3, column=0, padx=10, pady=20)

more_options_button = tk.Button(root, text="More Options", command=open_more_options_page)
more_options_button.grid(row=3, column=1, padx=10, pady=20)

root.mainloop()
