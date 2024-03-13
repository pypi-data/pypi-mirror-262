# tests/test_async_task_processor.py
import asyncio
import pytest
from async_task_processor.async_task_processor import AsyncTaskProcessor
from async_task_processor.models import Task, TaskStatus

@pytest.mark.asyncio
async def test_task_addition():
    processor = AsyncTaskProcessor()
    task = Task(task_id="1", function=asyncio.sleep, args=[0])
    await processor.add_task(task)
    assert task.task_id in processor.task_registry
    assert processor.task_queue.qsize() == 1

@pytest.mark.asyncio
async def test_task_processing():
    async def dummy_processing_function(*args, **kwargs):
        return "processed"

    processor = AsyncTaskProcessor()
    task = Task(task_id="2", function=dummy_processing_function)
    await processor.add_task(task)
    
    # Start the processor in a background task
    processing_task = asyncio.create_task(processor.process_tasks())
    
    # Give it a little bit of time to process
    await asyncio.sleep(0.1)
    
    assert task.status == TaskStatus.COMPLETED
    assert task.result == "processed"
    
    # Cleanup: Cancel the background processing task
    processing_task.cancel()
    try:
        await processing_task  # Await the task to catch the cancellation
    except asyncio.CancelledError:
        pass  # Expected due to cancellation

@pytest.mark.asyncio
async def test_failed_task_processing():
    async def failing_processing_function(*args, **kwargs):
        raise ValueError("Intentional failure")

    processor = AsyncTaskProcessor()
    task = Task(task_id="3", function=failing_processing_function)
    await processor.add_task(task)
    
    processing_task = asyncio.create_task(processor.process_tasks())
    await asyncio.sleep(0.1)  # Give it time to fail
    
    assert task.status == TaskStatus.FAILED
    assert "Intentional failure" in task.result["error"]
    
    processing_task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await processing_task

