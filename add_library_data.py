import sqlite3
from datetime import datetime, timedelta

DB_NAME = "library.db"

def insert_sample_data():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute("""INSERT INTO books (title, author, year, publisher, isbn, quantity, location) 
                VALUES ('Война и мир', 'Л.Н. Толстой', '2013', 'АСТ', '978-5-17-080303-8', 3, 'Зал 1')""")
    c.execute("""INSERT INTO books (title, author, year, publisher, isbn, quantity, location) 
                VALUES ('Преступление и наказание', 'Ф.М. Достоевский', '2015', 'АСТ', '978-5-17-091982-4', 2, 'Зал 1')""")
    c.execute("""INSERT INTO books (title, author, year, publisher, isbn, quantity, location) 
                VALUES ('Евгений Онегин', 'А.С. Пушкин', '2014', 'АСТ', '978-5-17-085672-8', 5, 'Зал 1')""")
    c.execute("""INSERT INTO books (title, author, year, publisher, isbn, quantity, location) 
                VALUES ('Мастер и Маргарита', 'М.А. Булгаков', '2016', 'Эксмо', '978-5-699-86704-0', 2, 'Зал 2')""")
    c.execute("""INSERT INTO books (title, author, year, publisher, isbn, quantity, location) 
                VALUES ('Анна Каренина', 'Л.Н. Толстой', '2013', 'АСТ', '978-5-17-074393-4', 3, 'Зал 1')""")
    c.execute("""INSERT INTO books (title, author, year, publisher, isbn, quantity, location) 
                VALUES ('Физика 7 класс', 'А.В. Перышкин', '2018', 'Дрофа', '978-5-358-18774-3', 10, 'Зал 3')""")
    c.execute("""INSERT INTO books (title, author, year, publisher, isbn, quantity, location) 
                VALUES ('Алгебра 8 класс', 'Ю.Н. Макарычев', '2019', 'Просвещение', '978-5-09-068073-8', 8, 'Зал 3')""")
    c.execute("""INSERT INTO books (title, author, year, publisher, isbn, quantity, location) 
                VALUES ('История России', 'А.Н. Сахаров', '2017', 'Просвещение', '978-5-09-045747-5', 5, 'Зал 2')""")
    
    c.execute("""INSERT INTO students (name, grade, phone) VALUES ('Иванов Иван Иванович', '7А', '+7 912 345-67-89')""")
    c.execute("""INSERT INTO students (name, grade, phone) VALUES ('Петрова Анна Сергеевна', '7А', '+7 923 456-78-90')""")
    c.execute("""INSERT INTO students (name, grade, phone) VALUES ('Сидоров Алексей Петрович', '8Б', '+7 934 567-89-01')""")
    c.execute("""INSERT INTO students (name, grade, phone) VALUES ('Смирнова Елена Михайловна', '9В', '+7 945 678-90-12')""")
    c.execute("""INSERT INTO students (name, grade, phone) VALUES ('Козлов Дмитрий Викторович', '10А', '+7 956 789-01-23')""")
    
    c.execute("""INSERT INTO issued_books (book_id, student_id, issue_date, return_date, returned) 
                VALUES (1, 1, ?, ?, 0)""", 
                ((datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"), 
                 (datetime.now() + timedelta(days=9)).strftime("%Y-%m-%d")))
    c.execute("""INSERT INTO issued_books (book_id, student_id, issue_date, return_date, returned) 
                VALUES (3, 2, ?, ?, 0)""",
                ((datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"), 
                 (datetime.now() + timedelta(days=4)).strftime("%Y-%m-%d")))
    c.execute("""INSERT INTO issued_books (book_id, student_id, issue_date, return_date, returned) 
                VALUES (2, 1, ?, ?, 1)""",
                ((datetime.now() - timedelta(days=20)).strftime("%Y-%m-%d"), 
                 (datetime.now() - timedelta(days=6)).strftime("%Y-%m-%d")))
    c.execute("""INSERT INTO issued_books (book_id, student_id, issue_date, return_date, returned) 
                VALUES (4, 3, ?, ?, 0)""",
                ((datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"), 
                 (datetime.now() + timedelta(days=12)).strftime("%Y-%m-%d")))
    
    conn.commit()
    conn.close()
    print("Данные добавлены!")

if __name__ == "__main__":
    insert_sample_data()