"""Regression and mutation-killing tests for ``ratelimit.TokenBucket``.

This file is the "safety net" of the ABC pipeline (agent C).  It covers the
invariants that the spec (``spec3.md``) demands and that the buggy version
written by agent A violated:

* the clock must never be able to *mint* extra tokens when it moves backwards;
* the injected clock is the only source of time;
* the refill is fractional and always capped at ``capacity``;
* ``cost <= 0`` raises ``ValueError`` and ``cost > capacity`` returns ``False``;
* ``reset()`` refills the bucket *and* restarts the internal timestamp;
* the default clock is resolved lazily (``None`` in the signature), not frozen
  into the function defaults at import time.
"""

from __future__ import annotations

import inspect
import time
import unittest
from typing import Callable

from ratelimit import TokenBucket


class FakeClock:
    """Deterministic, manually driven clock."""

    def __init__(self, start: float = 0.0):
        self.time = float(start)

    def __call__(self) -> float:
        return self.time

    def advance(self, delta: float) -> None:
        self.time += delta

    def set(self, value: float) -> None:
        self.time = float(value)


class TestClockRewindRegression(unittest.TestCase):
    """The bug agent B really fixed: a backwards clock must not mint tokens."""

    def test_backwards_clock_does_not_mint_tokens(self):
        """Regression for the minting bug fixed by B.

        With capacity=3 and refill_per_second=1: two tokens are consumed, so
        one token is left.  After one second of clock the bucket holds
        ``1 + 1 * 1 = 2`` tokens (refill *by rate*, not a full recharge).
        Rewinding the clock by 0.5s and coming back must not credit the
        elapsed interval a second time: the buggy implementation re-wound
        ``_last_timestamp`` and ended up with 2.5 tokens.
        """
        clock = FakeClock()
        bucket = TokenBucket(capacity=3, refill_per_second=1.0, clock=clock)

        bucket.allow()
        bucket.allow()
        self.assertEqual(bucket.available(), 1.0)

        clock.advance(1.0)
        self.assertEqual(bucket.available(), 2.0)

        # The clock goes backwards.
        clock.advance(-0.5)
        self.assertEqual(bucket.available(), 2.0)

        # ... and comes back to the very same instant it was before.
        clock.advance(0.5)
        # The interval [0.5, 1.0] was already credited; crediting it twice
        # would mint half a token.
        self.assertEqual(bucket.available(), 2.0)

    def test_backwards_clock_never_exceeds_elapsed_refill(self):
        """After any sequence of backwards jumps, the tokens accrued must not
        exceed ``elapsed_seconds * refill_rate`` (spec item 7)."""
        clock = FakeClock()
        capacity = 10.0
        rate = 2.0
        bucket = TokenBucket(capacity=capacity, refill_per_second=rate, clock=clock)

        bucket.allow(capacity)  # empty the bucket
        self.assertEqual(bucket.available(), 0.0)

        clock.advance(1.0)
        self.assertEqual(bucket.available(), 2.0)

        # Backwards jump of 0.75s, then forward again: only 0.25s of *new*
        # time may be credited.
        clock.advance(-0.75)
        self.assertEqual(bucket.available(), 2.0)
        clock.advance(1.0)
        self.assertAlmostEqual(bucket.available(), 2.5)

    def test_backwards_clock_keeps_bucket_consistent(self):
        """A backwards clock must not corrupt the state: a later allow() must
        still respect the (unchanged) token count."""
        clock = FakeClock()
        bucket = TokenBucket(capacity=3, refill_per_second=1.0, clock=clock)

        bucket.allow()
        clock.advance(-100.0)  # wild backwards jump
        self.assertEqual(bucket.available(), 2.0)
        self.assertTrue(bucket.allow())
        self.assertEqual(bucket.available(), 1.0)
        self.assertTrue(bucket.allow())
        self.assertEqual(bucket.available(), 0.0)
        self.assertFalse(bucket.allow())
        self.assertEqual(bucket.available(), 0.0)


