# todo.py
# ---------------------------------------------
# 📝 Advanced Console-Based To-Do List Manager
# Internship-ready Python Project!
# ---------------------------------------------

import datetime

TASKS_FILE = "tasks.txt"
COMPLETED_FILE = "completed.txt"

# ------------------ Utility Functions ------------------ #
def parse_task(line):
    parts = line.strip().split(" | ")
    if len(parts) == 4:
        return {"title": parts[0], "priority": parts[1], "due": parts[2], "added": parts[3]}
    return None

def format_task(task):
    return f"{task['title']} | {task['priority']} | {task['due']} | {task['added']}"

def load_tasks():
    try:
        with open(TASKS_FILE, "r") as file:
            return [parse_task(line) for line in file.readlines() if parse_task(line)]
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        for task in tasks:
            file.write(format_task(task) + "\n")

def save_completed_task(task):
    with open(COMPLETED_FILE, "a") as file:
        file.write(format_task(task) + f" | Completed: {datetime.datetime.now()}\n")

# ------------------ Task Operations ------------------ #
def show_tasks(tasks, show_index=True):
    if not tasks:
        print("\n🗒  No tasks found.")
    else:
        print("\n📋 To-Do List:")
        print("-" * 65)
        for i, task in enumerate(tasks, 1):
            prefix = f"{i}. " if show_index else ""
            print(f"{prefix}{task['title']} | Priority: {task['priority']} | Due: {task['due']} | Added: {task['added']}")
        print("-" * 65)

def add_task(tasks):
    title = input("➕ Enter task title: ").strip()
    if not title:
        print("⚠ Task title cannot be empty.")
        return

    priority = input("⭐ Priority (High/Medium/Low): ").capitalize()
    if priority not in ["High", "Medium", "Low"]:
        priority = "Low"

    due = input("📅 Due date (YYYY-MM-DD): ")
    try:
        datetime.datetime.strptime(due, "%Y-%m-%d")
    except ValueError:
        due = "No due date"

    added = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    tasks.append({"title": title, "priority": priority, "due": due, "added": added})
    print(f"✅ Task '{title}' added.")

def remove_task(tasks):
    show_tasks(tasks)
    try:
        index = int(input("❌ Enter task number to remove: ")) - 1
        if 0 <= index < len(tasks):
            removed = tasks.pop(index)
            print(f"🗑 Task '{removed['title']}' removed.")
        else:
            print("⚠ Invalid number.")
    except ValueError:
        print("⚠ Enter a valid number.")

def mark_completed(tasks):
    show_tasks(tasks)
    try:
        index = int(input("✅ Enter task number to mark as completed: ")) - 1
        if 0 <= index < len(tasks):
            task = tasks.pop(index)
            save_completed_task(task)
            print(f"🎉 Task '{task['title']}' marked as completed.")
        else:
            print("⚠ Invalid number.")
    except ValueError:
        print("⚠ Enter a valid number.")

def show_completed_tasks():
    try:
        with open(COMPLETED_FILE, "r") as file:
            lines = file.readlines()
            if not lines:
                print("📂 No completed tasks.")
                return
            print("\n✅ Completed Tasks:")
            print("-" * 65)
            for line in lines:
                print(line.strip())
            print("-" * 65)
    except FileNotFoundError:
        print("📂 No completed tasks found.")

def search_tasks(tasks):
    keyword = input("🔍 Enter keyword to search: ").lower()
    matches = [task for task in tasks if keyword in task["title"].lower()]
    if matches:
        print("\n🔎 Search Results:")
        show_tasks(matches, show_index=False)
    else:
        print("❌ No matching tasks.")

def sort_tasks(tasks):
    print("\nSort by:")
    print("1. Priority (High → Low)")
    print("2. Due Date (Soonest First)")
    choice = input("Choose option: ").strip()

    if choice == "1":
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        tasks.sort(key=lambda t: priority_order.get(t["priority"], 3))
        print("📊 Sorted by priority.")
    elif choice == "2":
        def parse_date(d):
            try:
                return datetime.datetime.strptime(d, "%Y-%m-%d")
            except:
                return datetime.datetime.max
        tasks.sort(key=lambda t: parse_date(t["due"]))
        print("📆 Sorted by due date.")
    else:
        print("⚠ Invalid option.")

# ------------------ Main Menu ------------------ #
def main():
    tasks = load_tasks()
    print("🔷 Welcome to the Python Advanced To-Do List App 🔷")

    while True:
        print("\n=== TO-DO MENU ===")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Remove Task")
        print("4. Mark as Completed")
        print("5. Show Completed Tasks")
        print("6. Search Task")
        print("7. Sort Tasks")
        print("8. Exit")
        choice = input("👉 Choose an option (1–8): ").strip()

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
            save_tasks(tasks)
        elif choice == "3":
            remove_task(tasks)
            save_tasks(tasks)
        elif choice == "4":
            mark_completed(tasks)
            save_tasks(tasks)
        elif choice == "5":
            show_completed_tasks()
        elif choice == "6":
            search_tasks(tasks)
        elif choice == "7":
            sort_tasks(tasks)
            save_tasks(tasks)
        elif choice == "8":
            save_tasks(tasks)
            print("👋 Goodbye! All tasks saved.")
            break
        else:
            print("⚠ Invalid choice. Please select a valid option.")

if _name_ == "_main_":
    main()