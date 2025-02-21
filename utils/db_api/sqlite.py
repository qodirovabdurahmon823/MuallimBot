import re
import sqlite3
from datetime import datetime
import pytz
import random
from typing import List, Optional, Dict, Any


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id int NOT NULL,
            fullname varchar(255) NOT NULL,
            username varchar(255),
            PRIMARY KEY (id)
            );
"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: int, fullname: str, username="Lomonosov"):
        sql = """
        INSERT INTO Users(id, fullname, username) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(id, fullname, username), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)


class Channel:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS channels
                                (username TEXT PRIMARY KEY UNIQUE,
                                 saved_time TEXT)''')
        self.conn.commit()

    def save_channel(self, username):
        current_time = datetime.now(pytz.timezone('Asia/Tashkent')).strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO channels VALUES (?, ?)", (username, current_time))
        self.conn.commit()

    def get_channels(self):
        self.cursor.execute("SELECT username FROM channels")
        return [row[0] for row in self.cursor.fetchall()]

    def get_time_channel(self, username):
        self.cursor.execute("SELECT saved_time FROM channels WHERE username=?", (username,))
        return result[0] if (result := self.cursor.fetchone()) else None

    def del_channel(self, username):
        self.cursor.execute("SELECT username FROM channels WHERE username=?", (username,))
        if result := self.cursor.fetchone():
            self.cursor.execute("DELETE FROM channels WHERE username=?", (username,))
            self.conn.commit()
            return True
        else:
            return False
        

    def del_channels(self):
        self.cursor.execute("DELETE FROM channels")
        self.conn.commit()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

class Subjects:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS subjects
                                (name TEXT PRIMARY KEY)''')
        self.conn.commit()

    def save_subject(self, name):
        self.cursor.execute("INSERT INTO subjects VALUES (?)", (name,))
        self.conn.commit()

    def get_subjects(self):
        self.cursor.execute("SELECT name FROM subjects")
        return [row[0] for row in self.cursor.fetchall()]


    def del_subject(self, name):
        self.cursor.execute("SELECT name FROM subjects WHERE name=?", (name,))
        if result := self.cursor.fetchone():
            self.cursor.execute("DELETE FROM subjects WHERE name=?", (name,))
            self.conn.commit()
            return True
        else:
            return False
        

    def del_subjects(self):
        self.cursor.execute("DELETE FROM subjects")
        self.conn.commit()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

class Books:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS books
                                (name TEXT,
                                 subject TEXT,
                                 file_id TEXT,
                                 message_id TEXT,
                                 PRIMARY KEY (name, subject))''')
        self.conn.commit()

    def save_book(self, name, subject, file_id, message_id):
        self.cursor.execute("INSERT INTO books VALUES (?, ?, ?, ?)", (name, subject, file_id, message_id))
        self.conn.commit()

    def edit_book(self, name, subject, file_id, message_id):
        self.cursor.execute("UPDATE books SET file_id=?, message_id=? WHERE name=? AND subject=?", (file_id, message_id, name, subject))
        self.conn.commit()


    def get_books(self, subject):
        self.cursor.execute("SELECT name, file_id, message_id FROM books WHERE subject=?", (subject,))

        return self.cursor.fetchall()
    
    def get_book(self, name, subject):
        self.cursor.execute("SELECT file_id, message_id FROM books WHERE name=? AND subject=?", (name, subject))
        return self.cursor.fetchone()

    def del_book(self, name, subject):
        self.cursor.execute("SELECT name FROM books WHERE name=? AND subject=?", (name, subject))
        if result := self.cursor.fetchone():
            self.cursor.execute("DELETE FROM books WHERE name=? AND subject=?", (name, subject))
            self.conn.commit()
            return True
        else: 
            return False

    def del_books(self):
        self.cursor.execute("DELETE FROM books")
        self.conn.commit()


class Lessons:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS lessons
                                (name TEXT,
                                 subject TEXT,
                                 file_id TEXT,
                                 message_id TEXT,
                                 PRIMARY KEY (name, subject))''')
        self.conn.commit()


    def save_lesson(self, name, subject, file_id, message_id):
        self.cursor.execute("INSERT INTO lessons VALUES (?, ?, ?, ?)", (name, subject, file_id, message_id))
        self.conn.commit()


    def get_lessons(self, subject):
        self.cursor.execute("SELECT name, file_id, message_id FROM lessons WHERE subject=?", (subject,))
        return self.cursor.fetchall()
    
    def edit_lesson(self, name, subject, file_id, message_id):
        self.cursor.execute("UPDATE lessons SET file_id=?, message_id=? WHERE name=? AND subject=?", (file_id, message_id, name, subject))
        self.conn.commit()


    def get_lesson(self, name, subject):
        self.cursor.execute("SELECT file_id, message_id FROM lessons WHERE name=? AND subject=?", (name, subject))
        return self.cursor.fetchone()

    def del_lesson(self, name, subject):
        self.cursor.execute("SELECT name FROM lessons WHERE name=? AND subject=?", (name, subject))
        if result := self.cursor.fetchone():
            self.cursor.execute("DELETE FROM lessons WHERE name=? AND subject=?", (name, subject))
            self.conn.commit()
            return True
        else:
            return False

    def del_lessons(self):
        self.cursor.execute("DELETE FROM lessons")
        self.conn.commit()



class TestsDB:
    def __init__(self, db_name="tests.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._initialize_db()

    def _initialize_db(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            test_name TEXT NOT NULL,
            shuffling_type TEXT NOT NULL,
            time INTEGER NOT NULL,
            test_type TEXT NOT NULL DEFAULT 'themed',
            created_time TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            options TEXT NOT NULL,
            correct_option INTEGER NOT NULL,
            FOREIGN KEY(test_id) REFERENCES tests(id)
        )
        """)
        self.conn.commit()

    def create_test(self, subject: str, test_name: str, shuffling_type: str, time: int, test_type: str = "themed") -> int:
        self.cursor.execute("""
        INSERT INTO tests (subject, test_name, shuffling_type, time, test_type)
        VALUES (?, ?, ?, ?, ?)
        """, (subject, test_name, shuffling_type, time, test_type))
        self.conn.commit()
        return self.cursor.lastrowid
        
    def get_tests(self, subject: Optional[str] = None, limit: int = 5, page: int = 1, test_type: str = "themed"):
        page = int(page)
        offset = (int(page) - 1) * limit
        if subject:
            if test_type.lower() == "all":
                self.cursor.execute("""
                SELECT id, test_name FROM tests
                WHERE subject = ?
                ORDER BY id DESC LIMIT ? OFFSET ?
                """, (subject, limit, offset))
                tests = self.cursor.fetchall()
                self.cursor.execute("SELECT COUNT(*) FROM tests WHERE subject = ?", (subject,))
            else:
                self.cursor.execute("""
                SELECT id, test_name FROM tests
                WHERE subject = ? AND test_type = ?
                ORDER BY id DESC LIMIT ? OFFSET ?
                """, (subject, test_type, limit, offset))
                tests = self.cursor.fetchall()
                self.cursor.execute("SELECT COUNT(*) FROM tests WHERE subject = ? AND test_type = ?", (subject, test_type))
        else:
            if test_type.lower() == "all":
                self.cursor.execute("""
                SELECT id, test_name FROM tests
                ORDER BY id DESC LIMIT ? OFFSET ?
                """, (limit, offset))
                tests = self.cursor.fetchall()
                self.cursor.execute("SELECT COUNT(*) FROM tests")
            else:
                self.cursor.execute("""
                SELECT id, test_name FROM tests
                WHERE test_type = ?
                ORDER BY id DESC LIMIT ? OFFSET ?
                """, (test_type, limit, offset))
                tests = self.cursor.fetchall()
                self.cursor.execute("SELECT COUNT(*) FROM tests WHERE test_type = ?", (test_type,))
        count_result = self.cursor.fetchone()
        total_tests = count_result[0] if count_result else 0
        total_pages = (total_tests + limit - 1) // limit
        return {
            "tests": [{"id": test[0], "name": test[1]} for test in tests],
            "has_next_page": page < total_pages,
            "next_page": page + 1 if page < total_pages else None,
            "has_previous_page": page > 1,
            "previous_page": page - 1 if page > 1 else None,
            "first_page": 1 if total_pages > 0 else None,
            "last_page": total_pages if total_pages > 0 else None,
            "current_page": page,
            "total_pages": total_pages,
        }




    def add_question(self, test_id: int, question: str, options: List[str], correct_option: int):
        self.cursor.execute("""
        SELECT id FROM tests WHERE id = ?
        """, (test_id,))
        if self.cursor.fetchone() is None:
            raise ValueError(f"Test with ID '{test_id}' does not exist.")
        options_str = ";".join(options)
        self.cursor.execute("""
        INSERT INTO questions (test_id, question, options, correct_option)
        VALUES (?, ?, ?, ?)
        """, (test_id, question, options_str, correct_option))
        self.conn.commit()


    def get_test(self, test_id: int) -> List[Dict[str, Any]]:
        self.cursor.execute("""
        SELECT shuffling_type FROM tests WHERE id = ?
        """, (test_id,))
        result = self.cursor.fetchone()
        if result is None:
            raise ValueError(f"Test with ID '{test_id}' does not exist.")
        shuffling_type = result[0]
        self.cursor.execute("SELECT * FROM questions WHERE test_id = ?", (test_id,))
        questions = self.cursor.fetchall()
        result = []
        for q in questions:
            question_id, _, question, options, correct_option = q
            options_list = options.split(";")
            result.append({
                "question": question,
                "options": options_list,
                "correct_option": correct_option,
                "question_id": question_id
            })
        if shuffling_type == "shuffle_all":
            random.shuffle(result)
            for r in result:
                answers = list(enumerate(r['options']))
                random.shuffle(answers)
                correct_index = [i for i, opt in answers].index(r["correct_option"])
                r["options"] = [opt for i, opt in answers]
                r["correct_option"] = correct_index
        elif shuffling_type == "shuffle_questions":
            random.shuffle(result)
        elif shuffling_type == "shuffle_answers":
            for r in result:
                answers = list(enumerate(r['options']))
                random.shuffle(answers)
                correct_index = [i for i, opt in answers].index(r["correct_option"])
                r["options"] = [opt for i, opt in answers]
                r["correct_option"] = correct_index
        return result


    def get_information(self, test_id: int) -> Dict[str, Any]:
        self.cursor.execute("""
        SELECT id, created_time, subject, test_name, shuffling_type, time, test_type
        FROM tests
        WHERE id = ?
        """, (test_id,))
        test_data = self.cursor.fetchone()
        if test_data is None:
            raise ValueError(f"Test with ID '{test_id}' does not exist.")
        test_id, created_time, test_subject, test_name, shuffling_type, time, test_type = test_data
        self.cursor.execute("""
        SELECT COUNT(*) FROM questions WHERE test_id = ?
        """, (test_id,))
        total_questions = self.cursor.fetchone()[0]
        return {
            "id": test_id,
            "created_time": created_time,
            "subject": test_subject,
            "test_name": test_name,
            "total_questions": total_questions,
            "shuffling_type": shuffling_type,
            "timer": time,
            "type": test_type
        }

    def change_shuffling_type(self, test_id: int, shuffling_type: str):
        self.cursor.execute("""
        UPDATE tests SET shuffling_type = ? WHERE id = ?
        """, (shuffling_type, test_id))
        self.conn.commit()

    def change_time(self, test_id: int, time: int):
        self.cursor.execute("""
        UPDATE tests SET time = ? WHERE id = ?
        """, (time, test_id))
        self.conn.commit()

    def delete_test(self, test_id: int) -> None:
        self.cursor.execute("""
        SELECT id FROM tests WHERE id = ?
        """, (test_id,))
        if self.cursor.fetchone() is None:
            raise ValueError(f"Test with ID '{test_id}' does not exist.")
        self.cursor.execute("""
        DELETE FROM questions WHERE test_id = ?
        """, (test_id,))
        self.cursor.execute("""
        DELETE FROM tests WHERE id = ?
        """, (test_id,))
        self.conn.commit()

    def parse_and_save_test(self, test_name: str, text: str):
        question_blocks = self._split_questions(text)
        for question, options, correct_option in question_blocks:
            self.add_question(test_name, question, options, correct_option)

    def _split_questions(self, text: str) -> List[tuple]:
        question_blocks = re.split(r"~", text)[1:]
        questions = []
        for block in question_blocks:
            lines = block.strip().split("\n")
            question = lines[0].strip()
            options = []
            correct_option = None
            for line in lines[1:]:
                if line.startswith("=="):
                    options.append(line[2:].strip())
                elif line.startswith("*="):
                    options.append(line[2:].strip())
                    correct_option = len(options) - 1
            if correct_option is None:
                raise ValueError(f"Correct answer is missing for question: '{question}'")
            questions.append((question, options, correct_option))
        return questions

    def _get_test_id(self, subject: str, test_name: str) -> Optional[int]:
        self.cursor.execute("""
        SELECT id FROM tests WHERE subject = ? AND test_name = ?
        """, (subject, test_name))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_test_by_id(self, test_id: int) -> Dict[str, Any]:
        self.cursor.execute("""
        SELECT id, subject, test_name, shuffling_type, time FROM tests WHERE id = ?
        """, (test_id,))
        test_data = self.cursor.fetchone()
        if test_data is None:
            raise ValueError(f"Test with ID '{test_id}' does not exist.")
        test_id, subject, test_name, shuffling_type, time = test_data
        self.cursor.execute("""
        SELECT question, options, correct_option FROM questions WHERE test_id = ?
        """, (test_id,))
        questions = self.cursor.fetchall()
        return {
            "id": test_id,
            "subject": subject,
            "test_name": test_name,
            "shuffling_type": shuffling_type,
            "time": time,
            "questions": [
                {
                    "question": q[0],
                    "options": q[1].split(";"),
                    "correct_option": q[2]
                } for q in questions
            ]
        }
