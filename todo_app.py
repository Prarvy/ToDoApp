# Designed by Prakash Srinivasan ( prarvy@gmail.com )
# Project Name: To Do App
# Version: 1.0: Base version by author
import sqlite3

header_names = ["Task ID", "Task Name", "Priority"]
header_widths = [10, 40, 10]
column_order = [0, 1, 2]


class ToDo:
    def __init__(self):
        self.conn = sqlite3.connect('todo.db')
        self.c = self.conn.cursor()
        self.create_task_table()

    def create_task_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                     id INTEGER PRIMARY KEY,
                     name TEXT NOT NULL,
                     priority INTEGER NOT NULL
                     );''')

    @staticmethod
    def print_menu():
        print("""
+------------------------------------------------------------------------------+
|                              To Do App:  M E N U                             |
+==============================================================================+
| 1. Show Tasks | 2. Add Task | 3. Change Priority | 4. Delete Task | 5. Exit  |        
+------------------------------------------------------------------------------+""")

    @staticmethod
    def print_header():
        print('+' + '-' * 78 + '+')
        print(*[n.ljust(w).upper() for n, w in zip(header_names, header_widths)], sep='| ')
        print('+' + '-' * 78 + '+')

    @staticmethod
    def read_user_choice():
        while True:
            try:
                _choice = int(input('>>> Enter your choice (1 - 5): '))
            except ValueError:
                print('Your Choice is not an Integer. Please re-try.')
                continue
            if _choice not in range(1, 6):
                print('Your Choice entered is not in the range 1 to 5. Please re-try.')
                continue
            return _choice

    def enter_name(self):
        while True:
            input_name = input('>>> Enter Task Name: ').strip()
            if input_name == '':
                print('Info: Received an Empty String. Task Name cannot be empty.')
                continue
            if self.find_task_name(input_name) is not None:
                print('You have entered an existing name. Please Retry with different name.')
                continue
            return input_name

    @staticmethod
    def enter_id(msg):
        while True:
            try:
                input_id = int(input(msg).strip())
            except ValueError:
                print('Entered data is not an Integer. Please re-try.')
                continue
            if input_id < 1:
                print('ID should not be less than 1. Please re-try.')
                continue
            return input_id

    @staticmethod
    def enter_priority():
        while True:
            try:
                input_priority = int(input('>>> Enter Priority: ').strip())
            except ValueError:
                print('Entered data is not an Integer. Please re-try.')
                continue
            if input_priority < 1:
                print('Priority should not be less than 1. Please re-try.')
                continue
            return input_priority

    def add_task(self):
        name = self.enter_name()
        priority = self.enter_priority()
        self.c.execute('INSERT INTO tasks (name, priority) VALUES (?,?)', (name, priority))
        self.conn.commit()
        print('The Task added successfully.')

    def find_task_name(self, name):
        self.c.execute('SELECT * FROM tasks WHERE name = ?', (name,))
        data = self.c.fetchone()
        if data is None:
            return None
        return data

    def find_task_id(self, _id):
        self.c.execute('SELECT * FROM tasks WHERE id = ?', (_id,))
        data = self.c.fetchone()
        if data is None:
            return False
        return True

    def change_priority(self):
        task_id = self.enter_id('>>> Enter Task ID to change Priority: ')
        if self.find_task_id(task_id):
            priority = self.enter_priority()
            self.c.execute('UPDATE tasks SET priority = ? WHERE id = ?', (priority, task_id))
            self.conn.commit()
            print('Status: Priority of Task ID: {} updated Successfully.'.format(task_id))
        else:
            print("The Task ID doesn't exists. Please retry with a different ID.")

    def delete_task(self):
        task_id = self.enter_id('>>> Enter Task ID to delete: ')
        if self.find_task_id(task_id):
            self.c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            self.conn.commit()
            print('Status: Task ID: {} deleted Successfully.'.format(task_id))
        else:
            print("The Task ID doesn't exists. Please retry with a different ID.")

    @staticmethod
    def print_task(data):
        print(*[str(data[n]).ljust(w) for (n, w) in zip(column_order, header_widths)], sep='| ')

    def show_tasks(self):

        self.c.execute('SELECT * FROM tasks')
        rows = self.c.fetchall()
        if len(rows) == 0:
            print("No Task is available to display.")
        else:
            self.print_header()
            for _task in rows:
                task = list(_task)
                self.print_task(task)


while True:
    app = ToDo()
    app.print_menu()
    choice = app.read_user_choice()
    if choice == 1:
        app.show_tasks()
    elif choice == 2:
        app.add_task()
    elif choice == 3:
        app.change_priority()
    elif choice == 4:
        app.delete_task()
    elif choice == 5:
        print('The application is Exiting. Bye!')
        break
