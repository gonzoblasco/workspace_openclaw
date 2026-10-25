import unittest
from typing import Callable

from ratelimit import TokenBucket


class FakeClock:
    def __init__(self, start: float = 0.0):
        self.time = start

    def __call__(self) -> float:
        return self.time

    def advance(self, delta: float) -> None:
        self.time += delta

    def set(self, value: float) -> None:
        self.time = value


class TestTokenBucket(unittest.TestCase):
    def test_initial_full_and_basic_allow(self):
        clock = FakeClock()
        bucket = TokenBucket(capacity=3, refill_per_second=0, clock=clock)
        # Initially full
        self.assertEqual(bucket.available(), 3)
        # Three successful allows
        for _ in range(3):
            self.assertTrue(bucket.allow())
        # Fourth should fail
        self.assertFalse(bucket.allow())
        # No tokens consumed on failed attempt
        self.assertEqual(bucket.available(), 0)

    def test_refill_per_second(self):
        clock = FakeClock()
        bucket = TokenBucket(capacity=5, refill_per_second=1.0, clock=clock)
        # Consume everything
        bucket.allow(5)
        self.assertEqual(bucket.available(), 0)
        # Advance 1 second -> 1 token
        clock.advance(1.0)
        self.assertAlmostEqual(bucket.available(), 1.0)
        # Consume the token
        self.assertTrue(bucket.allow())
        self.assertEqual(bucket.available(), 0)

    def test_fractional_refill(self):
        clock = FakeClock()
        bucket = TokenBucket(capacity=2, refill_per_second=0.5, clock=clock)
        # Consume one token
        bucket.allow()
        self.assertEqual(bucket.available(), 1)
        # Advance half a second -> 0.25 token (0.5 * 0.5)
        clock.advance(0.5)
        self.assertAlmostEqual(bucket.available(), 1 + 0.25)
        # Allow with cost 0.5 should succeed because we have >=0.5
        self.assertTrue(bucket.allow(0.5))
        # Tokens left should be original -0.5 + 0.25 = 0.75
        self.assertAlmostEqual(bucket.available(), 0.75)

    def test_invalid_cost(self):
        clock = FakeClock()
        bucket = TokenBucket(capacity=1, refill_per_second=1, clock=clock)
        with self.assertRaises(ValueError):
            bucket.allow(0)
        with self.assertRaises(ValueError):
            bucket.allow(-1)

    def test_cost_exceeds_capacity(self):
        clock = FakeClock()
        bucket = TokenBucket(capacity=2, refill_per_second=1, clock=clock)
        self.assertFalse(bucket.allow(5))
        # Ensure state unchanged (still full)
        self.assertEqual(bucket.available(), 2)

    def test_clock_goes_backward(self):
        clock = FakeClock()
        bucket = TokenBucket(capacity=3, refill_per_second=1, clock=clock)
        # Consume two tokens
        bucket.allow()
        bucket.allow()
        self.assertEqual(bucket.available(), 1)
        # Advance time 1 second -> refill is proportional to the rate:
        # 1 remaining token + 1.0s * 1 token/s = 2 tokens (NOT a full
        # recharge: the spec refills by rate, it does not refill completely).
        clock.advance(1.0)
        self.assertEqual(bucket.available(), 2.0)
        # Move clock backwards 0.5 seconds
        clock.advance(-0.5)
        # No extra tokens should be created; bucket stays at 2 tokens
        self.assertEqual(bucket.available(), 2.0)
        # Advance forward 0.5 seconds: the interval was already credited
        # before the rewind, so no new tokens appear.
        clock.advance(0.5)
        self.assertEqual(bucket.available(), 2.0)

    def test_reset(self):
        clock = FakeClock()
        bucket = TokenBucket(capacity=4, refill_per_second=1, clock=clock)
        bucket.allow(2)
        self.assertEqual(bucket.available(), 2)
        clock.advance(0.5)
        bucket.reset()
        # After reset we should be full regardless of prior time advancement
        self.assertEqual(bucket.available(), 4)
        # Ensure internal timestamp was refreshed (advance 1s gives exactly 1 token)
        clock.advance(1.0)
        self.assertAlmostEqual(bucket.available(), 4)  # still full, no overflow
        # Consume one token and check refill works after reset timestamp
        self.assertTrue(bucket.allow())
        self.assertEqual(bucket.available(), 3)
        clock.advance(1.0)
        self.assertAlmostEqual(bucket.available(), 4)  # refilled to capacity


if __name__ == "__main__":
    unittest.main()
