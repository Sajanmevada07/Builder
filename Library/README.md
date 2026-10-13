# 📚 Object-Oriented Library Management System

A standalone, production-ready Python script demonstrating core **Object-Oriented Programming (OOP)** design principles. The system models a library ecosystem with catalog tracking, member loan limits, search capabilities, and time-stamped transaction logs.

---

## 🏗️ Architecture & Class Structure

The application is structured into four primary classes, each adhering to the **Single Responsibility Principle**:

1. **`Book`**: Encapsulates book state (ISBN, title, author, availability).
2. **`Member`**: Manages patron details, active loans, and borrowing limit enforcement.
3. **`Transaction`**: Records time-stamped audit logs for checkouts and returns.
4. **`Library`**: System coordinator managing search indices, member registries, and transaction workflows.

---

## 💡 Key OOP Concepts Demonstrated

* **Encapsulation:** Protected state variables (e.g., `_is_borrowed`, `_borrowed_books`) prevent unauthorized direct modification from outside class boundaries.
* **Property Decorators (`@property`):** Exposes controlled, read-only interface views for class attributes.
* **Dunder/Magic Methods:** Custom `__str__` and `__repr__` implementations for human-readable console representation.
* **Composition:** The `Library` class coordinates and contains instances of `Book`, `Member`, and `Transaction`.

---

## 🚀 How to Run

### Prerequisites
* Python 3.9 or higher.

### Execution

1. Copy the code snippet into a file named `library.py`.
2. Run the script directly using Python:

```bash
python library.py


Expected Output 

==================================================
  LIBRARY MANAGEMENT SYSTEM - OOP DEMONSTRATION   
==================================================

--- Registering Catalog & Members ---
Added to library: 'Clean Code'
Added to library: 'The Pragmatic Programmer'
Added to library: 'Head First Design Patterns'
Registered member: Alice Vance

--- Catalog Search ---
Search Result: [978-0201616224] 'The Pragmatic Programmer' by Andrew Hunt (Available)

--- Borrowing Workflows & Limit Checks ---
Success: 'Clean Code' checked out to Alice Vance.
Success: 'The Pragmatic Programmer' checked out to Alice Vance.
Error: Alice Vance reached borrowing limit (2 max).

--- Patron State Check ---
Member: Alice Vance (ID: M001) - Borrowed: 2/2

--- Return Workflow ---
Success: 'Clean Code' returned by Alice Vance.
Success: 'Head First Design Patterns' checked out to Alice Vance.

--- Audit Log output ---

--- City Central Library Transaction Log ---
[2026-10-13 11:14:00] Member M001 -> BORROW -> Book 978-0135404676
[2026-10-13 11:14:00] Member M001 -> BORROW -> Book 978-0201616224
[2026-10-13 11:14:00] Member M001 -> RETURN -> Book 978-0135404676
[2026-10-13 11:14:00] Member M001 -> BORROW -> Book 978-0596009205