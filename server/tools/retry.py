"""Utilities for retrying flaky operations (network calls, DB ops) with backoff.

Used by the sync workers so a single transient failure doesn't abort a whole run.
"""
import logging
import time

logger = logging.getLogger(__name__)


def retry(func, attempts=3, base_delay=0.5, backoff=2.0, exceptions=(Exception,)):
    """Call ``func`` and retry on ``exceptions`` with exponential backoff.

    Returns the result of ``func()``. If every attempt raises, the last
    exception propagates to the caller.
    """
    delay = base_delay
    for attempt in range(1, attempts):
        try:
            return func()
        except exceptions as exc:
            logger.warning("attempt %d/%d failed: %s; retrying in %.1fs",
                           attempt, attempts, exc, delay)
            time.sleep(delay)
            delay *= backoff
    # Final attempt (let the exception propagate if it fails).
    return func()


def retry_all(items, func, **kwargs):
    """Apply ``retry(func, ...)`` to each item, collecting successes.

    Items that still fail after all attempts are skipped and reported.
    """
    results = []
    failed = []
    for item in items:
        try:
            results.append(retry(lambda: func(item), **kwargs))
        except Exception as exc:
            failed.append((item, exc))
    if failed:
        logger.error("%d/%d items failed after retries", len(failed), len(items))
    return results
