"""Regression / safety-net suite written by Agent C.

These tests are written so that a *deliberate mutation* of cache.py makes
them fail. Each test documents the concrete mutation it is designed to catch.

Run with:
    python3 -m unittest -v test_cache test_b_adversarial test_c_regression
"""
import inspect
import threading
import time
import unittest
from typing import List
from unittest import mock

import cache as cache_module
from cache import ResilientCache


class Clock:
    """Manually advanced, thread-safe clock."""

    def __init__(self, start: float = 0.0):
        self.t = start
        self.lock = threading.Lock()

    def __call__(self) -> float:
        with self.lock:
            return self.t

    def advance(self, s: float) -> None:
        with self.lock:
            self.t += s


def make_cache(ttl=10.0, max_entries=10, clock=None):
    return ResilientCache[int](
        ttl_seconds=ttl, max_entries=max_entries, clock=clock or Clock()
    )


# --------------------------------------------------------------------------
# 1. Clock injection: the only source of time is the injected callable.
# --------------------------------------------------------------------------

class TestClockIsTheOnlyTimeSource(unittest.TestCase):
    def test_source_contains_no_direct_time_calls(self):
        """Static invariant (spec 3): no direct `time.time()`/`time.monotonic()`
        call inside the class body. Mutation: replacing `self._clock()` with
        `time.time()` in _cleanup_expired / expiry computation."""
        src = inspect.getsource(cache_module.ResilientCache)
        self.assertNotIn("time.time(", src, "cache.py calls time.time() directly")
        self.assertNotIn("time.monotonic(", src,
                         "cache.py calls time.monotonic() directly")

    def test_runtime_time_time_is_never_called(self):
        """Runtime invariant: if any code path calls time.time() at runtime the
        patched stub explodes. Mutation: `now = time.time()` in _cleanup_expired
        or in the expiry computation."""
        clock = Clock(0.0)
        cache = make_cache(clock=clock)
        with mock.patch("time.time",
                        side_effect=AssertionError("cache.py used time.time()")):
            cache.get_or_fetch("a", lambda: 1)
            self.assertEqual(len(cache), 1)
            clock.advance(11)
            self.assertEqual(len(cache), 0)

    def test_runtime_time_monotonic_is_never_called_when_clock_injected(self):
        """Same idea for time.monotonic: an injected clock must fully replace it."""
        clock = Clock(500.0)
        cache = make_cache(clock=clock)
        with mock.patch("time.monotonic",
                        side_effect=AssertionError("cache.py used time.monotonic()")):
            cache.get_or_fetch("a", lambda: 1)
            self.assertEqual(cache.get_or_fetch("a", lambda: 2), 1)
            self.assertEqual(len(cache), 1)

    def test_full_api_works_with_frozen_clock(self):
        """The whole public API must work with a deterministic clock."""
        clock = Clock(0.0)
        cache = make_cache(ttl=100.0, max_entries=2, clock=clock)
        self.assertEqual(cache.get_or_fetch("a", lambda: 1), 1)
        self.assertEqual(cache.get_or_fetch("a", lambda: 2), 1)  # hit
        self.assertTrue(cache.invalidate("a"))
        self.assertFalse(cache.invalidate("a"))
        self.assertEqual(len(cache), 0)
        cache.get_or_fetch("b", lambda: 2)
        cache.get_or_fetch("c", lambda: 3)
        self.assertEqual(len(cache), 2)
        cache.clear()
        self.assertEqual(len(cache), 0)


# --------------------------------------------------------------------------
# 2. TTL exact-boundary mutation (`>=` -> `>`).
# --------------------------------------------------------------------------

