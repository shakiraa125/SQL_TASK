USE LibraryManagement;
-- Books Table
CREATE TABLE Books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    genre VARCHAR(100),
    availability VARCHAR(10) DEFAULT 'yes'
);
-- Members Table
CREATE TABLE Members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);
-- Transactions Table
CREATE TABLE Transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    member_id INT NOT NULL,
    borrow_date DATE ,
    return_date DATE,
    FOREIGN KEY (book_id) REFERENCES Books(book_id),
    FOREIGN KEY (member_id) REFERENCES Members(member_id)
);

ALTER TABLE Members
ADD phone VARCHAR(15);



select * from transactions;
ALTER TABLE books
RENAME COLUMN Availability TO available;

ALTER TABLE transactions
ADD COLUMN borroww_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
alter table transactions drop column borrow_date;
select * from transactions;
ALTER TABLE transactions
ADD COLUMN returnn_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
select * from books;
ALTER TABLE transactions
DROP FOREIGN KEY transactions_ibfk_1;

ALTER TABLE transactions
ADD CONSTRAINT transactions_ibfk_1
FOREIGN KEY (book_id) REFERENCES books(book_id)
ON DELETE CASCADE;
select * from members;
delete from members where member_id=7;
select * from books
;
ALTER TABLE members
ADD COLUMN memberships_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
alter table members drop column membership_date;




