import unittest
import threading
import time
from typing import List

# Import the implementation from the sibling file.
from cache import ResilientCache

class DummyClock:
    """Simple clock that can be manually advanced."""
    def __init__(self, start: float = 0.0):
        self._time = start
        self._lock = threading.Lock()
    def __call__(self) -> float:
        with self._lock:
            return self._time
    def advance(self, seconds: float):
        with self._lock:
            self._time += seconds

class TestResilientCache(unittest.TestCase):
    def test_basic_get_and_ttl(self):
        clock = DummyClock()
        cache = ResilientCache[int](ttl_seconds=10, max_entries=10, clock=clock)
        # Miss – fetcher called.
        calls: List[int] = []
        def fetcher():
            calls.append(1)
            return 42
        val = cache.get_or_fetch('a', fetcher)
        self.assertEqual(val, 42)
        self.assertEqual(len(calls), 1)
        # Hit – same value, no extra call.
        val2 = cache.get_or_fetch('a', fetcher)
        self.assertEqual(val2, 42)
        self.assertEqual(len(calls), 1)
        # Advance beyond ttl – should miss again.
        clock.advance(11)
        val3 = cache.get_or_fetch('a', fetcher)
        self.assertEqual(val3, 42)
        self.assertEqual(len(calls), 2)

    def test_invalidate_and_clear(self):
        clock = DummyClock()
        cache = ResilientCache[int](ttl_seconds=10, max_entries=10, clock=clock)
        cache.get_or_fetch('x', lambda: 1)
        cache.get_or_fetch('y', lambda: 2)
        self.assertEqual(len(cache), 2)
        self.assertTrue(cache.invalidate('x'))
        self.assertFalse(cache.invalidate('nonexistent'))
        self.assertEqual(len(cache), 1)
        cache.clear()
        self.assertEqual(len(cache), 0)

    def test_lru_eviction(self):
        clock = DummyClock()
        cache = ResilientCache[int](ttl_seconds=100, max_entries=2, clock=clock)
        cache.get_or_fetch('k1', lambda: 1)
        cache.get_or_fetch('k2', lambda: 2)
        # Access k1 to make it most recent.
        cache.get_or_fetch('k1', lambda: 1)
        # Insert third key, should evict k2.
        cache.get_or_fetch('k3', lambda: 3)
        self.assertTrue('k1' in cache._entries)
        self.assertTrue('k3' in cache._entries)
        self.assertFalse('k2' in cache._entries)
        self.assertEqual(len(cache), 2)

    def test_fetcher_exception_not_cached(self):
        clock = DummyClock()
        cache = ResilientCache[int](ttl_seconds=10, max_entries=10, clock=clock)
        call_count = 0
        def bad_fetcher():
            nonlocal call_count
            call_count += 1
            raise RuntimeError('fetch failed')
        with self.assertRaises(RuntimeError):
            cache.get_or_fetch('bad', bad_fetcher)
        self.assertEqual(call_count, 1)
        # Second attempt should call fetcher again.
        with self.assertRaises(RuntimeError):
            cache.get_or_fetch('bad', bad_fetcher)
        self.assertEqual(call_count, 2)
        # Successful fetch afterwards stores the value.
        cache.get_or_fetch('bad', lambda: 99)
        self.assertEqual(cache.get_or_fetch('bad', lambda: 0), 99)

    def test_reentrancy_single_flight(self):
        clock = DummyClock()
        cache = ResilientCache[int](ttl_seconds=10, max_entries=10, clock=clock)
        fetch_calls = 0
        fetch_lock = threading.Lock()
        def fetcher():
            nonlocal fetch_calls
            with fetch_lock:
                fetch_calls += 1
            # Simulate work.
            time.sleep(0.1)
            return 123
        results = []
        def worker():
            val = cache.get_or_fetch('shared', fetcher)
            results.append(val)
        threads = [threading.Thread(target=worker) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertEqual(fetch_calls, 1)
        self.assertEqual(results, [123] * 5)

if __name__ == '__main__':
    unittest.main()
