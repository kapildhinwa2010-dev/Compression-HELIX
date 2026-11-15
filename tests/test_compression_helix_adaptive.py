"""Tests for AdaptiveHybridStore: bit-depth selection by tolerance."""

import numpy as np
import pytest

from compression_helix import AdaptiveHybridStore, HybridStore


def _smooth_matrix(rows=16, cols=32):
    t = np.linspace(0.0, 2.0 * np.pi, cols, endpoint=False)
    return np.outer(np.sin(t), np.cos(t))


def test_put_adaptive_meets_tight_tolerance_with_more_bits():
    store = AdaptiveHybridStore()
    W = _smooth_matrix()
    stats = store.put_adaptive("m1", W, tolerance=0.001)
    assert stats["relative_rmse"] <= 0.001
    assert stats["bits"] >= 8


def test_put_adaptive_uses_fewer_bits_for_loose_tolerance():
    store = AdaptiveHybridStore()
    W = _smooth_matrix()
    loose = store.put_adaptive("loose", W, tolerance=0.5)
    tight = store.put_adaptive("tight", W, tolerance=0.001)
    assert loose["bits"] <= tight["bits"]
    assert loose["ratio"] >= tight["ratio"]


def test_get_returns_stored_matrix():
    store = AdaptiveHybridStore()
    W = _smooth_matrix()
    store.put_adaptive("m1", W, tolerance=0.001)
    recon = store.get("m1")
    assert recon.shape == W.shape
    assert float(np.max(np.abs(recon - W))) < 0.01


def test_compression_report_lists_all_models():
    store = AdaptiveHybridStore()
    store.put_adaptive("a", _smooth_matrix())
    store.put_adaptive("b", _smooth_matrix())
    report = store.compression_report()
    assert sorted(report) == ["a", "b"]
    assert all("bits" in v and "ratio" in v for v in report.values())


def test_validation():
    with pytest.raises(ValueError):
        AdaptiveHybridStore(tolerance=0.0)
    store = AdaptiveHybridStore()
    with pytest.raises(ValueError):
        store.put_adaptive("", _smooth_matrix())
    with pytest.raises(ValueError):
        store.put_adaptive("bad", np.zeros(4))


def test_base_class_still_available():
    store = HybridStore()
    assert len(store) == 0