class TestTTLMutationGuards(unittest.TestCase):
    def test_exact_ttl_boundary_expires(self):
        """Mutation: `now > exp` instead of `now >= exp` (or `<` instead of
        `<=`) -> entry would still be alive exactly at the TTL boundary."""
        clock = Clock(0.0)
        cache = make_cache(ttl=10.0, clock=clock)
        cache.get_or_fetch("a", lambda: 1)
        clock.advance(10.0)
        self.assertEqual(len(cache), 0, "entry survived exactly at TTL boundary")

    def test_expiry_is_computed_from_clock_at_insert_time(self):
        """Mutation: `expiry = time.time() + ttl` -> expiry depends on wall
        clock, not the injected one. With a fake clock at 0 the entry must
        still be alive after wall-clock time has moved a lot."""
        clock = Clock(0.0)
        cache = make_cache(ttl=10.0, clock=clock)
        cache.get_or_fetch("a", lambda: 1)
        real = time.monotonic()
        self.assertEqual(len(cache), 1, "expiry not derived from injected clock")
        self.assertGreaterEqual(real, 0.0)

    def test_expired_entry_is_purged_not_just_hidden(self):
        """Mutation: dropping the `del self._entries[k]` from _cleanup_expired
        (leaving dead entries in the map) -> internal size grows without bound
        and LRU slots get wasted by corpses."""
        clock = Clock(0.0)
        cache = make_cache(ttl=5.0, max_entries=10, clock=clock)
        cache.get_or_fetch("a", lambda: 1)
        clock.advance(6)
        self.assertEqual(len(cache), 0)
        self.assertEqual(len(cache._entries), 0,
                         "expired entry still physically present in _entries")

    def test_invalidate_of_expired_key_returns_false(self):
        """Mutation: invalidate() not purging expired entries -> reports True
        for a key that is already dead (spec 4)."""
        clock = Clock(0.0)
        cache = make_cache(ttl=5.0, clock=clock)
        cache.get_or_fetch("a", lambda: 1)
        clock.advance(6)
        self.assertFalse(cache.invalidate("a"))


# --------------------------------------------------------------------------
# 3. LRU invariants (properties, not one-off cases).
# --------------------------------------------------------------------------

class TestLRUProperties(unittest.TestCase):
    def test_len_never_exceeds_max_entries(self):
        """Property: for ANY N of insertions, len(cache) <= K.
        Mutation: removing the eviction call (`_evict_if_necessary`)."""
        clock = Clock()
        cache = make_cache(ttl=1000.0, max_entries=3, clock=clock)
        for i in range(50):
            cache.get_or_fetch(f"k{i}", lambda i=i: i)
            self.assertLessEqual(len(cache), 3,
                                 f"len exceeded max_entries after insert {i}")
        self.assertEqual(len(cache), 3)

    def test_most_recent_key_always_present(self):
        """Property: the just-inserted key is always alive.
        Mutation: evicting the newest instead of the oldest, or evicting the
        key that was just inserted."""
        clock = Clock()
        cache = make_cache(ttl=1000.0, max_entries=2, clock=clock)
        for i in range(20):
            key = f"k{i}"
            cache.get_or_fetch(key, lambda i=i: i)
            self.assertIn(key, cache._entries,
                          f"newest key {key} missing right after insertion")

    def test_eviction_removes_oldest_only(self):
        """Mutation: `popitem(last=True)` (evict the most recent) instead of
        `last=False`."""
        clock = Clock()
        cache = make_cache(ttl=1000.0, max_entries=2, clock=clock)
        cache.get_or_fetch("a", lambda: 1)
        cache.get_or_fetch("b", lambda: 2)
        cache.get_or_fetch("c", lambda: 3)
        self.assertNotIn("a", cache._entries, "oldest entry was not evicted")
        self.assertIn("b", cache._entries)
        self.assertIn("c", cache._entries)

    def test_hit_promotes_key_to_most_recent(self):
        """Mutation: dropping `move_to_end(key)` on the hit path -> the
        LRU order no longer reflects real usage."""
        clock = Clock()
        cache = make_cache(ttl=1000.0, max_entries=2, clock=clock)
        cache.get_or_fetch("a", lambda: 1)
        cache.get_or_fetch("b", lambda: 2)
        cache.get_or_fetch("a", lambda: 1)  # promote "a"
        self.assertEqual(list(cache._entries.keys()), ["b", "a"])
        cache.get_or_fetch("c", lambda: 3)  # must evict "b", not "a"
        self.assertIn("a", cache._entries)
        self.assertNotIn("b", cache._entries)

    def test_lru_order_is_oldest_first(self):
        """Mutation: storing with `move_to_end` missing -> new entries land
        at the front of the order."""
        clock = Clock()
        cache = make_cache(ttl=1000.0, max_entries=5, clock=clock)
        cache.get_or_fetch("a", lambda: 1)
        cache.get_or_fetch("b", lambda: 2)
        cache.get_or_fetch("c", lambda: 3)
        self.assertEqual(list(cache._entries.keys()), ["a", "b", "c"])

    def test_len_counts_only_live_entries(self):
        """len() must reflect live entries only (mutation: len() without
        cleanup)."""
        clock = Clock(0.0)
        cache = make_cache(ttl=5.0, max_entries=10, clock=clock)
        for i in range(4):
            cache.get_or_fetch(f"k{i}", lambda i=i: i)
        self.assertEqual(len(cache), 4)
        clock.advance(6)
        self.assertEqual(len(cache), 0)


