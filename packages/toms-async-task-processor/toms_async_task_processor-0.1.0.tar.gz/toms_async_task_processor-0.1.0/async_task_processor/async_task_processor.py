# async_task_processor/async_task_processor.py
import asyncio
from .models import Task, TaskStatus
from .utils import time


class AsyncTaskProcessor:
    """
    Manages the queue of tasks for asynchronous processing.
    Holds tasks in a queue and processes them sequentially, updating their status and results.
    """

    def __init__(self):
        """
        Initializes the QueueManager with an empty asyncio queue and an empty task registry.
        """
        self.task_queue = asyncio.Queue()
        self.task_registry = {}
        self.queue_order = [] # A simple list to track the order of task IDs in the queue

    async def add_task(self, task: Task):
        """
        Adds a task to the queue and registers it in the task registry.

        Args:
            task (Task): The task object to be added to the queue.
        """
        await self.task_queue.put(task)
        self.task_registry[task.task_id] = task
        self.queue_order.append(task.task_id)  # Add task ID to queue_order list
        task.status = TaskStatus.QUEUED

    async def process_tasks(self):
        while True:
            task = await self.task_queue.get()  # Wait for a task
            task.started_at = time.get_current_time()  # Mark start time
            try:
                print(f"Processing task {task.task_id} with GPU")
                task.status = TaskStatus.PROCESSING
                
                task.result = await task.function(*task.args, **task.kwargs)
                task.status = TaskStatus.COMPLETED
                    
            except Exception as e:
                task.status = TaskStatus.FAILED
                task.result = {"error": str(e)}
                print(f"Error processing task {task.task_id}: {e}")
            finally:
                self.task_queue.task_done()
                task.completed_at = time.get_current_time()  # Ensure completion time is marked even on failure
                if task.task_id in self.queue_order:
                    self.queue_order.remove(task.task_id)  # Update this line to remove task ID from queue_order
    
    def get_task_position_in_queue(self, task_id: str) -> int:
        """
        Retrieves the position of a task in the queue by its ID.

        Args:
            task_id (str): The unique identifier of the task.

        Returns:
            int: The position of the task in the queue, or -1 if the task is not queued.
        """
        if task_id in self.queue_order:
            return self.queue_order.index(task_id) + 1
        else:
            return -1
        
    def get_task(self, task_id: str) -> Task:
        """
        Retrieves a task by its ID.
        
        Args:
            task_id (str): The unique identifier of the task.
        
        Returns:
            Task: The task object with the given ID, or None if no task is found.
        """
        return self.task_registry.get(task_id)

async_task_processor = AsyncTaskProcessor()
