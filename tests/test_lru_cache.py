import pytest
from lru_cache import LRUCache


class TestBasicOperations:

    def test_get_missing_key_returns_minus_one(self):
        cache = LRUCache(2)
        assert cache.get(1) == -1

    def test_put_and_get(self):
        cache = LRUCache(2)
        cache.put(1, 10)
        assert cache.get(1) == 10

    def test_put_updates_existing_key(self):
        cache = LRUCache(2)
        cache.put(1, 10)
        cache.put(1, 99)
        assert cache.get(1) == 99
        assert len(cache) == 1   # No duplicate entries

    def test_multiple_keys(self):
        cache = LRUCache(3)
        cache.put(1, 10)
        cache.put(2, 20)
        cache.put(3, 30)
        assert cache.get(1) == 10
        assert cache.get(2) == 20
        assert cache.get(3) == 30


class TestEviction:

    def test_lru_evicted_on_overflow(self):
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        cache.put(3, 3)        # 1 should be evicted (LRU)
        assert cache.get(1) == -1
        assert cache.get(2) == 2
        assert cache.get(3) == 3

    def test_get_refreshes_usage_order(self):
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        cache.get(1)           # 1 is now MRU; 2 becomes LRU
        cache.put(3, 3)        # 2 should be evicted
        assert cache.get(2) == -1
        assert cache.get(1) == 1
        assert cache.get(3) == 3

    def test_put_update_refreshes_usage_order(self):
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        cache.put(1, 100)      # 1 updated → 1 is MRU, 2 is LRU
        cache.put(3, 3)        # 2 should be evicted
        assert cache.get(2) == -1
        assert cache.get(1) == 100
        assert cache.get(3) == 3

    def test_eviction_chain(self):
        cache = LRUCache(3)
        for i in range(1, 6):  # puts 1..5, each time evicting oldest
            cache.put(i, i * 10)
        # After 5 puts into capacity-3: survivors should be 3, 4, 5
        assert cache.get(1) == -1
        assert cache.get(2) == -1
        assert cache.get(3) == 30
        assert cache.get(4) == 40
        assert cache.get(5) == 50


class TestCapacityBoundaries:

    def test_capacity_one(self):
        cache = LRUCache(1)
        cache.put(1, 1)
        assert cache.get(1) == 1
        cache.put(2, 2)        # 1 evicted immediately
        assert cache.get(1) == -1
        assert cache.get(2) == 2

    def test_capacity_one_repeated_updates(self):
        cache = LRUCache(1)
        cache.put(1, 1)
        cache.put(1, 2)
        cache.put(1, 3)
        assert len(cache) == 1
        assert cache.get(1) == 3

    def test_size_never_exceeds_capacity(self):
        cap   = 5
        cache = LRUCache(cap)
        for i in range(20):
            cache.put(i, i)
            assert len(cache) <= cap

    def test_invalid_capacity_raises(self):
        with pytest.raises(ValueError):
            LRUCache(0)
        with pytest.raises(ValueError):
            LRUCache(-3)


class TestRepr:

    def test_repr_shows_lru_to_mru_order(self):
        cache = LRUCache(3)
        cache.put(1, 1)
        cache.put(2, 2)
        cache.put(3, 3)
        r = repr(cache)
        # Order should be LRU (1) → MRU (3)
        assert r.index("1:1") < r.index("2:2") < r.index("3:3")

    def test_repr_after_access_reorders(self):
        cache = LRUCache(3)
        cache.put(1, 1)
        cache.put(2, 2)
        cache.put(3, 3)
        cache.get(1)           # 1 moves to MRU
        r = repr(cache)
        assert r.index("2:2") < r.index("3:3") < r.index("1:1")


class TestLeetCodeExample:

    def test_leetcode_example(self):
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        assert cache.get(1) == 1    # returns 1
        cache.put(3, 3)             # evicts key 2
        assert cache.get(2) == -1   # returns -1 (not found)
        cache.put(4, 4)             # evicts key 1
        assert cache.get(1) == -1   # returns -1 (not found)
        assert cache.get(3) == 3    # returns 3
        assert cache.get(4) == 4    # returns 4