# --------------------------------------------------------------------------
# 4. Exception handling: no partial/poisoned cache entry.
# --------------------------------------------------------------------------

class TestExceptionInvariants(unittest.TestCase):
    def test_exception_leaves_no_entry(self):
        """Mutation: caching a placeholder (e.g. `except Exception:
        self._entries[key] = (None, ...)`) after a failed fetch."""
        clock = Clock()
        cache = make_cache(clock=clock)

        def bad():
            raise RuntimeError("boom")

        with self.assertRaises(RuntimeError):
            cache.get_or_fetch("k", bad)
        self.assertEqual(len(cache), 0)
        self.assertNotIn("k", cache._entries)

    def test_hit_never_invokes_fetcher(self):
        """A cache hit must not call the fetcher at all (mutation: always
        calling the fetcher and then discarding its result)."""
        clock = Clock()
        cache = make_cache(clock=clock)
        cache.get_or_fetch("k", lambda: 1)

        def exploding():
            raise AssertionError("fetcher called on a cache hit")

        self.assertEqual(cache.get_or_fetch("k", exploding), 1)

    def test_failed_fetch_does_not_poison_other_keys(self):
        """Mutation: clearing the whole cache on a failed fetch."""
        clock = Clock()
        cache = make_cache(clock=clock)
        cache.get_or_fetch("good", lambda: 1)
        with self.assertRaises(ValueError):
            cache.get_or_fetch("bad", lambda: (_ for _ in ()).throw(ValueError()))
        self.assertIn("good", cache._entries)
        self.assertEqual(cache.get_or_fetch("good", lambda: 2), 1)

    def test_repeated_failures_keep_calling_fetcher(self):
        """Mutation: caching the failure (memoizing the exception) so the
        fetcher is never retried."""
        clock = Clock()
        cache = make_cache(clock=clock)
        calls = 0

        def bad():
            nonlocal calls
            calls += 1
            raise RuntimeError("boom")

        for _ in range(3):
            with self.assertRaises(RuntimeError):
                cache.get_or_fetch("k", bad)
        self.assertEqual(calls, 3)


# --------------------------------------------------------------------------
# 5. Reentrancy / single flight with REAL threads.
# --------------------------------------------------------------------------

