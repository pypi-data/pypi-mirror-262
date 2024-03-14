
# ConcurrentTasking

`ConcurrentTasking` is a powerful, yet straightforward Python library for managing and processing tasks concurrently. Leveraging Python's `asyncio` library, it simplifies the queuing and asynchronous execution of tasks, providing real-time updates on their progress and outcomes.

## Features

- Efficient management of a task queue for concurrent processing.
- Asynchronous execution of tasks with live updates on their status.
- Supports any callable Python function for flexible task creation.
- Detailed tracking of task statuses, from queued to completed or failed.

## Installation

Install `ConcurrentTasking` using pip:

```bash
pip install ConcurrentTasking
```

## Quick Start

Here's how to get up and running with `ConcurrentTasking`:

1. **Define a Task**

```python
from concurrent_tasking.models import Task

# Define an asynchronous function for your task
async def sample_task_function(arg1, arg2):
    # Task logic here
    return arg1 + arg2

# Create a task instance
task = Task(task_id="1", function=sample_task_function, args=[10, 20])
```

2. **Initialize the Task Manager and Add Tasks**

```python
from concurrent_tasking.task_manager import TaskManager

manager = TaskManager()

# Queue tasks for processing
await manager.add_task(task)
```

3. **Start Task Processing**

```python
# Begin processing queued tasks
await manager.process_tasks()
```

## Contributing

Your contributions make `ConcurrentTasking` even better! Whether it's a feature request, bug report, or a pull request, we warmly welcome your input. Please feel free to open an issue or submit a PR.
