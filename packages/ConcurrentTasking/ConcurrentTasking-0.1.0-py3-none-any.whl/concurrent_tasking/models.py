# async_task_processor/models.py
from datetime import datetime
from typing import Any, Dict, List, Optional, Union, Callable
from pydantic import BaseModel, Field
from enum import Enum
from .utils import time_helper


class TaskStatus(Enum):
    """
    Enum representing the possible statuses of a task.
    """

    DANGLING = "dangling"
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Task(BaseModel):
    """
    Represents a task to be processed, including its ID, status, the function to execute, its arguments, and the result.
    """

    task_id: str
    status: TaskStatus = TaskStatus.DANGLING
    function: Callable
    args: Optional[List[Any]] = []  # Positional arguments for the processing function
    kwargs: Optional[Dict[str, Any]] = (
        {}
    )  # Keyword arguments for the processing function
    result: Optional[Union[List, dict]] = None
    created_at: datetime = Field(default_factory=time_helper.get_current_time)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    @property
    def processing_duration_in_seconds(self) -> Optional[int]:
        """
        Returns the processing duration of the task in seconds.

        If the task is completed, the duration is the difference between the completion time and the start time.
        If the task is not completed, the duration is the difference between the current time and the start time.

        Returns:
            int: The processing duration of the task in seconds, or None if the task has not started yet.
        """
        if self.started_at is None:
            return None

        end_time = self.completed_at if self.completed_at else time_helper.get_current_time()
        duration = end_time - self.started_at

        return int(duration.total_seconds())

    @property
    def total_duration_in_seconds(self) -> Optional[int]:
        """
        Returns the total duration of the task in seconds.

        If the task is completed, the duration is the difference between the completion time and the creation time.
        If the task is not completed, the duration is the difference between the current time and the creation time.

        Returns:
            int: The total duration of the task in seconds, or None if the task has not been created yet.
        """
        if self.created_at is None:
            return None

        end_time = self.completed_at if self.completed_at else time_helper.get_current_time()
        duration = end_time - self.created_at

        return int(duration.total_seconds())

    def dict(self, **kwargs):
        """
        Override the dict method to include properties.
        """
        d = super().dict(**kwargs)
        d["processing_duration_in_seconds"] = self.processing_duration_in_seconds
        d["total_duration_in_seconds"] = self.total_duration_in_seconds
        return d
