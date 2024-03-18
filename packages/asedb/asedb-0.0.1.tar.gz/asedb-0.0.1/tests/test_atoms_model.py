from __future__ import annotations

import itertools
import random

import ase
import numpy as np
import pytest
from ase.build import bulk, fcc111
from ase.calculators.singlepoint import SinglePointCalculator
from asedb import AtomsModel, Element
from asedb.atoms_model import Calculation, _decode_pbc, _encode_pbc


def make_atoms_list():
    return [
        ase.Atoms("H2", positions=[[0, 0, 0], [0, 0, 0.7]]),
        bulk("NaCl", crystalstructure="rocksalt", a=4.0).repeat((3, 2, 2)),
        fcc111("Al", size=(2, 2, 3), vacuum=10.0),
    ]


def cmp_atoms(atoms1: ase.Atoms, atoms2: ase.Atoms) -> None:
    assert atoms2 is not atoms1
    assert isinstance(atoms1, ase.Atoms)
    assert isinstance(atoms2, ase.Atoms)
    assert len(atoms2) == len(atoms1)
    assert np.equal(atoms1.numbers, atoms2.numbers).all()
    assert (atoms2.symbols == atoms1.symbols).all()
    assert np.allclose(atoms1.get_positions(), atoms2.positions)
    assert (atoms1.pbc == atoms2.pbc).all()
    assert (atoms1.get_tags() == atoms2.get_tags()).all()
    assert np.allclose(atoms1.cell, atoms2.cell)
    assert np.allclose(atoms1.get_masses(), atoms2.get_masses())
    assert np.allclose(atoms1.get_momenta(), atoms2.get_momenta())

    assert np.allclose(atoms1.get_masses(), atoms2.get_masses())
    assert np.allclose(atoms1.get_initial_charges(), atoms2.get_initial_charges())
    assert np.allclose(atoms1.get_initial_magnetic_moments(), atoms2.get_initial_magnetic_moments())


@pytest.mark.parametrize("atoms", make_atoms_list())
def test_atoms_model(atoms: ase.Atoms, session):
    model = AtomsModel.from_atoms(atoms)
    assert "AtomsModel" in repr(model)
    session.add(model)
    session.commit()

    id = model.id
    assert isinstance(id, int)

    loaded = session.query(AtomsModel).filter_by(id=id).scalar()
    assert isinstance(loaded, AtomsModel)
    loaded_atoms = loaded.to_atoms()
    cmp_atoms(atoms, loaded_atoms)


def test_multiple_atoms(session):
    atoms_list = make_atoms_list()
    for atoms in atoms_list:
        model = AtomsModel.from_atoms(atoms)
        session.add(model)
    session.commit()

    loaded_all = session.query(AtomsModel).all()
    assert len(loaded_all) == len(atoms_list)
    for ii, loaded in enumerate(loaded_all):
        cmp_atoms(loaded.to_atoms(), atoms_list[ii])


def test_atoms_with_calc(session):
    atoms_list = make_atoms_list()

    for expect_id, atoms in enumerate(atoms_list, start=1):
        energy = random.uniform(-10, 10)
        forces = np.random.uniform(-3, 3, size=(len(atoms), 3))
        stress = np.random.uniform(-11, 11, size=(6,))
        magmoms = np.random.uniform(0, 5, size=len(atoms))
        calc = SinglePointCalculator(
            atoms, energy=energy, forces=forces, stress=stress, magmoms=magmoms
        )
        atoms.calc = calc

        session.add(AtomsModel.from_atoms(atoms))
        session.commit()

        del calc
        del atoms

        loaded = session.query(AtomsModel).filter_by(id=expect_id).scalar()
        loaded_atoms = loaded.to_atoms()

        assert pytest.approx(loaded_atoms.get_potential_energy()) == energy
        assert np.allclose(loaded_atoms.get_forces(), forces)
        assert loaded.calculation.fmax == pytest.approx(np.linalg.norm(forces, axis=1).max())
    all_loads = session.query(AtomsModel).all()
    assert len(all_loads) == len(atoms_list)
    all_calcs = session.query(Calculation).all()
    assert len(all_calcs) == len(atoms_list)


def test_query_atoms(session):
    atoms_list = make_atoms_list()
    for atoms in atoms_list:
        session.add(AtomsModel.from_atoms(atoms))
    session.commit()

    found = (
        session.query(AtomsModel)
        .join(Element)
        .where((Element.symbol == "H") & (Element.count == 2))
        .all()
    )
    assert len(found) == 1
    cmp_atoms(atoms_list[0], found[0].to_atoms())

    found = session.query(AtomsModel).join(Element).where(Element.count > 2).all()
    assert len(found) == len(atoms_list) - 1


def test_encode_decode_pbc():
    seen = set()
    for pbc in itertools.product([True, False], [True, False], [True, False]):
        pbc_np = np.array(pbc, dtype=bool)
        val = _encode_pbc(pbc_np)
        assert val not in seen
        seen.add(val)
        assert (pbc_np == _decode_pbc(val)).all()
    assert len(seen) == 2**3


def test_doc_example(session):
    atoms = ase.Atoms("H2O", positions=[[0, 0, 0], [0, 0, 1], [1, 0, 0]])
    atoms_model = AtomsModel.from_atoms(atoms)
    session.add(atoms_model)
    session.commit()

    atoms = atoms_model.to_atoms()
    atoms += ase.Atom("O", position=[1.2, 0, 0])
    atoms_model.set_atoms(atoms)
    session.add(atoms_model)
    session.commit()

    loaded_models = session.query(AtomsModel).all()
    assert len(loaded_models) == 1
    loaded = loaded_models[0]
    elem_counts = loaded.get_element_counts()
    assert len(elem_counts) == 2
    assert elem_counts["H"] == 2
    assert elem_counts["O"] == 2


@pytest.mark.parametrize("atoms", make_atoms_list())
def test_atoms_model_arrays(atoms: ase.Atoms, session):
    atoms_orig = atoms.copy()
    for _ in range(3):
        atoms = atoms_orig.copy()
        numbers = np.random.randint(1, 90, len(atoms))
        atoms.numbers = numbers

        tags = np.random.randint(0, 11, size=len(atoms))
        atoms.set_tags(tags)

        charges = np.random.uniform(-2, 2, size=len(atoms))
        atoms.set_initial_charges(charges)

        ini_magmoms = np.random.uniform(-3, 3, size=len(atoms))
        atoms.set_initial_magnetic_moments(ini_magmoms)

        masses = np.random.uniform(1, 20, size=len(atoms))
        atoms.set_masses(masses)

        momenta = np.random.uniform(-10, 10, size=(len(atoms), 3))
        atoms.set_momenta(momenta)

        model = AtomsModel.from_atoms(atoms)
        session.add(model)
        session.commit()

        id = model.id
        assert isinstance(id, int)
        del model

        loaded_model = session.query(AtomsModel).filter_by(id=id).scalar()
        assert isinstance(loaded_model, AtomsModel)
        loaded = loaded_model.to_atoms()

        assert np.allclose(loaded.get_tags(), tags)
        assert np.allclose(loaded.get_initial_charges(), charges)
        assert np.allclose(loaded.get_initial_magnetic_moments(), ini_magmoms)
        assert np.allclose(loaded.get_momenta(), momenta)
        assert np.allclose(loaded.get_masses(), masses)
        assert np.equal(loaded.numbers, numbers).all()

        cmp_atoms(atoms, loaded)
