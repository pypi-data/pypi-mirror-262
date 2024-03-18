.. _quickstart:


Quickstart
###########

Engine & Session
-----------------

First, you need to set up an engine & session as with any SQLAlchemy project. A helper function for creating a
SQLite engine has been provided:

.. code-block:: python

    from asedb import make_sqlite_engine, initialize_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine

    engine = make_sqlite_engine("foo.db")  # Helper function to create a SQL Alchemy engine for sqlite
    initialize_engine(engine)  # Create necessary schema/tables

    Session = sessionmaker(bind=engine)
    session = Session()


Here, we used the `make_sqlite_engine` helper function to create the SQL Alchemy engine
object for a sqlite database. You can also create your own engine, e.g. for postgres:


.. code-block:: python

    import urllib.parse
    from sqlalchemy import create_engine

    def make_engine():
        database = os.environ["PG_DATABASE"]
        user = os.environ["PG_USER"]
        password = urllib.parse.quote_plus(os.environ["PG_PASSWORD"])
        host = os.environ["PG_HOST"]
        port = os.environ["PG_PORT"]
        connection_string = (
            f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
        )
        return create_engine(connection_string)

    engine = make_engine()

The AtomsModel
--------------

Querying Atoms
===============

You can perform complex queries involving atomic structures and their elements. For example, to find all atomic structures containing Hydrogen (H) atoms
where the count of H atoms is at least 2, you can use the following query:

.. code-block:: python

    from asedb import AtomsModel, Element

    results = (
        session.query(AtomsModel)
        .join(Element)
        .where((Element.symbol == 'H') & (Element.count >= 2))
        .all()
    )

    for atom_model in results:
        print(atom_model.to_atoms())

This query joins the ``AtomsModel`` with the ``Element`` model, filters for structures containing at least two Hydrogen atoms, and retrieves the resulting atomic structures.

Working with AtomsModel
=======================

The ``AtomsModel`` class provides methods to convert between ASE's ``Atoms`` objects and the database models:

- ``to_atoms()``: Converts the database model to an ASE ``Atoms`` object.
- ``from_atoms(atoms, import_calculation=True)``: Converts an ASE ``Atoms`` object to the database model, optionally importing calculation results.

Here's an example of converting an ASE ``Atoms`` object to an ``AtomsModel`` and saving it to the database:

.. code-block:: python

    from ase import Atoms
    from asedb import AtomsModel

    # Create an ASE Atoms object
    atoms = Atoms('H2O', positions=[[0, 0, 0], [0, 0, 1], [1, 0, 0]])

    # Convert to AtomsModel and save to database
    atoms_model = AtomsModel.from_atoms(atoms)
    session.add(atoms_model)
    session.commit()

    # Retrieve and convert back to ASE Atoms
    retrieved_atoms_model = session.query(AtomsModel).first()
    atoms = retrieved_atoms_model.to_atoms()
    print(atoms)

Updating Atomic Structures
===========================

Atomic structures represented by the `AtomsModel` can be updated to reflect changes in their corresponding ASE `Atoms` objects.
This is particularly useful when an atomic structure has been modified, such as changing atom positions, adding or removing atoms, or updating simulation parameters,
and these changes need to be persisted in the database.

The ``set_atoms`` Method
=========================

The ``set_atoms`` method of the ``AtomsModel`` class provides a mechanism to update the model with a new or modified ASE `Atoms` object.
This method overwrites the existing atomic structure information in the `AtomsModel` with the data from the provided `Atoms` object,
including any changes made to the atomic configuration or associated calculation results.

Example Usage
=============

Consider an existing `AtomsModel` instance that needs to be updated due to changes in the atomic structure or simulation results. The following steps demonstrate how to apply these updates:

1. Retrieve the existing ``AtomsModel`` from the database.
2. Modify the ASE ``Atoms`` object as required by your simulation or analysis workflow.
3. Use the ``set_atoms`` method on the existing ``AtomsModel`` to apply the updates.
4. Commit the changes to the database.

.. code-block:: python

    from ase import Atom
    from asedb import AtomsModel

    # Retrieve an existing AtomsModel from the database
    atoms_model = session.query(AtomsModel).first()

    # Get the ASE Atoms object from the model
    atoms = atoms_model.to_atoms()

    # Modify the Atoms object (example: add a new atom)
    atoms += Atom('O', position=[1.2, 0, 0])

    # Update the AtomsModel with the modified Atoms object
    atoms_model.set_atoms(atoms)

    # Commit the changes to the database
    session.commit()

This process ensures that the ``AtomsModel`` in the database accurately reflects the updated atomic structure.
The ``set_atoms`` method allows for flexible and dynamic updates to atomic structures, facilitating iterative workflows and adjustments to simulation parameters or configurations.

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
