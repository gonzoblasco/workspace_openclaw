# ratelimit.py
"""Implementation of a token bucket rate limiter.

This module provides a ``TokenBucket`` class that limits the rate of actions
by consuming *tokens* from a bucket.  Tokens are added to the bucket over
time at a configurable ``refill_per_second`` rate.  The bucket is
initialised full (the number of available tokens equals the ``capacity``).

All public methods are fully type‑annotated and include docstrings.
"""

from __future__ import annotations

import time
from typing import Callable


class TokenBucket:
    """A simple token‑bucket rate limiter.

    Parameters
    ----------
    capacity:
        Maximum number of tokens the bucket can hold.  ``float`` is accepted to
        allow fractional capacities.
    refill_per_second:
        Number of tokens added to the bucket each second.  Fractional values are
        permitted – e.g. ``0.5`` adds half a token every second.
    clock:
        Callable returning the current monotonic time.  Defaults to
        ``time.monotonic``.  The implementation never calls ``time.*`` directly;
        it always obtains the time from this injected callable.  This enables
        deterministic unit‑testing and safe handling of clocks that move
        backwards.
    """

    def __init__(
        self,
        capacity: float,
        refill_per_second: float,
        clock: Callable[[], float] | None = None,
    ) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if refill_per_second < 0:
            raise ValueError("refill_per_second cannot be negative")
        self._capacity: float = float(capacity)
        self._refill_rate: float = float(refill_per_second)
        # Resolve the default clock at construction time, through the module,
        # so that ``time`` is looked up lazily instead of being frozen into the
        # function signature at definition time.
        self._clock: Callable[[], float] = time.monotonic if clock is None else clock
        # The bucket starts full.
        self._tokens: float = self._capacity
        # Keep the timestamp of the last refill operation.
        self._last_timestamp: float = self._clock()

    def _refill(self) -> None:
        """Refill tokens based on elapsed time.

        The method updates ``self._tokens`` according to the time that has passed
        since the previous call.  If the injected clock moves backwards the
        implementation **does not** create extra tokens, and it never forgets
        time that has already been accounted for: the reference timestamp only
        moves forward, so a backwards jump does not let the same elapsed time be
        credited twice (and any fractional token already accrued is preserved).
        """
        now = self._clock()
        delta = now - self._last_timestamp
        if delta <= 0:
            # Clock went backwards or did not advance – keep state consistent.
            # Do not rewind the reference: the already-elapsed time keeps its
            # value, and refilling resumes only once the clock passes it again.
            return
        # Add tokens proportionally to the elapsed time.
        added = delta * self._refill_rate
        self._tokens = min(self._capacity, self._tokens + added)
        self._last_timestamp = now

    def available(self) -> float:
        """Return the number of tokens currently available.

        The bucket is first refreshed using the injected clock; the returned
        value is never greater than ``capacity``.
        """
        self._refill()
        return self._tokens

    def allow(self, cost: float = 1.0) -> bool:
        """Attempt to consume ``cost`` tokens.

        Parameters
        ----------
        cost:
            Number of tokens required for the operation.  Must be positive.

        Returns
        -------
        bool
            ``True`` if enough tokens were available and they have been
            consumed; ``False`` otherwise.  When ``cost`` exceeds ``capacity``
            the method always returns ``False`` without raising.
        """
        if cost <= 0:
            raise ValueError("cost must be positive")
        if cost > self._capacity:
            # The request can never be satisfied.
            return False
        self._refill()
        if self._tokens >= cost:
            self._tokens -= cost
            return True
        return False

    def reset(self) -> None:
        """Reset the bucket to a full state and restart the internal clock.
        """
        self._tokens = self._capacity
        self._last_timestamp = self._clock()

    # ---------------------------------------------------------------------
    # Introspection helpers (not required by the spec but useful for debugging)
    # ---------------------------------------------------------------------
    @property
    def capacity(self) -> float:
        """The maximum number of tokens the bucket can hold."""
        return self._capacity

    @property
    def refill_per_second(self) -> float:
        """The configured refill rate (tokens per second)."""
        return self._refill_rate