class TestInjectedClockIsTheOnlyClock(unittest.TestCase):
    """Spec item 4: the refill uses the injected clock, never ``time.*``."""

    def test_refill_uses_injected_clock_not_wall_clock(self):
        """Mutation ``now = time.time()`` must be detected.

        If the implementation queried the real wall clock, the tiny amount of
        time spent inside the test would be credited and the bucket would jump
        straight to ``capacity``.
        """
        clock = FakeClock()
        bucket = TokenBucket(capacity=5, refill_per_second=1.0, clock=clock)
        bucket.allow(5)
        self.assertEqual(bucket.available(), 0.0)

        clock.advance(1.0)
        # Exactly one token of refill, and not a single extra.
        self.assertEqual(bucket.available(), 1.0)

    def test_default_clock_is_monotonic_not_wall_clock(self):
        """The default clock must be ``time.monotonic``."""
        bucket = TokenBucket(capacity=1, refill_per_second=1.0)
        self.assertIs(bucket._clock, time.monotonic)


class TestRefillSemantics(unittest.TestCase):
    """Spec items 3 and 4: fractional refill, capped at capacity."""

    def test_refill_is_fractional_not_rounded(self):
        """Mutation ``int(delta * rate)`` must be detected."""
        clock = FakeClock()
        bucket = TokenBucket(capacity=2, refill_per_second=0.5, clock=clock)
        bucket.allow()
        self.assertEqual(bucket.available(), 1.0)

        clock.advance(0.5)
        # 0.5 tokens * 0.5 rate = 0.25 tokens, not 0.
        self.assertAlmostEqual(bucket.available(), 1.25)

    def test_refill_is_fractional_with_small_rate(self):
        clock = FakeClock()
        bucket = TokenBucket(capacity=1, refill_per_second=0.1, clock=clock)
        bucket.allow()
        self.assertEqual(bucket.available(), 0.0)
        clock.advance(0.3)
        self.assertAlmostEqual(bucket.available(), 0.03)

    def test_refill_is_capped_at_capacity(self):
        """Mutation that drops the ``min(capacity, ...)`` must be detected."""
        clock = FakeClock()
        bucket = TokenBucket(capacity=3, refill_per_second=1.0, clock=clock)
        clock.advance(100.0)
        self.assertEqual(bucket.available(), 3.0)

    def test_available_never_exceeds_capacity(self):
        """Property: ``available()`` is always within ``[0, capacity]``."""
        clock = FakeClock()
        capacity = 4.0
        bucket = TokenBucket(capacity=capacity, refill_per_second=0.7, clock=clock)
        for step in range(40):
            clock.advance(0.3)
            bucket.allow(1.0)
            bucket.allow(0.5)
            value = bucket.available()
            self.assertLessEqual(value, capacity)
            self.assertGreaterEqual(value, 0.0)


class TestCostValidation(unittest.TestCase):
    """Spec items 5 and 6."""

    def test_cost_greater_than_capacity_returns_false_without_raising(self):
        """Mutation that raises instead of returning ``False`` must be caught."""
        clock = FakeClock()
        bucket = TokenBucket(capacity=2, refill_per_second=1.0, clock=clock)
        self.assertFalse(bucket.allow(999))
        # State must be untouched.
        self.assertEqual(bucket.available(), 2.0)

    def test_cost_greater_than_capacity_stays_false_forever(self):
        clock = FakeClock()
        bucket = TokenBucket(capacity=2, refill_per_second=100.0, clock=clock)
        for _ in range(5):
            self.assertFalse(bucket.allow(3))
            clock.advance(10.0)
        self.assertEqual(bucket.available(), 2.0)

    def test_non_positive_cost_raises_value_error(self):
        """Mutation that drops the validation must be detected."""
        clock = FakeClock()
        bucket = TokenBucket(capacity=1, refill_per_second=1.0, clock=clock)
        for bad in (0, 0.0, -1, -0.5):
            with self.assertRaises(ValueError):
                bucket.allow(bad)
        # The failed calls must not have consumed anything.
        self.assertEqual(bucket.available(), 1.0)


