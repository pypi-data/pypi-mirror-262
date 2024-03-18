from __future__ import annotations

import random

import numpy as np
import pytest
from ase.build import bulk
from ase.calculators.singlepoint import SinglePointCalculator
from asedb.atoms_model import AtomsModel, CalcArray, Calculation
from asedb.properties import ArrayProperties


@pytest.fixture
def atoms():
    atoms = bulk("Au", cubic=True) * (3, 3, 2)
    energy = random.uniform(-10, 10)
    forces = np.random.uniform(-2, 2, size=(len(atoms), 3))
    calc = SinglePointCalculator(atoms, energy=energy, forces=forces)
    atoms.calc = calc
    return atoms


def test_calculation(atoms, session):
    hits = session.query(Calculation).all()
    assert len(hits) == 0

    session.add(AtomsModel.from_atoms(atoms))
    session.commit()

    hits = session.query(CalcArray).all()
    assert len(hits) == 1

    hits = session.query(Calculation).all()
    assert len(hits) == 1

    calc_model = hits[0]
    assert len(calc_model.arrays) == 1
    assert calc_model.arrays[0].name == ArrayProperties.FORCES
    calc_model.drop_array(ArrayProperties.FORCES)
    session.add(calc_model)
    session.commit()

    del calc_model

    hits = session.query(Calculation).all()
    assert len(hits) == 1
    loaded = hits[0]
    assert len(loaded.arrays) == 0

    hits = session.query(CalcArray).all()
    assert len(hits) == 0


def test_calc_array(atoms, session):
    session.add(AtomsModel.from_atoms(atoms))
    session.commit()

    hits = session.query(CalcArray).all()
    assert len(hits) == 1
    model = hits[0]
    assert isinstance(model.array_obj, np.ndarray)

    assert "CalcArray" in repr(model)

    array = model.get_array()
    assert isinstance(array, np.ndarray)
    assert array.dtype == atoms.get_forces().dtype
    assert np.allclose(array, atoms.get_forces())
