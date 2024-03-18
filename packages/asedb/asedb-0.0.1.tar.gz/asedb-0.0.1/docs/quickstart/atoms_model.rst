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

Another example, where we query the total number of atoms:

.. code-block:: python

    (
        session.query(AtomsModel)
        .where(AtomsModel.natoms>2)
        .all()
    )


Or if you want a particular Atoms object with a previously known ID:


.. code-block:: python

    my_id = 2  # Example ID
    session.query(AtomsModel).filter_by(id=my_id).scalar()


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

    print("Model ID:", atoms_model.id)  # The ID assigned to the model after the commit.

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

.. automodule:: asedb.atoms_model
    :members: AtomsModel, Calculation, Element
    :no-index:
