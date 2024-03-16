from typing import Callable
import time as t


def explicit(
    condition: Callable,
    timeout: int = 9,
    poll_frequency: float = 0.5,
    returnBool: bool = False,
):
    start = t.time()
    while (t.time() - start) < timeout:
        if condition():
            return True if returnBool else None
        t.sleep(poll_frequency)
    if returnBool:
        return False
    raise TimeoutError("Condition not met within the specified timeout.")
