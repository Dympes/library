import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB_NAME = "library.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        year INTEGER,
        publisher TEXT,
        isbn TEXT,
        quantity INTEGER DEFAULT 1,
        location TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        grade TEXT,
        phone TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS issued_books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER,
        student_id INTEGER,
        issue_date TEXT,
        return_date TEXT,
        returned INTEGER DEFAULT 0,
        FOREIGN KEY (book_id) REFERENCES books(id),
        FOREIGN KEY (student_id) REFERENCES students(id)
    )''')
    
    conn.commit()
    conn.close()

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Библиотека")
        self.root.geometry("900x600")
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.tab_books = ttk.Frame(self.notebook)
        self.tab_students = ttk.Frame(self.notebook)
        self.tab_issued = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_books, text="Книги")
        self.notebook.add(self.tab_students, text="Ученики")
        self.notebook.add(self.tab_issued, text="Выдача")
        
        self.setup_books_tab()
        self.setup_students_tab()
        self.setup_issued_tab()
        
        self.refresh_all()

    def setup_books_tab(self):
        frame = ttk.LabelFrame(self.tab_books, text="Добавить книгу")
        frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frame, text="Название:").grid(row=0, column=0, padx=5, pady=5)
        self.book_title = ttk.Entry(frame, width=25)
        self.book_title.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="Автор:").grid(row=0, column=2, padx=5, pady=5)
        self.book_author = ttk.Entry(frame, width=20)
        self.book_author.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(frame, text="Год:").grid(row=0, column=4, padx=5, pady=5)
        self.book_year = ttk.Entry(frame, width=8)
        self.book_year.grid(row=0, column=5, padx=5, pady=5)
        
        ttk.Label(frame, text="Издательство:").grid(row=1, column=0, padx=5, pady=5)
        self.book_publisher = ttk.Entry(frame, width=20)
        self.book_publisher.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="ISBN:").grid(row=1, column=2, padx=5, pady=5)
        self.book_isbn = ttk.Entry(frame, width=15)
        self.book_isbn.grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Label(frame, text="Кол-во:").grid(row=1, column=4, padx=5, pady=5)
        self.book_quantity = ttk.Entry(frame, width=8)
        self.book_quantity.grid(row=1, column=5, padx=5, pady=5)
        self.book_quantity.insert(0, "1")
        
        ttk.Label(frame, text="Место:").grid(row=2, column=0, padx=5, pady=5)
        self.book_location = ttk.Entry(frame, width=10)
        self.book_location.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(frame, text="Добавить", command=self.add_book).grid(row=2, column=2, padx=5)
        ttk.Button(frame, text="Редакт.", command=self.edit_book).grid(row=2, column=3, padx=5)
        ttk.Button(frame, text="Удалить", command=self.delete_book).grid(row=2, column=4, padx=5)
        
        columns = ("id", "title", "author", "year", "publisher", "isbn", "qty", "location")
        self.books_tree = ttk.Treeview(self.tab_books, columns=columns, show='headings', height=15)
        self.books_tree.heading("id", text="ID")
        self.books_tree.heading("title", text="Название")
        self.books_tree.heading("author", text="Автор")
        self.books_tree.heading("year", text="Год")
        self.books_tree.heading("publisher", text="Издательство")
        self.books_tree.heading("isbn", text="ISBN")
        self.books_tree.heading("qty", text="Кол-во")
        self.books_tree.heading("location", text="Место")
        self.books_tree.column("id", width=30)
        self.books_tree.column("title", width=150)
        self.books_tree.column("author", width=120)
        self.books_tree.column("year", width=50)
        self.books_tree.column("publisher", width=80)
        self.books_tree.column("isbn", width=80)
        self.books_tree.column("qty", width=50)
        self.books_tree.pack(fill='both', expand=True, padx=10, pady=10)

    def setup_students_tab(self):
        frame = ttk.LabelFrame(self.tab_students, text="Добавить ученика")
        frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frame, text="ФИО:").grid(row=0, column=0, padx=5, pady=5)
        self.student_name = ttk.Entry(frame, width=25)
        self.student_name.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="Класс:").grid(row=0, column=2, padx=5, pady=5)
        self.student_grade = ttk.Entry(frame, width=10)
        self.student_grade.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(frame, text="Телефон:").grid(row=0, column=4, padx=5, pady=5)
        self.student_phone = ttk.Entry(frame, width=15)
        self.student_phone.grid(row=0, column=5, padx=5, pady=5)
        
        ttk.Button(frame, text="Добавить", command=self.add_student).grid(row=0, column=6, padx=5)
        ttk.Button(frame, text="Редакт.", command=self.edit_student).grid(row=0, column=7, padx=5)
        ttk.Button(frame, text="Удалить", command=self.delete_student).grid(row=0, column=8, padx=5)
        
        columns = ("id", "name", "grade", "phone")
        self.students_tree = ttk.Treeview(self.tab_students, columns=columns, show='headings', height=15)
        self.students_tree.heading("id", text="ID")
        self.students_tree.heading("name", text="ФИО")
        self.students_tree.heading("grade", text="Класс")
        self.students_tree.heading("phone", text="Телефон")
        self.students_tree.column("id", width=30)
        self.students_tree.pack(fill='both', expand=True, padx=10, pady=10)

    def setup_issued_tab(self):
        frame = ttk.LabelFrame(self.tab_issued, text="Выдать книгу")
        frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frame, text="Книга:").grid(row=0, column=0, padx=5, pady=5)
        self.issued_book = ttk.Combobox(frame, width=25)
        self.issued_book.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="Ученик:").grid(row=0, column=2, padx=5, pady=5)
        self.issued_student = ttk.Combobox(frame, width=25)
        self.issued_student.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(frame, text="Вернуть через (дней):").grid(row=0, column=4, padx=5, pady=5)
        self.issued_days = ttk.Entry(frame, width=8)
        self.issued_days.grid(row=0, column=5, padx=5, pady=5)
        self.issued_days.insert(0, "14")
        
        ttk.Button(frame, text="Выдать", command=self.issue_book).grid(row=0, column=6, padx=5)
        ttk.Button(frame, text="Вернуть", command=self.return_book).grid(row=0, column=7, padx=5)
        
        columns = ("id", "book", "student", "issue_date", "return_date", "status")
        self.issued_tree = ttk.Treeview(self.tab_issued, columns=columns, show='headings', height=15)
        self.issued_tree.heading("id", text="ID")
        self.issued_tree.heading("book", text="Книга")
        self.issued_tree.heading("student", text="Ученик")
        self.issued_tree.heading("issue_date", text="Выдана")
        self.issued_tree.heading("return_date", text="Вернуть")
        self.issued_tree.heading("status", text="Статус")
        self.issued_tree.column("id", width=30)
        self.issued_tree.column("book", width=150)
        self.issued_tree.column("student", width=120)
        self.issued_tree.column("issue_date", width=80)
        self.issued_tree.column("return_date", width=80)
        self.issued_tree.column("status", width=70)
        self.issued_tree.pack(fill='both', expand=True, padx=10, pady=10)

    def add_book(self):
        title = self.book_title.get()
        author = self.book_author.get()
        
        if not title:
            messagebox.showerror("Ошибка", "Введите название книги")
            return
        
        year = self.book_year.get()
        publisher = self.book_publisher.get()
        isbn = self.book_isbn.get()
        quantity = self.book_quantity.get() or 1
        location = self.book_location.get()
        
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO books (title, author, year, publisher, isbn, quantity, location) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (title, author, year, publisher, isbn, quantity, location))
        conn.commit()
        conn.close()
        
        self.clear_book_fields()
        self.refresh_books()

    def edit_book(self):
        selected = self.books_tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите книгу")
            return
        
        item = self.books_tree.item(selected)
        book_id = item['values'][0]
        
        win = tk.Toplevel(self.root)
        win.title("Редактировать книгу")
        win.geometry("400x280")
        
        ttk.Label(win, text="Название:").grid(row=0, column=0, padx=5, pady=5)
        entry_title = ttk.Entry(win, width=30)
        entry_title.grid(row=0, column=1, padx=5, pady=5)
        entry_title.insert(0, item['values'][1])
        
        ttk.Label(win, text="Автор:").grid(row=1, column=0, padx=5, pady=5)
        entry_author = ttk.Entry(win, width=30)
        entry_author.grid(row=1, column=1, padx=5, pady=5)
        entry_author.insert(0, item['values'][2])
        
        ttk.Label(win, text="Год:").grid(row=2, column=0, padx=5, pady=5)
        entry_year = ttk.Entry(win, width=10)
        entry_year.grid(row=2, column=1, padx=5, pady=5)
        entry_year.insert(0, item['values'][3] or "")
        
        ttk.Label(win, text="Издательство:").grid(row=3, column=0, padx=5, pady=5)
        entry_publisher = ttk.Entry(win, width=30)
        entry_publisher.grid(row=3, column=1, padx=5, pady=5)
        entry_publisher.insert(0, item['values'][4] or "")
        
        ttk.Label(win, text="ISBN:").grid(row=4, column=0, padx=5, pady=5)
        entry_isbn = ttk.Entry(win, width=30)
        entry_isbn.grid(row=4, column=1, padx=5, pady=5)
        entry_isbn.insert(0, item['values'][5] or "")
        
        ttk.Label(win, text="Кол-во:").grid(row=5, column=0, padx=5, pady=5)
        entry_quantity = ttk.Entry(win, width=10)
        entry_quantity.grid(row=5, column=1, padx=5, pady=5)
        entry_quantity.insert(0, item['values'][6] or 1)
        
        ttk.Label(win, text="Место:").grid(row=6, column=0, padx=5, pady=5)
        entry_location = ttk.Entry(win, width=10)
        entry_location.grid(row=6, column=1, padx=5, pady=5)
        entry_location.insert(0, item['values'][7] or "")
        
        def save():
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("""UPDATE books SET title=?, author=?, year=?, publisher=?, isbn=?, quantity=?, location=? WHERE id=?""",
                      (entry_title.get(), entry_author.get(), entry_year.get(), entry_publisher.get(),
                       entry_isbn.get(), entry_quantity.get(), entry_location.get(), book_id))
            conn.commit()
            conn.close()
            win.destroy()
            self.refresh_books()
        
        ttk.Button(win, text="Сохранить", command=save).grid(row=7, column=0, columnspan=2, pady=20)

    def delete_book(self):
        selected = self.books_tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите книгу")
            return
        
        item = self.books_tree.item(selected)
        book_id = item['values'][0]
        
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("DELETE FROM issued_books WHERE book_id=? AND returned=0", (book_id,))
        c.execute("DELETE FROM books WHERE id=?", (book_id,))
        conn.commit()
        conn.close()
        
        self.refresh_books()

    def add_student(self):
        name = self.student_name.get()
        
        if not name:
            messagebox.showerror("Ошибка", "Введите ФИО ученика")
            return
        
        grade = self.student_grade.get()
        phone = self.student_phone.get()
        
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO students (name, grade, phone) VALUES (?, ?, ?)", (name, grade, phone))
        conn.commit()
        conn.close()
        
        self.student_name.delete(0, tk.END)
        self.student_grade.delete(0, tk.END)
        self.student_phone.delete(0, tk.END)
        self.refresh_students()

    def edit_student(self):
        selected = self.students_tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите ученика")
            return
        
        item = self.students_tree.item(selected)
        student_id = item['values'][0]
        
        win = tk.Toplevel(self.root)
        win.title("Редактировать ученика")
        win.geometry("300x150")
        
        ttk.Label(win, text="ФИО:").grid(row=0, column=0, padx=5, pady=5)
        entry_name = ttk.Entry(win, width=25)
        entry_name.grid(row=0, column=1, padx=5, pady=5)
        entry_name.insert(0, item['values'][1])
        
        ttk.Label(win, text="Класс:").grid(row=1, column=0, padx=5, pady=5)
        entry_grade = ttk.Entry(win, width=10)
        entry_grade.grid(row=1, column=1, padx=5, pady=5)
        entry_grade.insert(0, item['values'][2] or "")
        
        ttk.Label(win, text="Телефон:").grid(row=2, column=0, padx=5, pady=5)
        entry_phone = ttk.Entry(win, width=15)
        entry_phone.grid(row=2, column=1, padx=5, pady=5)
        entry_phone.insert(0, item['values'][3] or "")
        
        def save():
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("UPDATE students SET name=?, grade=?, phone=? WHERE id=?",
                      (entry_name.get(), entry_grade.get(), entry_phone.get(), student_id))
            conn.commit()
            conn.close()
            win.destroy()
            self.refresh_students()
        
        ttk.Button(win, text="Сохранить", command=save).grid(row=3, column=0, columnspan=2, pady=20)

    def delete_student(self):
        selected = self.students_tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите ученика")
            return
        
        item = self.students_tree.item(selected)
        student_id = item['values'][0]
        
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("UPDATE issued_books SET returned=1 WHERE student_id=? AND returned=0", (student_id,))
        c.execute("DELETE FROM students WHERE id=?", (student_id,))
        conn.commit()
        conn.close()
        
        self.refresh_students()

    def issue_book(self):
        book = self.issued_book.get()
        student = self.issued_student.get()
        days = self.issued_days.get() or 14
        
        if not book or not student:
            messagebox.showerror("Ошибка", "Выберите книгу и ученика")
            return
        
        book_id = None
        student_id = None
        available = 0
        
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        
        c.execute("SELECT id, quantity FROM books WHERE title=?", (book,))
        row = c.fetchone()
        if row:
            book_id = row[0]
            total_qty = row[1]
            
            c.execute("SELECT COUNT(*) FROM issued_books WHERE book_id=? AND returned=0", (book_id,))
            issued = c.fetchone()[0]
            available = total_qty - issued
        
        if available <= 0:
            messagebox.showerror("Ошибка", "Нет доступных экземпляров")
            conn.close()
            return
        
        c.execute("SELECT id FROM students WHERE name=?", (student,))
        row = c.fetchone()
        if row:
            student_id = row[0]
        
        if book_id and student_id:
            from datetime import datetime, timedelta
            issue_date = datetime.now().strftime("%Y-%m-%d")
            return_date = (datetime.now() + timedelta(days=int(days))).strftime("%Y-%m-%d")
            
            c.execute("INSERT INTO issued_books (book_id, student_id, issue_date, return_date) VALUES (?, ?, ?, ?)",
                      (book_id, student_id, issue_date, return_date))
        
        conn.commit()
        conn.close()
        
        self.refresh_issued()

    def return_book(self):
        selected = self.issued_tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите запись")
            return
        
        item = self.issued_tree.item(selected)
        if item['values'][5] == "Возвращено":
            return
        
        issued_id = item['values'][0]
        
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("UPDATE issued_books SET returned=1 WHERE id=?", (issued_id,))
        conn.commit()
        conn.close()
        
        self.refresh_issued()

    def clear_book_fields(self):
        self.book_title.delete(0, tk.END)
        self.book_author.delete(0, tk.END)
        self.book_year.delete(0, tk.END)
        self.book_publisher.delete(0, tk.END)
        self.book_isbn.delete(0, tk.END)
        self.book_quantity.delete(0, tk.END)
        self.book_quantity.insert(0, "1")
        self.book_location.delete(0, tk.END)

    def refresh_books(self):
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)
        
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT id, title, author, year, publisher, isbn, quantity, location FROM books ORDER BY title")
        for row in c.fetchall():
            self.books_tree.insert("", tk.END, values=row)
        conn.close()
        
        self.refresh_issued_combos()

    def refresh_students(self):
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT id, name, grade, phone FROM students ORDER BY name")
        for row in c.fetchall():
            self.students_tree.insert("", tk.END, values=row)
        conn.close()
        
        self.refresh_issued_combos()

    def refresh_issued_combos(self):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        
        c.execute("SELECT title FROM books ORDER BY title")
        books = [row[0] for row in c.fetchall()]
        
        c.execute("SELECT name FROM students ORDER BY name")
        students = [row[0] for row in c.fetchall()]
        
        conn.close()
        
        self.issued_book['values'] = books
        self.issued_student['values'] = students

    def refresh_issued(self):
        for item in self.issued_tree.get_children():
            self.issued_tree.delete(item)
        
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""SELECT i.id, b.title, s.name, i.issue_date, i.return_date, i.returned
                    FROM issued_books i
                    JOIN books b ON i.book_id = b.id
                    JOIN students s ON i.student_id = s.id
                    ORDER BY i.returned, i.return_date""")
        for row in c.fetchall():
            status = "Возвращено" if row[5] else "На руках"
            self.issued_tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4], status))
        conn.close()
        
        self.refresh_issued_combos()

    def refresh_all(self):
        self.refresh_books()
        self.refresh_students()
        self.refresh_issued()

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()