class TestTokenAccountingProperties(unittest.TestCase):
    """Property based checks over the token arithmetic."""

    def test_available_equals_capacity_minus_consumed(self):
        """After N allows of cost 1 with capacity K, ``available() == K - N``."""
        capacity = 5
        clock = FakeClock()
        bucket = TokenBucket(capacity=capacity, refill_per_second=1.0, clock=clock)
        for n in range(capacity):
            allowed = bucket.allow(1.0)
            self.assertTrue(allowed)
            self.assertEqual(bucket.available(), float(capacity - (n + 1)))
        # One more allow must fail and consume nothing.
        self.assertFalse(bucket.allow(1.0))
        self.assertEqual(bucket.available(), 0.0)

    def test_failed_allow_consumes_nothing(self):
        clock = FakeClock()
        bucket = TokenBucket(capacity=2, refill_per_second=0.0, clock=clock)
        self.assertTrue(bucket.allow())
        self.assertTrue(bucket.allow())
        self.assertFalse(bucket.allow())
        self.assertEqual(bucket.available(), 0.0)

    def test_big_clock_jump_is_capped_at_capacity(self):
        clock = FakeClock()
        bucket = TokenBucket(capacity=3, refill_per_second=0.5, clock=clock)
        clock.advance(10_000.0)
        self.assertEqual(bucket.available(), 3.0)


class TestReset(unittest.TestCase):
    """Spec item 8."""

    def test_reset_restores_full_bucket(self):
        clock = FakeClock()
        bucket = TokenBucket(capacity=4, refill_per_second=1.0, clock=clock)
        bucket.allow(2)
        self.assertEqual(bucket.available(), 2.0)
        bucket.reset()
        self.assertEqual(bucket.available(), 4.0)

    def test_reset_restarts_the_internal_timestamp(self):
        """After a reset, the internal timestamp must be the current instant.

        If ``reset()`` refilled the tokens but left a stale ``_last_timestamp``,
        the next interval would be credited twice and the bucket would refill
        faster than the configured rate.
        """
        clock = FakeClock()
        capacity = 4.0
        bucket = TokenBucket(capacity=capacity, refill_per_second=1.0, clock=clock)

        clock.advance(10.0)
        bucket.reset()
        self.assertEqual(bucket.available(), capacity)
        # The internal clock reference was restarted at the reset instant.
        self.assertAlmostEqual(bucket._last_timestamp, 10.0)

        # Empty the bucket, then wait exactly one second.
        self.assertTrue(bucket.allow(capacity))
        self.assertEqual(bucket.available(), 0.0)
        clock.advance(1.0)
        self.assertAlmostEqual(bucket.available(), 1.0)

    def test_reset_then_backwards_clock_does_not_recredit_old_time(self):
        """A reset followed by a backwards clock must not re-credit the time
        that elapsed before the reset."""
        clock = FakeClock()
        bucket = TokenBucket(capacity=4.0, refill_per_second=1.0, clock=clock)

        clock.advance(10.0)
        bucket.reset()
        # The clock goes back before the reset instant.
        clock.set(5.0)
        self.assertEqual(bucket.available(), 4.0)
        # Empty the bucket and come back to the reset instant: no time may be
        # credited for the interval before the reset.
        self.assertTrue(bucket.allow(4.0))
        self.assertEqual(bucket.available(), 0.0)
        clock.set(10.0)
        self.assertAlmostEqual(bucket.available(), 0.0)

    def test_reset_does_not_accumulate_extra_tokens(self):
        clock = FakeClock()
        capacity = 3.0
        bucket = TokenBucket(capacity=capacity, refill_per_second=1.0, clock=clock)
        bucket.reset()
        clock.advance(1000.0)
        self.assertEqual(bucket.available(), capacity)


class TestClockDefaultIsResolvedLazily(unittest.TestCase):
    """The default clock must not be a ``time.*`` captured in the signature."""

    def test_init_defaults_contain_no_captured_time_callable(self):
        defaults = TokenBucket.__init__.__defaults__
        self.assertIsNotNone(defaults)
        for default in defaults:
            self.assertIsNone(
                default,
                "TokenBucket.__init__ must default the clock to None and resolve "
                "time.monotonic inside the constructor",
            )

    def test_signature_default_is_none(self):
        signature = inspect.signature(TokenBucket.__init__)
        clock_param = signature.parameters["clock"]
        self.assertIsNone(clock_param.default)

    def test_default_clock_still_works(self):
        bucket = TokenBucket(capacity=2, refill_per_second=1.0)
        self.assertTrue(bucket.allow())
        # The real clock advances between calls, so the refill is a tiny bit
        # above 1.0; allow for that.
        self.assertGreater(bucket.available(), 1.0)
        self.assertLess(bucket.available(), 1.01)
        self.assertIs(bucket._clock, time.monotonic)


if __name__ == "__main__":
    unittest.main()
