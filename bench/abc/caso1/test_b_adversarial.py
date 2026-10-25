"""Adversarial review suite written by Agent B.

Each test targets one specific claim of spec1.md. Run with:
    python3 -m unittest -v test_b_adversarial
"""
import threading
import time
import unittest
from typing import List

from cache import ResilientCache


class Clock:
    def __init__(self, start: float = 0.0):
        self.t = start
        self.lock = threading.Lock()

    def __call__(self) -> float:
        with self.lock:
            return self.t

    def advance(self, s: float) -> None:
        with self.lock:
            self.t += s


class TestSingleFlight(unittest.TestCase):
    def test_concurrent_miss_calls_fetcher_once(self):
        """Spec 8: N threads on the same missing key -> fetcher called once."""
        clock = Clock()
        cache = ResilientCache[int](ttl_seconds=10, max_entries=10, clock=clock)
        calls = 0
        calls_lock = threading.Lock()

        def fetcher() -> int:
            nonlocal calls
            with calls_lock:
                calls += 1
            time.sleep(0.15)
            return 7

        results: List[int] = []
        errors: List[BaseException] = []
        barrier = threading.Barrier(8)

        def worker() -> None:
            barrier.wait()
            try:
                results.append(cache.get_or_fetch("k", fetcher))
            except BaseException as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [threading.Thread(target=worker) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(errors, [])
        self.assertEqual(results, [7] * 8)
        self.assertEqual(calls, 1, f"fetcher invoked {calls} times, expected 1")

    def test_no_lock_trapped_after_fetcher_exception(self):
        """Spec 9: an exception in fetcher must not leave the key lock stuck."""
        clock = Clock()
        cache = ResilientCache[int](ttl_seconds=10, max_entries=10, clock=clock)

        def bad() -> int:
            raise RuntimeError("boom")

        with self.assertRaises(RuntimeError):
            cache.get_or_fetch("k", bad)

        # If a key lock stayed held, this hangs forever. Run it with a watchdog.
        outcome: List[object] = []

        def retry() -> None:
            try:
                outcome.append(cache.get_or_fetch("k", lambda: 5))
            except BaseException as exc:  # noqa: BLE001
                outcome.append(exc)

        t = threading.Thread(target=retry, daemon=True)
        t.start()
        t.join(timeout=2.0)
        self.assertFalse(t.is_alive(), "second call blocked: key lock still held")
        self.assertEqual(outcome, [5])

    def test_concurrent_threads_after_exception(self):
        """An exception must not poison the key for other waiting threads."""
        clock = Clock()
        cache = ResilientCache[int](ttl_seconds=10, max_entries=10, clock=clock)
        started = threading.Event()

        def slow_bad() -> int:
            started.set()
            time.sleep(0.1)
            raise ValueError("nope")

        first: List[BaseException] = []

        def t1() -> None:
            try:
                cache.get_or_fetch("k", slow_bad)
            except BaseException as exc:  # noqa: BLE001
                first.append(exc)

        th1 = threading.Thread(target=t1, daemon=True)
        th1.start()
        started.wait(1.0)
        retry_calls = 0

        def good() -> int:
            nonlocal retry_calls
            retry_calls += 1
            return 11

        th2_res: List[object] = []

        def t2() -> None:
            try:
                th2_res.append(cache.get_or_fetch("k", good))
            except BaseException as exc:  # noqa: BLE001
                th2_res.append(exc)

        th2 = threading.Thread(target=t2, daemon=True)
        th2.start()
        th1.join(timeout=2.0)
        th2.join(timeout=2.0)
        self.assertFalse(th1.is_alive(), "first thread stuck")
        self.assertFalse(th2.is_alive(), "second thread stuck")
        self.assertIsInstance(first[0], ValueError)


class TestFetcherException(unittest.TestCase):
    def test_keyboard_interrupt_not_cached_and_lock_released(self):
        """Spec 9: fetcher raising KeyboardInterrupt (BaseException) must not
        leave the key cached nor the key lock held."""
        clock = Clock()
        cache = ResilientCache[int](ttl_seconds=10, max_entries=10, clock=clock)

        def boom() -> int:
            raise KeyboardInterrupt()

        with self.assertRaises(KeyboardInterrupt):
            cache.get_or_fetch("k", boom)

        self.assertEqual(len(cache), 0, "entry cached after KeyboardInterrupt")

        outcome: List[object] = []

        def retry() -> None:
            try:
                outcome.append(cache.get_or_fetch("k", lambda: 3))
            except BaseException as exc:  # noqa: BLE001
                outcome.append(exc)

        t = threading.Thread(target=retry, daemon=True)
        t.start()
        t.join(timeout=2.0)
        self.assertFalse(t.is_alive(), "key lock still held after KeyboardInterrupt")
        self.assertEqual(outcome, [3])


class TestLRU(unittest.TestCase):
    def test_lru_insert_order_evicts_oldest(self):
        """Spec 7: max_entries=2, insert 3 fresh keys, oldest must be evicted."""
        clock = Clock()
        cache = ResilientCache[int](ttl_seconds=100, max_entries=2, clock=clock)
        cache.get_or_fetch("a", lambda: 1)
        cache.get_or_fetch("b", lambda: 2)
        cache.get_or_fetch("c", lambda: 3)
        self.assertNotIn("a", cache._entries, "oldest entry 'a' was not evicted")
        self.assertIn("b", cache._entries)
        self.assertIn("c", cache._entries)
        self.assertEqual(len(cache), 2)

    def test_lru_eviction_does_not_change_existing_key_order(self):
        """Eviction must remove the LRU entry only; order must otherwise stay
        oldest-first so successive inserts keep evicting the actual LRU."""
        clock = Clock()
        cache = ResilientCache[int](ttl_seconds=100, max_entries=2, clock=clock)
        cache.get_or_fetch("a", lambda: 1)
        cache.get_or_fetch("b", lambda: 2)
        keys_in_order = list(cache._entries.keys())
        self.assertEqual(keys_in_order, ["a", "b"])

    def test_lru_hit_promotes_key(self):
        clock = Clock()
        cache = ResilientCache[int](ttl_seconds=100, max_entries=2, clock=clock)
        cache.get_or_fetch("a", lambda: 1)
        cache.get_or_fetch("b", lambda: 2)
        cache.get_or_fetch("a", lambda: 1)  # promote a
        cache.get_or_fetch("c", lambda: 3)  # evict b
        self.assertIn("a", cache._entries)
        self.assertNotIn("b", cache._entries)

    def test_max_entries_one(self):
        clock = Clock()
        cache = ResilientCache[int](ttl_seconds=100, max_entries=1, clock=clock)
        cache.get_or_fetch("a", lambda: 1)
        cache.get_or_fetch("b", lambda: 2)
        self.assertEqual(len(cache), 1)
        self.assertNotIn("a", cache._entries)
        self.assertIn("b", cache._entries)


class TestTTLBoundary(unittest.TestCase):
    def test_ttl_exact_boundary_is_expired(self):
        """Exactly ttl elapsed: spec says "vencida" -> entry considered expired."""
        clock = Clock(0.0)
        cache = ResilientCache[int](ttl_seconds=10, max_entries=10, clock=clock)
        cache.get_or_fetch("a", lambda: 1)
        clock.advance(10.0)
        self.assertEqual(len(cache), 0, "entry alive exactly at TTL boundary")

    def test_ttl_just_before_boundary_is_alive(self):
        clock = Clock(0.0)
        cache = ResilientCache[int](ttl_seconds=10, max_entries=10, clock=clock)
        cache.get_or_fetch("a", lambda: 1)
        clock.advance(9.999)
        self.assertEqual(len(cache), 1)
        self.assertEqual(cache.get_or_fetch("a", lambda: 2), 1)

    def test_expired_key_does_not_count_in_len(self):
        clock = Clock(0.0)
        cache = ResilientCache[int](ttl_seconds=5, max_entries=10, clock=clock)
        cache.get_or_fetch("a", lambda: 1)
        cache.get_or_fetch("b", lambda: 2)
        clock.advance(6)
        self.assertEqual(len(cache), 0)

    def test_expired_entry_cannot_evict_live_one(self):
        """Expired entries must not occupy LRU slots and evict live entries."""
        clock = Clock(0.0)
        cache = ResilientCache[int](ttl_seconds=10, max_entries=2, clock=clock)
        cache.get_or_fetch("a", lambda: 1)
        clock.advance(11)  # "a" expired
        cache.get_or_fetch("b", lambda: 2)
        cache.get_or_fetch("c", lambda: 3)
        self.assertIn("b", cache._entries)
        self.assertIn("c", cache._entries)
        self.assertNotIn("a", cache._entries)


class TestInvalidateClear(unittest.TestCase):
    def test_invalidate_missing_returns_false(self):
        cache = ResilientCache[int](ttl_seconds=10, max_entries=10, clock=Clock())
        self.assertFalse(cache.invalidate("nope"))

    def test_invalidate_expired_key(self):
        clock = Clock()
        cache = ResilientCache[int](ttl_seconds=5, max_entries=10, clock=clock)
        cache.get_or_fetch("a", lambda: 1)
        clock.advance(6)
        self.assertFalse(cache.invalidate("a"), "expired entry reported as existing")

    def test_clear_empties(self):
        clock = Clock()
        cache = ResilientCache[int](ttl_seconds=10, max_entries=10, clock=clock)
        cache.get_or_fetch("a", lambda: 1)
        cache.get_or_fetch("b", lambda: 2)
        cache.clear()
        self.assertEqual(len(cache), 0)
        self.assertFalse(cache.invalidate("a"))


class TestClockInjection(unittest.TestCase):
    def test_clock_is_the_only_time_source(self):
        """Spec 3: logic must only read time via self._clock()."""
        clock = Clock(1000.0)
        cache = ResilientCache[int](ttl_seconds=10, max_entries=10, clock=clock)
        cache.get_or_fetch("a", lambda: 1)
        # With a fake clock at 1000, nothing can have expired regardless of wall.
        self.assertEqual(len(cache), 1)
        clock.advance(11)
        self.assertEqual(len(cache), 0)


if __name__ == "__main__":
    unittest.main()