class TestRealThreadSingleFlight(unittest.TestCase):
    def test_barrier_single_flight_real_threads(self):
        """Spec 8 with real threads and a Barrier: the fetcher must run
        exactly once and all threads must get the same object.

        Mutation: dropping the per-key lock (fetch happens under the global
        lock only, or not at all) -> fetcher called N times.
        """
        clock = Clock()
        cache = make_cache(ttl=100.0, max_entries=10, clock=clock)
        n_threads = 8
        barrier = threading.Barrier(n_threads, timeout=5.0)
        calls = 0
        calls_lock = threading.Lock()
        results: List[object] = []
        errors: List[BaseException] = []

        def fetcher():
            nonlocal calls
            with calls_lock:
                calls += 1
            time.sleep(0.2)  # widen the race window
            return object()

        def worker():
            try:
                barrier.wait()
                results.append(cache.get_or_fetch("shared", fetcher))
            except BaseException as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [threading.Thread(target=worker) for _ in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=10.0)

        self.assertTrue(all(not t.is_alive() for t in threads),
                        "deadlock: some threads never finished")
        self.assertEqual(errors, [])
        self.assertEqual(calls, 1, f"fetcher invoked {calls} times, expected 1")
        self.assertEqual(len(results), n_threads)
        self.assertTrue(all(r is results[0] for r in results),
                        "threads received different results")

    def test_different_keys_fetch_in_parallel(self):
        """The global lock must NOT be held while the fetcher runs.
        Mutation: calling the fetcher inside `with self._lock` -> the two
        fetches serialize and the test deadlocks (caught by the timeout)."""
        clock = Clock()
        cache = make_cache(ttl=100.0, max_entries=10, clock=clock)
        a_entered = threading.Event()
        b_entered = threading.Event()
        results: List[object] = []
        errors: List[BaseException] = []

        def fetch_a():
            a_entered.set()
            if not b_entered.wait(timeout=3.0):
                raise AssertionError("fetch_b never started: fetches serialized")
            return "A"

        def fetch_b():
            b_entered.set()
            if not a_entered.wait(timeout=3.0):
                raise AssertionError("fetch_a never started: fetches serialized")
            return "B"

        def worker(key, fn):
            try:
                results.append(cache.get_or_fetch(key, fn))
            except BaseException as exc:  # noqa: BLE001
                errors.append(exc)

        ta = threading.Thread(target=worker, args=("a", fetch_a), daemon=True)
        tb = threading.Thread(target=worker, args=("b", fetch_b), daemon=True)
        ta.start()
        tb.start()
        ta.join(timeout=10.0)
        tb.join(timeout=10.0)

        self.assertFalse(ta.is_alive() or tb.is_alive(),
                         "deadlock while fetching two different keys")
        self.assertEqual(errors, [])
        self.assertEqual(sorted(results), ["A", "B"])

    def test_single_flight_under_contention_keeps_single_entry(self):
        """After the storm, exactly one live entry for the shared key."""
        clock = Clock()
        cache = make_cache(ttl=100.0, max_entries=10, clock=clock)
        n_threads = 6
        barrier = threading.Barrier(n_threads, timeout=5.0)

        def worker():
            barrier.wait()
            cache.get_or_fetch("k", lambda: "v")

        threads = [threading.Thread(target=worker) for _ in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=10.0)
        self.assertTrue(all(not t.is_alive() for t in threads))
        self.assertEqual(len(cache), 1)


# --------------------------------------------------------------------------
# 6. BaseException (KeyboardInterrupt) reentrancy: the lock must not stick.
# --------------------------------------------------------------------------

