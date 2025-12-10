import json
import os
from datetime import datetime
from enum import Enum

class TaskStatus(Enum):
    """Task status enumeration"""
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"

class Task:
    """Represents a single task"""
    
    def __init__(self, task_id, description, status=TaskStatus.TODO, created_at=None):
        self.id = task_id
        self.description = description
        self.status = TaskStatus(status) if isinstance(status, str) else status
        self.created_at = created_at or datetime.now().isoformat()
    
    def update_description(self, new_description):
        """Update task description"""
        self.description = new_description
    
    def mark_in_progress(self):
        """Mark task as in progress"""
        self.status = TaskStatus.IN_PROGRESS
    
    def mark_done(self):
        """Mark task as done"""
        self.status = TaskStatus.DONE
    
    def to_dict(self):
        """Convert task to dictionary"""
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status.value,
            "created_at": self.created_at
        }
    
    def __str__(self):
        return f"ID: {self.id} | [{self.status.value.upper()}] {self.description}"

class TaskTracker:
    """Manages all tasks"""
    
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = {}
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
                for task_id, task_data in data.items():
                    task = Task(
                        task_id=task_data["id"],
                        description=task_data["description"],
                        status=task_data["status"],
                        created_at=task_data["created_at"]
                    )
                    self.tasks[str(task.id)] = task
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        data = {str(task_id): task.to_dict() for task_id, task in self.tasks.items()}
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_next_id(self):
        """Get the next available task ID"""
        if not self.tasks:
            return 1
        return max(int(task_id) for task_id in self.tasks.keys()) + 1
    
    def add_task(self, description):
        """Add a new task"""
        task_id = self.get_next_id()
        task = Task(task_id, description)
        self.tasks[str(task_id)] = task
        self.save_tasks()
        return task
    
    def get_task(self, task_id):
        """Get a task by ID"""
        return self.tasks.get(str(task_id))
    
    def update_task(self, task_id, new_description):
        """Update a task's description"""
        task = self.get_task(task_id)
        if task:
            task.update_description(new_description)
            self.save_tasks()
            return True
        return False
    
    def delete_task(self, task_id):
        """Delete a task"""
        if str(task_id) in self.tasks:
            del self.tasks[str(task_id)]
            self.save_tasks()
            return True
        return False
    
    def mark_in_progress(self, task_id):
        """Mark a task as in progress"""
        task = self.get_task(task_id)
        if task:
            task.mark_in_progress()
            self.save_tasks()
            return True
        return False
    
    def mark_done(self, task_id):
        """Mark a task as done"""
        task = self.get_task(task_id)
        if task:
            task.mark_done()
            self.save_tasks()
            return True
        return False
    
    def get_all_tasks(self):
        """Get all tasks sorted by ID"""
        return sorted(self.tasks.values(), key=lambda t: t.id)
    
    def get_tasks_by_status(self, status):
        """Get tasks filtered by status"""
        status_enum = TaskStatus(status) if isinstance(status, str) else status
        return sorted(
            [t for t in self.tasks.values() if t.status == status_enum],
            key=lambda t: t.id
        )

class CLI:
    """Command-line interface for task tracker"""
    
    def __init__(self):
        self.tracker = TaskTracker()
    
    def add_command(self, description):
        """Handle add command"""
        task = self.tracker.add_task(description)
        print(f"Task added successfully (ID: {task.id})")
    
    def update_command(self, task_id, description):
        """Handle update command"""
        if self.tracker.update_task(task_id, description):
            print(f"Task {task_id} updated successfully")
        else:
            print(f"Task {task_id} not found")
    
    def delete_command(self, task_id):
        """Handle delete command"""
        if self.tracker.delete_task(task_id):
            print(f"Task {task_id} deleted successfully")
        else:
            print(f"Task {task_id} not found")
    
    def mark_in_progress_command(self, task_id):
        """Handle mark-in-progress command"""
        if self.tracker.mark_in_progress(task_id):
            print(f"Task {task_id} marked as in progress")
        else:
            print(f"Task {task_id} not found")
    
    def mark_done_command(self, task_id):
        """Handle mark-done command"""
        if self.tracker.mark_done(task_id):
            print(f"Task {task_id} marked as done")
        else:
            print(f"Task {task_id} not found")
    
    def list_command(self, status=None):
        """Handle list command"""
        print("\n" + "="*60)
        
        if status:
            tasks = self.tracker.get_tasks_by_status(status)
            print(f"Tasks ({status}):")
        else:
            tasks = self.tracker.get_all_tasks()
            print("All Tasks:")
        
        print("="*60)
        
        if not tasks:
            print("No tasks found")
        else:
            for task in tasks:
                print(task)
        
        print("="*60 + "\n")
    
    def show_help(self):
        """Show help message"""
        print("Usage:")
        print("  task-cli add <description>")
        print("  task-cli update <id> <description>")
        print("  task-cli delete <id>")
        print("  task-cli mark-in-progress <id>")
        print("  task-cli mark-done <id>")
        print("  task-cli list [status]")
    
    def run(self, args):
        """Main command handler"""
        if len(args) < 2:
            self.show_help()
            return
        
        command = args[1]
        
        try:
            if command == "add" and len(args) > 2:
                self.add_command(" ".join(args[2:]))
            elif command == "update" and len(args) > 3:
                self.update_command(int(args[2]), " ".join(args[3:]))
            elif command == "delete" and len(args) > 2:
                self.delete_command(int(args[2]))
            elif command == "mark-in-progress" and len(args) > 2:
                self.mark_in_progress_command(int(args[2]))
            elif command == "mark-done" and len(args) > 2:
                self.mark_done_command(int(args[2]))
            elif command == "list":
                status = args[2] if len(args) > 2 else None
                self.list_command(status)
            else:
                print("Invalid command")
                self.show_help()
        except (ValueError, IndexError) as e:
            print("Invalid arguments")
            self.show_help()

def main():
    """Entry point"""
    import sys
    cli = CLI()
    cli.run(sys.argv)

if __name__ == "__main__":
    main()