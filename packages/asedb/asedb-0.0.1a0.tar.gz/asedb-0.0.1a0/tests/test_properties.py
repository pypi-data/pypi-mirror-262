from __future__ import annotations

import pytest
from asedb.properties import ArrayProperties, ValueProperties


@pytest.mark.parametrize("prop", [ValueProperties, ArrayProperties])
def test_properties(prop):
    cnt = 0
    for item in prop.iter():
        assert isinstance(item, str)
        cnt += 1
    assert cnt == len(prop)


def test_equality():
    assert ArrayProperties.FORCES == "forces"
    assert ArrayProperties.MAGMOMS != "forces"

    assert ValueProperties.ENERGY == "energy"
    assert ValueProperties.ENERGY != "free_energy"
    assert ValueProperties.FREE_ENERGY == "free_energy"
