from __future__ import annotations

import warnings

import chardet
from chardet._utils import (
    LowConfidenceWarning,
    _warn_low_confidence,
)


def test_low_confidence_warning_is_user_warning():
    assert issubclass(LowConfidenceWarning, UserWarning)
    assert LowConfidenceWarning.__name__ == "LowConfidenceWarning"


def test_warn_low_confidence_below_threshold():
    result = {"encoding": "utf-8", "confidence": 0.1, "language": None}
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        _warn_low_confidence(result, 0.5)
        assert len(w) == 1
        assert issubclass(w[0].category, LowConfidenceWarning)
        assert "Low confidence" in str(w[0].message)


def test_warn_low_confidence_above_threshold():
    result = {"encoding": "utf-8", "confidence": 0.9, "language": None}
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        _warn_low_confidence(result, 0.5)
        assert len(w) == 0


def test_detect_emits_low_confidence_warning():
    data = bytes(range(0x80, 0x100)) * 10
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = chardet.detect(data, low_confidence_threshold=0.99)
        low_warnings = [x for x in w if issubclass(x.category, LowConfidenceWarning)]
        assert len(low_warnings) >= 1
        assert result is not None


def test_detect_no_warning_for_high_confidence():
    data = b"Hello world, this is clearly ASCII text. " * 5
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        chardet.detect(data, low_confidence_threshold=0.5)
        low_warnings = [x for x in w if issubclass(x.category, LowConfidenceWarning)]
        assert len(low_warnings) == 0


def test_low_confidence_threshold_exported():
    assert hasattr(chardet, "LOW_CONFIDENCE_THRESHOLD")
    assert isinstance(chardet.LOW_CONFIDENCE_THRESHOLD, float)


def test_low_confidence_warning_exported():
    assert hasattr(chardet, "LowConfidenceWarning")
