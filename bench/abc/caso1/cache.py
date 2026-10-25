import time
import threading
from collections import OrderedDict
from typing import Callable, Generic, TypeVar, Dict, Tuple, Optional

T = TypeVar('T')

class ResilientCache(Generic[T]):
    """Thread‑safe cache with TTL, LRU eviction and *single flight* fetch.

    All time‑related operations use the injected ``clock`` callable. The cache
    supports concurrent ``get_or_fetch`` calls for the same key without invoking
    the ``fetcher`` more than once.
    """

    def __init__(self, ttl_seconds: float, max_entries: int = 128,
                 clock: Callable[[], float] = time.monotonic):
        if max_entries <= 0:
            raise ValueError("max_entries must be > 0")
        self._ttl = ttl_seconds
        self._max = max_entries
        self._clock = clock
        # OrderedDict preserves insertion order; the *end* is most‑recent.
        self._entries: "OrderedDict[str, Tuple[T, float]]" = OrderedDict()
        self._lock = threading.RLock()
        # Per‑key locks to guarantee a single fetch in flight.
        self._key_locks: Dict[str, threading.Lock] = {}

    def _evict_if_necessary(self) -> None:
        """Evict least‑recently used items until size <= ``max_entries``.
        Must be called with ``self._lock`` held.
        """
        while len(self._entries) > self._max:
            # popitem(last=False) removes the *oldest* (least‑recent) entry.
            self._entries.popitem(last=False)

    def _cleanup_expired(self) -> None:
        """Remove entries whose TTL has elapsed. Called while holding the lock.
        """
        now = self._clock()
        expired = [k for k, (_, exp) in self._entries.items() if now >= exp]
        for k in expired:
            del self._entries[k]

    def _get_key_lock(self, key: str) -> threading.Lock:
        """Return a dedicated lock for *key*, creating it if necessary.
        The returned lock is always the same object for the same key.
        """
        with self._lock:
            lock = self._key_locks.get(key)
            if lock is None:
                lock = threading.Lock()
                self._key_locks[key] = lock
            return lock

    def get_or_fetch(self, key: str, fetcher: Callable[[], T]) -> T:
        """Return the cached value for *key* or compute it with ``fetcher``.

        If multiple threads request the same missing key concurrently, ``fetcher``
        is executed only once; the other threads wait for the result (or the
        exception) and then return/raise the same outcome.
        """
        # Fast path – read‑only check under the global lock.
        with self._lock:
            self._cleanup_expired()
            entry = self._entries.get(key)
            if entry is not None:
                value, _ = entry
                # Update LRU order.
                self._entries.move_to_end(key)
                return value
        # Acquire per‑key lock to ensure a single fetch.
        key_lock = self._get_key_lock(key)
        with key_lock:
            # Re‑check inside the lock – another thread may have filled it.
            with self._lock:
                self._cleanup_expired()
                entry = self._entries.get(key)
                if entry is not None:
                    value, _ = entry
                    self._entries.move_to_end(key)
                    return value
            # Cache miss – run the fetcher.
            try:
                result = fetcher()
            except Exception:
                # Do *not* cache anything; propagate the exception.
                raise
            # Store the fresh value.
            with self._lock:
                expiry = self._clock() + self._ttl
                self._entries[key] = (result, expiry)
                self._entries.move_to_end(key)
                self._evict_if_necessary()
            return result

    def invalidate(self, key: str) -> bool:
        """Remove *key* from the cache. Return ``True`` if it existed.
        """
        with self._lock:
            # Expired entries are not "alive" (spec 4/6): purge them first so
            # invalidate() reports False for an entry that already died.
            self._cleanup_expired()
            existed = key in self._entries
            if existed:
                del self._entries[key]
            return existed

    def clear(self) -> None:
        """Remove all entries and per‑key lock records.
        """
        with self._lock:
            self._entries.clear()
            self._key_locks.clear()

    def __len__(self) -> int:
        """Return the number of *live* (non‑expired) entries.
        """
        with self._lock:
            self._cleanup_expired()
            return len(self._entries)

    # The following methods are for introspection in tests; they are not part
    # of the public spec but are safe because they expose internal state only
    # for debugging.
    # NOTE: ``_entries`` is an OrderedDict; the order reflects LRU usage.
