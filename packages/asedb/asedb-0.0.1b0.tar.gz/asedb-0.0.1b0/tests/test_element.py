from __future__ import annotations

import pytest
from ase.build import bulk
from asedb import AtomsModel, Element


@pytest.fixture
def li_atoms():
    return bulk("Li") * (2, 2, 2)


def test_element(li_atoms, session):
    atoms = li_atoms
    hits = session.query(Element).all()
    assert len(hits) == 0

    model = AtomsModel.from_atoms(atoms)
    session.add(model)
    session.commit()

    hits = session.query(Element).all()
    assert len(hits) == 1
    assert hits[0].symbol == "Li"
    assert hits[0].count == len(atoms)
    first_id = hits[0].id

    atoms.symbols = "Na"

    # Change the atoms, verify we also update the Element object automatically
    model.set_atoms(atoms)
    session.add(model)
    session.commit()

    hits = session.query(Element).all()
    assert len(hits) == 1
    assert hits[0].symbol == "Na"
    assert hits[0].count == len(atoms)
    assert hits[0].id == first_id + 1
