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


