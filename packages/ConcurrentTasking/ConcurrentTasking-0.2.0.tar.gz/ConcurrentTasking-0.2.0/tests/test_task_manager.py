import pytest
import asyncio
from concurrent_tasking.task_manager import TaskManager
from concurrent_tasking.models import Task, TaskStatus


@pytest.mark.asyncio
async def test_add_task():
    manager = TaskManager()

    async def sample_task(num1, num2):
        return num1 + num2

    task = Task(task_id="test1", function=sample_task, args=[1, 2])
    await manager.add_task(task)

    assert task.task_id in manager.task_registry
    assert task.status == TaskStatus.QUEUED
    assert manager.task_queue.qsize() == 1


@pytest.mark.asyncio
async def test_process_tasks():
    manager = TaskManager()

    results = []

    async def sample_task(num1, num2):
        results.append(num1 + num2)
        return num1 + num2

    task1 = Task(task_id="test_process1", function=sample_task, args=[1, 2])
    task2 = Task(task_id="test_process2", function=sample_task, args=[3, 4])
    await manager.add_task(task1)
    await manager.add_task(task2)

    # Running task processing in a background task
    processing = asyncio.create_task(manager.process_tasks())

    # Small delay to allow processing
    await asyncio.sleep(0.1)

    # Ensuring tasks are processed
    assert task1.status == TaskStatus.COMPLETED
    assert task2.status == TaskStatus.COMPLETED
    assert results == [3, 7]

    # Cleanup
    processing.cancel()


@pytest.mark.asyncio
async def test_task_status_updates():
    manager = TaskManager()

    async def sample_task(num1, num2):
        return num1 + num2

    task = Task(task_id="test_status", function=sample_task, args=[1, 2])
    await manager.add_task(task)
    assert task.status == TaskStatus.QUEUED

    processing = asyncio.create_task(manager.process_tasks())

    # Small delay to allow task to start processing
    await asyncio.sleep(0.1)

    assert task.status == TaskStatus.PROCESSING or task.status == TaskStatus.COMPLETED

    processing.cancel()


@pytest.mark.asyncio
async def test_get_task():
    manager = TaskManager()

    async def sample_task(num1, num2):
        return num1 + num2

    task_id = "test_get"
    task = Task(task_id=task_id, function=sample_task, args=[1, 2])
    await manager.add_task(task)

    retrieved_task = manager.get_task(task_id)
    assert retrieved_task == task


@pytest.mark.asyncio
async def test_get_task_position_in_queue():
    manager = TaskManager()
    manager.reset()  # Reset the state before the test

    async def sample_task(num1, num2):
        return num1 + num2

    task1 = Task(task_id="test_position1", function=sample_task, args=[1, 2])
    task2 = Task(task_id="test_position2", function=sample_task, args=[3, 4])
    await manager.add_task(task1)
    await manager.add_task(task2)

    position = manager.get_task_position_in_queue("test_position1")
    assert position == 1
    position = manager.get_task_position_in_queue("test_position2")
    assert position == 2
