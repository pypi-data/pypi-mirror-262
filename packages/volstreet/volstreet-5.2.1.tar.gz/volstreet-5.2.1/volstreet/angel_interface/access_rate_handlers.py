import asyncio
import functools
from datetime import datetime
from time import sleep
import threading
from collections import defaultdict
from volstreet.config import latency_logger
from volstreet.utils.core import current_time


class SemaphoreFactory:
    """Not being used. Did not get it to work as expected."""

    semaphores = defaultdict(dict)

    @classmethod
    def get_semaphore(cls, identifier, max_limit):
        loop = asyncio.get_running_loop()
        if identifier not in cls.semaphores[loop]:
            cls.semaphores[loop][identifier] = asyncio.Semaphore(max_limit)
        return cls.semaphores[loop][identifier]


# A class based implementation for educating myself on decorators
class AccessRateHandler:
    def __init__(self, delay=1):
        self.delay = delay + 0.1  # Add a small buffer to the delay
        self.last_call_time = datetime(
            1997, 12, 30
        )  # A date with an interesting trivia in the field of CS

    def __call__(self, func):
        def wrapped(*args, **kwargs):
            time_since_last_call = (
                current_time() - self.last_call_time
            ).total_seconds()
            if time_since_last_call < self.delay:
                sleep(self.delay - time_since_last_call)
            result = func(*args, **kwargs)
            self.last_call_time = current_time()
            return result

        return wrapped


def access_rate_handler(*, max_requests=None, per_seconds=None, is_async=False):
    request_times: list[datetime] = []

    if not is_async:
        sem = threading.Semaphore(max_requests)
        lock = threading.Lock()

        def remove_expired_request_times():
            nonlocal request_times, lock
            with lock:
                time_now = current_time()
                request_times = [
                    t
                    for t in request_times
                    if (time_now - t).total_seconds() < per_seconds
                ]

    def decorator(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            nonlocal request_times
            with sem:
                remove_expired_request_times()
                while len(request_times) >= max_requests:
                    remove_expired_request_times()
                    sleep(0.01)
                request_times.append(current_time())

            result = func(*args, **kwargs)
            return result

        @functools.wraps(func)
        async def async_wrapped(*args, **kwargs):
            """Not being used. Did not get it to work as expected."""
            semaphore = SemaphoreFactory.get_semaphore(func.__name__, max_requests)
            if "function_number" in kwargs:
                function_number = kwargs.pop("function_number")
            else:
                function_number = "NA"

            # This if else block determines the wait time
            async with semaphore:
                latency_logger.debug(
                    f"{function_number} is starting with {func.__name__}."
                )
                latency_logger.debug(
                    f"Request times before {function_number} makes http request is {request_times}. "
                    f"Length: {len(request_times)}"
                )
                while len(request_times) >= max_requests:
                    time_now = current_time()
                    oldest_request_time = request_times[0]
                    wait_time = max(
                        0,
                        per_seconds
                        - (current_time() - oldest_request_time).total_seconds(),
                    )
                    latency_logger.debug(
                        f"In access rate handling for {func.__name__}: {function_number} is waiting for {wait_time} seconds."
                        f"Based on the oldest request time: {oldest_request_time} and the current time: {time_now}."
                    )
                    if wait_time > 0:
                        latency_logger.debug(
                            f"In access rate handling for {func.__name__}: {function_number} is waiting for {wait_time} seconds."
                        )
                        await asyncio.sleep(wait_time)
                        latency_logger.debug(
                            f"In access rate handling for {func.__name__}: {function_number} is done waiting."
                        )
                    else:
                        break  # No need to wait, proceed with the request

                request_times.append(current_time())
                result = await func(*args, **kwargs)
                latency_logger.debug(f"{function_number} is done with {func.__name__}.")
                latency_logger.debug(
                    f"Request times after {function_number} is {request_times}."
                )
                return result

        return async_wrapped if is_async else wrapped

    return decorator
