# Source - https://stackoverflow.com/a/48923087
# Posted by Ihor B., modified by community. See post 'Timeline' for change history
# Retrieved 2026-09-08, License - CC BY-SA 4.0

import os
import time
from functools import wraps  # Added to preserve function metadata for Prefect

import psutil


def elapsed_since(start):
    return time.strftime("%H:%M:%S", time.gmtime(time.time() - start))


def get_process_memory():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss


def format_memory(bytes_value):
    """Converts bytes into a human-readable string (KB, MB, GB)."""
    # Handles negative consumption if memory drops during execution
    abs_value = abs(bytes_value)

    if abs_value >= 1024**3:
        value = bytes_value / (1024**3)
        unit = "GB"
    elif abs_value >= 1024**2:
        value = bytes_value / (1024**2)
        unit = "MB"
    elif abs_value >= 1024:
        value = bytes_value / 1024
        unit = "KB"
    else:
        value = bytes_value
        unit = "B"

    return f"{value:.2f} {unit}"


def track(func):
    @wraps(func)  # Keeps your Prefect tests passing (.fn works)
    def wrapper(*args, **kwargs):
        mem_before = get_process_memory()

        start = time.time()

        result = func(*args, **kwargs)

        elapsed_time = elapsed_since(start)

        mem_after = get_process_memory()

        mem_consumed = mem_after - mem_before

        print(
            f"[{func.__name__}]:"
            f"memory before: {format_memory(mem_before)} | "
            f"memory after: {format_memory(mem_after)} | "
            f"consumed: {format_memory(mem_consumed)} | "
            f"exec time: {elapsed_time}"
        )
        return result
    return wrapper
