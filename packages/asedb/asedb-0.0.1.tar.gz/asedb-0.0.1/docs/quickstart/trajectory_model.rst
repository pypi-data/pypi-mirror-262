The Trajectory Model
---------------------

In addition to atomic structures and calculations, the ``asedb`` library provides a ``Trajectory`` model for representing sequences of atomic structures,
typically used to represent simulation trajectories or a series of states in a calculation.

Model Overview
===============

The ``Trajectory`` model stores a collection of atomic structures (`AtomsModel` instances) as a sequence.
This model facilitates the organization and retrieval of atomic configurations that are related as a time series or a progression of states.

The relationship between ``Trajectory`` and ``AtomsModel`` is many-to-many, represented by the `atoms_trajectory_mapping` table.

.. note::
    An ``AtomsModel`` may be owned by a ``Trajectory``, so if an ``AtomsModel`` is removed from the ``atoms_list`` property and comitted to the database,
    this atoms object may be lost.

Using the Trajectory Model
==========================

Creating a new trajectory involves adding ``AtomsModel`` instances to the ``atoms_list`` attribute of a ``Trajectory`` instance.
Here's an example of how to create a trajectory, add atomic structures to it, and retrieve the structures as ASE ``Atoms`` objects:

.. code-block:: python

    from ase import Atoms
    from asedb import Trajectory
    from sqlalchemy.orm import Session

    session = Session()

    # Create a new Trajectory instance
    trajectory = Trajectory(project='My Simulation Project')

    # Add atomic structures to the trajectory
    atoms1 = Atoms('H2', positions=[[0, 0, 0], [0, 0, 1]])
    atoms2 = Atoms('H2O', positions=[[0, 0, 0], [0, 0, 1], [1, 0, 0]])
    trajectory.add_atoms(atoms1)
    trajectory.add_atoms(atoms2)

    session.add(trajectory)
    session.commit()

    # Retrieve the trajectory and its atomic structures
    retrieved_trajectory = session.query(Trajectory).first()
    atoms_list = retrieved_trajectory.to_atoms_list()
    for atoms in atoms_list:
        print(atoms)

The ``add_atoms`` method accepts an ASE ``Atoms`` object, converts it to an ``AtomsModel``, and adds it to the trajectory.
The ``to_atoms_list`` method converts the stored ``AtomsModel`` instances back into a list of ASE ``Atoms`` objects.
