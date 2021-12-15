import time


def now() -> int:
    return time.time_ns()


def now_plus(s=0, ms=0, ns=0) -> int:
    return (time.time_ns() +
            s * 1_000_000_000 +
            ms * 1_000_000 +
            ns)


def is_due(time_ns: int):
    return time_ns <= now()
