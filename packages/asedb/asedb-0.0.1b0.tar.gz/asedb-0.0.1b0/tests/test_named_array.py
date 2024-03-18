from __future__ import annotations

import numpy as np
import pytest
from asedb.abstract import NamedArray


class DummyNamedArray(NamedArray):
    """Test version of a NamedArray"""

    __tablename__ = "test_table"


@pytest.mark.parametrize(
    "arr",
    [
        np.array([1, 2, 3]),
        np.array([1.1, 2.2, 3.3]),
    ],
)
def test_named_array(arr, session):
    model = DummyNamedArray.from_np_array("dummy", arr)
    session.add(model)
    session.commit()

    id = model.id
    del model
    old_arr = arr.copy()
    arr *= 20

    loaded = session.query(DummyNamedArray).filter_by(id=id).scalar()
    loaded_arr = loaded.get_array()
    assert isinstance(loaded_arr, np.ndarray)
    assert np.allclose(loaded_arr, old_arr)
    assert not np.allclose(loaded_arr, arr)


def test_set_array(session):
    arr = np.array([1, 2, 3])
    model = DummyNamedArray.from_np_array("dummy", arr)

    session.add(model)
    session.commit()

    assert np.allclose(model.get_array(), arr)

    new_arr = np.array([1.2, 1.5, 200.4, 3])
    model.set_array(new_arr)
    session.add(model)
    session.commit()

    loaded_model = session.query(DummyNamedArray).first()
    loaded = loaded_model.get_array()

    assert loaded.shape != arr.shape
    assert loaded.dtype != arr.dtype
    assert loaded.shape == new_arr.shape
    assert loaded.dtype == new_arr.dtype
    assert np.allclose(loaded, new_arr)
