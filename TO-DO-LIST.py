import json
from datetime import datetime, date
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class Task:
    def __init__(self, description, due_date=None, priority=1, completed=False):
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.completed = completed
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "description": self.description,
            "due_date": self.due_date.strftime("%Y-%m-%d") if self.due_date else None,
            "priority": self.priority,
            "completed": self.completed,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(data["description"])
        task.due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date() if data["due_date"] else None
        task.priority = data["priority"]
        task.completed = data["completed"]
        task.created_at = data["created_at"]
        return task


class ToDoList:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, description, due_date=None, priority=1):
        if due_date:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        task = Task(description, due_date, priority)
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()

    def mark_complete(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = True
            self.save_tasks()

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump([task.to_dict() for task in self.tasks], f)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(task_data) for task_data in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []


class ToDoApp(tk.Tk):
    def __init__(self, todo_list):
        super().__init__()
        self.todo_list = todo_list
        self.title("To-Do List Application")
        self.geometry("800x600")  # Enlarged window

        self.create_widgets()
        self.refresh_task_list()

    def create_widgets(self):
        # Input Frame
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Task Description:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.desc_entry = tk.Entry(input_frame, width=40, font=("Arial", 14))
        self.desc_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(input_frame, text="Due Date (YYYY-MM-DD):", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.due_entry = tk.Entry(input_frame, width=20, font=("Arial", 14))
        self.due_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        tk.Label(input_frame, text="Priority (1-5):", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.priority_spin = tk.Spinbox(input_frame, from_=1, to=5, width=5, font=("Arial", 14))
        self.priority_spin.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        add_button = tk.Button(self, text="Add Task", command=self.add_task, font=("Arial", 14), bg="#4CAF50", fg="white")
        add_button.pack(pady=10)

        # Task List
        self.tree = ttk.Treeview(self, columns=("Description", "Due", "Priority", "Status"), show="headings", height=15)
        self.tree.heading("Description", text="Description")
        self.tree.heading("Due", text="Due Date")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Status", text="Status")
        self.tree.column("Description", width=300)
        self.tree.column("Due", width=100)
        self.tree.column("Priority", width=100)
        self.tree.column("Status", width=100)
        self.tree.pack(pady=10)

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        mark_button = tk.Button(btn_frame, text="Mark as Complete", command=self.mark_complete, font=("Arial", 12))
        mark_button.grid(row=0, column=0, padx=10)

        remove_button = tk.Button(btn_frame, text="Remove Task", command=self.remove_task, font=("Arial", 12))
        remove_button.grid(row=0, column=1, padx=10)

    def refresh_task_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, task in enumerate(self.todo_list.tasks):
            due = task.due_date.strftime("%Y-%m-%d") if task.due_date else "N/A"
            status = "✓" if task.completed else "✗"
            self.tree.insert("", "end", iid=i, values=(task.description, due, task.priority, status))

    def add_task(self):
        desc = self.desc_entry.get()
        due = self.due_entry.get()
        priority = self.priority_spin.get()

        if not desc.strip():
            messagebox.showerror("Error", "Task description cannot be empty.")
            return

        try:
            priority = int(priority)
            if not 1 <= priority <= 5:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Priority must be an integer between 1 and 5.")
            return

        try:
            self.todo_list.add_task(desc, due if due else None, priority)
            self.refresh_task_list()
            self.desc_entry.delete(0, tk.END)
            self.due_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Invalid due date format. Use YYYY-MM-DD.")

    def mark_complete(self):
        selected = self.tree.selection()
        if selected:
            index = int(selected[0])
            self.todo_list.mark_complete(index)
            self.refresh_task_list()
        else:
            messagebox.showwarning("Warning", "Select a task to mark as complete.")

    def remove_task(self):
        selected = self.tree.selection()
        if selected:
            index = int(selected[0])
            self.todo_list.remove_task(index)
            self.refresh_task_list()
        else:
            messagebox.showwarning("Warning", "Select a task to remove.")


if __name__ == "__main__":
    todo_list = ToDoList()
    app = ToDoApp(todo_list)
    app.mainloop()