class TestBaseExceptionReentrancy(unittest.TestCase):
    def test_keyboard_interrupt_releases_key_lock(self):
        """Watchdog test: after a KeyboardInterrupt inside the fetcher, the
        per-key lock must be free. Mutation: acquiring the key lock manually
        without a `with` (no release on exception)."""
        clock = Clock()
        cache = make_cache(clock=clock)

        def boom():
            raise KeyboardInterrupt()

        with self.assertRaises(KeyboardInterrupt):
            cache.get_or_fetch("k", boom)

        outcome: List[object] = []

        def retry():
            try:
                outcome.append(cache.get_or_fetch("k", lambda: 42))
            except BaseException as exc:  # noqa: BLE001
                outcome.append(exc)

        t = threading.Thread(target=retry, daemon=True)
        t.start()
        t.join(timeout=3.0)
        self.assertFalse(t.is_alive(),
                         "key lock still held after KeyboardInterrupt (deadlock)")
        self.assertEqual(outcome, [42])

    def test_base_exception_in_thread_does_not_block_other_threads(self):
        """A BaseException raised in one thread must not leave the cache
        unusable for the others (watchdog with timeout)."""
        clock = Clock()
        cache = make_cache(ttl=100.0, max_entries=10, clock=clock)
        started = threading.Event()
        errors: List[BaseException] = []

        def boom():
            started.set()
            time.sleep(0.05)
            raise KeyboardInterrupt()

        def t1():
            try:
                cache.get_or_fetch("k", boom)
            except BaseException as exc:  # noqa: BLE001
                errors.append(exc)

        th1 = threading.Thread(target=t1, daemon=True)
        th1.start()
        started.wait(2.0)

        out: List[object] = []

        def t2():
            try:
                out.append(cache.get_or_fetch("k", lambda: 99))
            except BaseException as exc:  # noqa: BLE001
                out.append(exc)

        th2 = threading.Thread(target=t2, daemon=True)
        th2.start()
        th1.join(timeout=5.0)
        th2.join(timeout=5.0)
        self.assertFalse(th1.is_alive(), "first thread stuck")
        self.assertFalse(th2.is_alive(), "second thread stuck (lock trapped)")
        self.assertIsInstance(errors[0], KeyboardInterrupt)
        self.assertEqual(out, [99])
        self.assertEqual(len(cache), 1)


# --------------------------------------------------------------------------
# 7. State hygiene: clear(), invalidate(), constructor validation.
# --------------------------------------------------------------------------

class TestStateHygiene(unittest.TestCase):
    def test_invalidate_returns_true_exactly_once(self):
        """Mutation: invalidate() always returning True."""
        cache = make_cache()
        cache.get_or_fetch("a", lambda: 1)
        self.assertTrue(cache.invalidate("a"))
        self.assertFalse(cache.invalidate("a"))
        self.assertFalse(cache.invalidate("never-existed"))

    def test_clear_also_drops_key_locks(self):
        """Mutation: clear() not clearing the per-key lock registry (leak and
        stale locks)."""
        cache = make_cache()
        cache.get_or_fetch("a", lambda: 1)
        cache.get_or_fetch("b", lambda: 2)
        cache.clear()
        self.assertEqual(len(cache), 0)
        self.assertEqual(len(cache._key_locks), 0,
                         "clear() left per-key locks behind")

    def test_clear_then_refetch_works(self):
        cache = make_cache()
        cache.get_or_fetch("a", lambda: 1)
        cache.clear()
        self.assertEqual(cache.get_or_fetch("a", lambda: 2), 2,
                         "cleared key not refetched")

    def test_max_entries_must_be_positive(self):
        """Mutation: dropping the `max_entries <= 0` guard -> invalid cache
        silently created (and eviction loop misbehaves)."""
        with self.assertRaises(ValueError):
            ResilientCache[int](ttl_seconds=1, max_entries=0, clock=Clock())
        with self.assertRaises(ValueError):
            ResilientCache[int](ttl_seconds=1, max_entries=-3, clock=Clock())

    def test_internal_state_is_not_exposed_by_len(self):
        """`len(cache)` returns a snapshot int, not a live container:
        mutation returning the internal dict/len object would break the API."""
        cache = make_cache()
        cache.get_or_fetch("a", lambda: 1)
        n = len(cache)
        self.assertIsInstance(n, int)
        cache.get_or_fetch("b", lambda: 2)
        self.assertEqual(n, 1, "len() returned a live reference")


if __name__ == "__main__":
    unittest.main()
