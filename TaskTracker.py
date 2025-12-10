#CLI Task Tracker for Roadmap.sh 
#Made by Dtshah17 
#Published Dec 2025
#For useage refer to README.md

import os
import sys
import json 
from datetime import datetime
from enum import Enum

class TaskStatus(Enum):
    TODO = "todo"               #0
    IN_PROGRESS = "in-progress" #1
    DONE = "done"               #2

class Task:
    def __init__(self, task_id, taskDesc="", status=TaskStatus.TODO, createdOn=None):
        self.id = task_id
        self.taskDesc = taskDesc
        self.createdOn = createdOn or datetime.now().isoformat()
        self.status = TaskStatus(status)
    
    def markTD(self):
        self.status = TaskStatus.TODO
    
    def markIP(self):
        self.status = TaskStatus.IN_PROGRESS

    def markD(self):
        self.status = TaskStatus.DONE
    
    def updateDesc(self, new_desc):
        self.taskDesc = new_desc
    
    def task_dict(self):
        return {
            'id' : self.id,
            'description' : self.taskDesc,
            'status' : self.status.value,
            'created' : self.createdOn
        }

    def __str__(self):
        return f"[{self.id}]\t/{self.status}/\t{self.taskDesc}\t{self.createdOn}"

class TaskTracker:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = {}
        self.load_tasks()
    
    def load_tasks(self):
        if os.path.exist(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
                for task_id, task_data in data.items():
                    task = Task(
                        task_id=task_data['id'],
                        taskDesc=task_data['description'],
                        status=task_data['status'],
                        createdOn=task_data['created']
                    )
                    self.tasks[str(task.id)] = task

    def save_task(self):
        data = {str(task_id): task.task_dict() for task_id, task in self.tasks.items()}
        with open(self.filename, 'w') as f:
            json.dumps(data, f, indent=2)

    def next_task_id(self):
        if not self.tasks:
            return 1
        return max(int(task_id) for task_id in self.tasks.keys()) + 1
    
#Tests######################################

task1 = Task(1, "Make Program")
print(task1)

task1.markD()
task1.task_dict()

print(task1)

############################################



    

    

        
