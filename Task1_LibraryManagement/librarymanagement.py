import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# Database connection function
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="shakira",
            database="LibraryManagement"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database connection failed: {err}")
        return None

# Insert a new book
def insert_book():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        title = title_entry.get()
        author = author_entry.get()
        genre = genre_entry.get()
        try:
            cursor.execute("INSERT INTO books (title, author, genre) VALUES (%s, %s, %s)", (title, author, genre))
            conn.commit()
            messagebox.showinfo("Success", "Book added successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to insert book: {err}")
        finally:
            cursor.close()
            conn.close()

# Insert a new member
def insert_member():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        name = member_name_entry.get()
        email = member_email_entry.get()
        phone = member_phone_entry.get()
        cursor.execute("SELECT COUNT(*) FROM Members WHERE email = %s", (email,))
        emailac = cursor.fetchone()[0]
        if emailac > 0:
            messagebox.showerror("Error", "Email ID already exists. Please use a different email.")
        else:
            try:
                cursor.execute("""INSERT INTO Members (name, email, phone) VALUES (%s, %s, %s)""", (name, email, phone))
                conn.commit()
                messagebox.showinfo("Success", "Member added successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to add member: {err}")
            finally:
                cursor.close()
                conn.close()

# Record a transaction
def record_transaction():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        book_id = transaction_book_id_entry.get()
        member_id = transaction_member_id_entry.get()
        try:
            cursor.execute("INSERT INTO transactions (book_id, member_id) VALUES (%s, %s)", (book_id, member_id))
            cursor.execute("UPDATE books SET available = FALSE WHERE book_id = %s", (book_id,))
            conn.commit()
            messagebox.showinfo("Success", "Transaction recorded successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to record transaction: {err}")
        finally:
            cursor.close()
            conn.close()

# Return a book
def return_book():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        transaction_id = transaction_id_entry.get()
        try:
            cursor.execute("UPDATE transactions SET return_date = CURRENT_TIMESTAMP WHERE transaction_id = %s", (transaction_id,))
            cursor.execute("SELECT book_id FROM transactions WHERE transaction_id = %s", (transaction_id,))
            book_id = cursor.fetchone()[0]
            cursor.execute("UPDATE books SET available = TRUE WHERE book_id = %s", (book_id,))
            conn.commit()
            messagebox.showinfo("Success", "Book returned successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to return book: {err}")
        finally:
            cursor.close()
            conn.close()

# Function to view all books
def view_all_books():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM books")
            rows = cursor.fetchall()

            # Create a new window for displaying books
            view_window = tk.Toplevel(root)
            view_window.title("View All Books")

            # Treeview for displaying books
            tree = ttk.Treeview(view_window, columns=("Book ID", "Title", "Author", "Genre", "Available"), show="headings")
            tree.heading("Book ID", text="Book ID")
            tree.heading("Title", text="Title")
            tree.heading("Author", text="Author")
            tree.heading("Genre", text="Genre")
            tree.heading("Available", text="Available")

            tree.column("Book ID", width=100, anchor="center")
            tree.column("Title", width=200)
            tree.column("Author", width=150)
            tree.column("Genre", width=100)
            tree.column("Available", width=100, anchor="center")

            # Insert data into the Treeview
            for row in rows:
                tree.insert("", "end", values=row)

            tree.pack(fill="both", expand=True)

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to fetch books: {err}")
        finally:
            cursor.close()
            conn.close()

