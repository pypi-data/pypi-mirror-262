from __future__ import annotations

import ase
import numpy as np
from ase.build import bulk, fcc111
from asedb.atoms_model import AtomsModel
from asedb.trajectory_model import Trajectory


def make_atoms_list():
    return [
        ase.Atoms("H2", positions=[[0, 0, 0], [0, 0, 0.7]]),
        bulk("NaCl", crystalstructure="rocksalt", a=4.0).repeat((3, 2, 2)),
        fcc111("Al", size=(2, 2, 3), vacuum=10.0),
    ]


def test_trajectory(session):
    traj = Trajectory()
    expect = make_atoms_list()
    for atoms in expect:
        traj.add_atoms(atoms)
    session.add(traj)
    session.commit()

    loaded: Trajectory = session.query(Trajectory).filter_by(id=1).scalar()

    assert len(loaded.atoms_list) == 3
    atoms_list = loaded.to_atoms_list()
    assert len(atoms_list) == 3
    for ii, atoms in enumerate(atoms_list):
        assert isinstance(atoms, ase.Atoms)
        exp = expect[ii]
        assert atoms is not exp
        assert len(atoms) == len(exp)
        assert (atoms.symbols == exp.symbols).all()
        assert np.allclose(atoms.positions, exp.positions)


def test_trajectory_delete_cascade(session):
    traj = Trajectory()
    expect = make_atoms_list()
    for atoms in expect:
        traj.add_atoms(atoms)
    session.add(traj)
    session.commit()

    hits = session.query(AtomsModel).all()
    assert len(hits) == 3

    session.expire_all()
    del traj.atoms_list[0]
    session.add(traj)
    session.commit()

    hits = session.query(AtomsModel).all()
    assert len(hits) == 2
