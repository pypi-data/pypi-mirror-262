from __future__ import annotations

import numpy as np
import pytest
from asedb.abstract import _deserialize_array, _serialize_array


@pytest.mark.parametrize(
    "arr",
    [
        np.array([1, 2, 3], dtype=int),
        np.array(["Hello", "World"]),
        np.arange(12).reshape(6, 2).astype(np.float32),
        np.array(["a", "B", "c", "æ", "Åøæå"], dtype=str),
        np.array([1.23, 4.321, 3.1415], dtype=np.float32),
        np.array([1.23, 4.32100001, 3.14159], dtype=np.float64),
        np.array([1.23, 2.0 + 4.12j, 5.11j], dtype=np.complex_),
    ],
)
def test_serialize_array(arr: np.ndarray):
    serialized = _serialize_array(arr)
    assert isinstance(serialized, bytes)

    loaded = _deserialize_array(serialized)
    assert loaded.shape == arr.shape
    assert loaded.dtype == arr.dtype
    assert np.equal(loaded, arr).all()


@pytest.mark.parametrize(
    "shape",
    [
        (10,),
        (15, 15),
        (1, 19),
        (9, 4, 3, 1, 8, 11),
    ],
)
def test_random_arrays(shape: tuple[int, ...]):
    arr = np.random.uniform(-10, 10, size=shape)
    serialized = _serialize_array(arr)
    loaded = _deserialize_array(serialized)

    assert loaded.shape == arr.shape
    assert loaded.dtype == arr.dtype
    assert np.equal(loaded, arr).all()


def test_no_arbitrary_objects():
    arr = np.array([object()])
    assert arr.dtype == np.dtype("object")
    with pytest.raises(ValueError):
        _serialize_array(arr)