# Function to delete a book by ID
def delete_book():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        book_id = book_id_entry.get()

        if book_id.strip() == "":
            messagebox.showerror("Error", "Please enter a Book ID to delete.")
            return

        try:
            # Check if the book is referenced in the transactions table
            cursor.execute("SELECT 1 FROM transactions WHERE book_id = %s", (book_id,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Cannot delete the book. It is referenced in transactions.")
                return

            # Proceed to delete if no references exist
            cursor.execute("DELETE FROM books WHERE book_id = %s", (book_id,))
            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Success", f"Book with ID {book_id} deleted successfully!")
            else:
                messagebox.showerror("Error", f"No book found with ID {book_id}.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to delete book: {err}")
        finally:
            cursor.close()
            conn.close()

# Function to view all members
def view_all_members():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Members")
            rows = cursor.fetchall()

            # Create a new window for displaying members
            view_window = tk.Toplevel(root)
            view_window.title("View All Members")

            # Treeview for displaying members
            tree = ttk.Treeview(view_window, columns=("Member ID", "Name", "Email", "Phone"), show="headings")
            tree.heading("Member ID", text="Member ID")
            tree.heading("Name", text="Name")
            tree.heading("Email", text="Email")
            tree.heading("Phone", text="Phone")

            tree.column("Member ID", width=100, anchor="center")
            tree.column("Name", width=200)
            tree.column("Email", width=200)
            tree.column("Phone", width=150, anchor="center")

            # Insert data into the Treeview
            for row in rows:
                tree.insert("", "end", values=row)

            tree.pack(fill="both", expand=True)

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to fetch members: {err}")
        finally:
            cursor.close()
            conn.close()
# Function to view all transactions
def view_all_transactions():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM transactions")
            rows = cursor.fetchall()

            # Create a new window for displaying transactions
            view_window = tk.Toplevel(root)
            view_window.title("View All Transactions")

            # Treeview for displaying transactions
            tree = ttk.Treeview(view_window, columns=("Transaction ID", "Book ID", "Member ID", "Borrow Date", "Return Date"), show="headings")
            tree.heading("Transaction ID", text="Transaction ID")
            tree.heading("Book ID", text="Book ID")
            tree.heading("Member ID", text="Member ID")
            tree.heading("Borrow Date", text="Borrow Date")
            tree.heading("Return Date", text="Return Date")

            tree.column("Transaction ID", width=100, anchor="center")
            tree.column("Book ID", width=100, anchor="center")
            tree.column("Member ID", width=100, anchor="center")
            tree.column("Borrow Date", width=200)
            tree.column("Return Date", width=200)

            # Insert data into the Treeview
            for row in rows:
                tree.insert("", "end", values=row)

            tree.pack(fill="both", expand=True)

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to fetch transactions: {err}")
        finally:
            cursor.close()
            conn.close()

# GUI setup
root = tk.Tk()
root.title("Library Management System")
root.geometry("1000x700")
root.config(bg="#D2B48C")  # Brown theme background color

# Title Label
title_label = tk.Label(root, text="Library Management System", font=("Arial", 24, "bold"), bg="#D2B48C", fg="#8B4513")
title_label.pack(pady=20)

# Create a frame for the main layout
main_frame = tk.Frame(root, bg="#D2B48C", bd=5, relief="solid")
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

# Configure columns and rows for the responsive layout
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_columnconfigure(2, weight=1)
main_frame.grid_columnconfigure(3, weight=1)
main_frame.grid_rowconfigure(0, weight=1)

# Left Frame (Add Books)
left_frame = tk.Frame(main_frame, bg="#D2B48C", bd=2, relief="solid")
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Second Frame (Add Members)
second_frame = tk.Frame(main_frame, bg="#D2B48C", bd=2, relief="solid")
second_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Center Frame (Transactions)
center_frame = tk.Frame(main_frame, bg="#D2B48C", bd=2, relief="solid")
center_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

# Right Frame (View/Delete Books)
right_frame = tk.Frame(main_frame, bg="#D2B48C", bd=2, relief="solid")
right_frame.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

# Book Management Section (Left Frame)
tk.Label(left_frame, text="Add Books", font=("Arial", 14, "bold"), bg="#D2B48C", fg="#8B4513").grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(left_frame, text="Title:", font=("Arial", 12, "bold"), bg="#D2B48C").grid(row=1, column=0, padx=10, pady=5)
title_entry = tk.Entry(left_frame)
title_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(left_frame, text="Author:", font=("Arial", 12, "bold"), bg="#D2B48C").grid(row=2, column=0, padx=10, pady=5)
author_entry = tk.Entry(left_frame)
author_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(left_frame, text="Genre:", font=("Arial", 12, "bold"), bg="#D2B48C").grid(row=3, column=0, padx=10, pady=5)
genre_entry = tk.Entry(left_frame)
genre_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Button(left_frame, text="Add Book", command=insert_book, bg="#8B4513", fg="white", font=("Arial", 12, "bold")).grid(row=4, column=0, columnspan=2, pady=5)

# Member Management Section (Second Frame)
tk.Label(second_frame, text="Add Members", font=("Arial", 14, "bold"), bg="#D2B48C", fg="#8B4513").grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(second_frame, text="Name:", font=("Arial", 12, "bold"), bg="#D2B48C").grid(row=1, column=0, padx=10, pady=5)
member_name_entry = tk.Entry(second_frame)
member_name_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(second_frame, text="Email:", font=("Arial", 12, "bold"), bg="#D2B48C").grid(row=2, column=0, padx=10, pady=5)
member_email_entry = tk.Entry(second_frame)
member_email_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(second_frame, text="Phone:", font=("Arial", 12, "bold"), bg="#D2B48C").grid(row=3, column=0, padx=10, pady=5)
member_phone_entry = tk.Entry(second_frame)
member_phone_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Button(second_frame, text="Add Member", command=insert_member, bg="#8B4513", fg="white", font=("Arial", 12, "bold")).grid(row=4, column=0, columnspan=2, pady=5)

# Transaction Management Section (Center Frame)
tk.Label(center_frame, text="Transactions", font=("Arial", 14, "bold"), bg="#D2B48C", fg="#8B4513").grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(center_frame, text="Book ID:", font=("Arial", 12, "bold"), bg="#D2B48C").grid(row=1, column=0, padx=10, pady=5)
transaction_book_id_entry = tk.Entry(center_frame)
transaction_book_id_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(center_frame, text="Member ID:", font=("Arial", 12, "bold"), bg="#D2B48C").grid(row=2, column=0, padx=10, pady=5)
transaction_member_id_entry = tk.Entry(center_frame)
transaction_member_id_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Button(center_frame, text="Borrow Book", command=record_transaction, bg="#8B4513", fg="white", font=("Arial", 12, "bold")).grid(row=3, column=0, columnspan=2, pady=5)

tk.Label(center_frame, text="Transaction ID:", font=("Arial", 12, "bold"), bg="#D2B48C").grid(row=4, column=0, padx=10, pady=5)
transaction_id_entry = tk.Entry(center_frame)
transaction_id_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Button(center_frame, text="Return Book", command=return_book, bg="#8B4513", fg="white", font=("Arial", 12, "bold")).grid(row=5, column=0, columnspan=2, pady=5)

# View/Delete Books Section (Right Frame)
tk.Label(right_frame, text="View/Delete Books", font=("Arial", 14, "bold"), bg="#D2B48C", fg="#8B4513").grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(right_frame, text="Book ID:", font=("Arial", 12, "bold"), bg="#D2B48C").grid(row=1, column=0, padx=10, pady=5)
book_id_entry = tk.Entry(right_frame)
book_id_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Button(right_frame, text="View All Books", command=view_all_books, bg="#8B4513", fg="white", font=("Arial", 12, "bold")).grid(row=3, column=0, padx=10, pady=5)
tk.Button(right_frame, text="Delete Book", command=delete_book, bg="#8B4513", fg="white", font=("Arial", 12, "bold")).grid(row=2, column=1, padx=10, pady=5)
tk.Button(right_frame, text="View All Members", command=view_all_members, bg="#8B4513", fg="white", font=("Arial", 12, "bold")).grid(row=4, column=0, padx=10, pady=5)
tk.Button(right_frame, text="View All Transactions", command=view_all_transactions, bg="#8B4513", fg="white", font=("Arial", 12, "bold")).grid(row=5, column=0, padx=10, pady=5)

# Start the application
root.mainloop()
