**Library Management System Project Report**

---
**TASK:**
Create a database for managing a library's book inventory, members, and
borrow/return transactions. This project helps you learn basic SQL commands
and database design. Design tables for books, members, and transactions.
Write SQL queries to insert, update, delete, and retrieve data.
**Language Used:**
- SQL
- Python

**Tools Utilized:**
- MySQL
- Visual Studio Code

---

### **Project Overview:**
The Library Management System is designed to streamline and organize library operations. This system enables administrators to efficiently manage book inventory, member details, and borrow/return transactions through a user-friendly graphical interface developed using Python’s Tkinter module. It ensures seamless record-keeping and enhances operational efficiency.

---

### **Database Design:**
The database consists of three primary tables:

1. **Books Table:**
   - **Fields:**
     - `book_id` (Primary Key): Unique identifier for each book.
     - `book_name`: Title of the book.
     - `author`: Author of the book.
     - `genre`: Category or genre of the book (e.g., Fiction, Science).
   
2. **Members Table:**
   - **Fields:**
     - `member_id` (Primary Key): Unique identifier for each member.
     - `name`: Name of the member.
     - `email`: Email ID of the member.
     - `phone`: Contact number of the member.
     - `membership_date`: The date when the member registered.

3. **Transactions Table:**
   - **Fields:**
     - `transaction_id` (Primary Key): Unique identifier for each transaction.
     - `member_id` (Foreign Key): ID of the member borrowing or returning the book.
     - `book_id` (Foreign Key): ID of the borrowed book.
     - `borrow_date`: Date when the book was borrowed.
     - `return_date`: Date when the book was returned.

---

### **Graphical User Interface (GUI):**
The GUI for the Library Management System was built using the Tkinter module in Python. It features several buttons that allow the administrator to perform key operations effortlessly. Below is the list of functionalities provided through the GUI:

1. **Add Book:**
   - Allows the admin to add a new book to the inventory by providing book details such as name, author, and genre.

2. **Add Member:**
   - Enables the admin to register a new library member by entering their name, email, phone number, and membership date.

3. **Borrow Book:**
   - Records the borrowing transaction by linking a book to a member along with the borrow date.

4. **Return Book:**
   - Updates the transactions table with the return date of a borrowed book.

5. **View Books:**
   - Displays all books in the library in a well-formatted table view.

6. **Delete Book:**
   - Removes a book from the inventory after ensuring it is not currently involved in any active transaction.

7. **View Members:**
   - Shows a list of all registered members along with their details.

8. **View Transactions:**
   - Displays a comprehensive list of all borrowing and return transactions for better tracking.

---

### **Admin Functionalities:**
The system provides the administrator with complete control over library management. The admin can:

- Add and manage book records.
- Add and manage member records.
- View all books, members, and transactions.
- Record borrowing and returning of books.
- Delete books (with constraints to avoid breaking dependencies).
- Monitor transaction history for better accountability.

---

### **Conclusion:**
The Library Management System effectively automates and simplifies routine library tasks. The use of SQL ensures robust database management, while Python with Tkinter provides an intuitive GUI for interaction. This project demonstrates the integration of front-end and back-end systems to deliver a cohesive and functional application. It is scalable and can be further enhanced with additional features like reporting, email notifications, or integration with an online portal for members.

---

