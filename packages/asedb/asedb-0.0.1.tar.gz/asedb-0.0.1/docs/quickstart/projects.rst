.. projects:

Projects
########


Managing Projects with the `project` Attribute
----------------------------------------------

The `asedb` library supports the management of atomic structures and trajectories across multiple projects using the `project` attribute.
This feature allows users to categorize and isolate data within specific projects, simplifying data organization and retrieval.
The `project` attribute is available in both the `AtomsModel` and `Trajectory` models, enabling consistent project-based filtering across different types of data.

Using the `project` Attribute
-----------------------------

The `project` attribute can be set when creating new instances of `AtomsModel` or `Trajectory`, and can be used as a
criterion for querying the database to retrieve only the data associated with a specific project.

When creating a new `AtomsModel` or `Trajectory`, specify the `project` attribute to categorize the data:

.. code-block:: python

    from ase import Atoms
    from asedb import AtomsModel, Trajectory

    # Create a Trajectory within a specific project
    trajectory = Trajectory(project='Molecular Dynamics')

    # Create an AtomsModel within a specific project
    atoms = Atoms('H2O', positions=[[0, 0, 0], [0, 0, 1], [1, 0, 0]])

    model = trajectory.add_atoms(atoms)  # Creates an returns a new AtomsModel instance
    model.project = "Water Simulation"

    session.add(trajectory)
    session.commit()

Querying by Project
-------------------

To retrieve data from a specific project, use the `project` attribute as a filter in your queries:

.. code-block:: python

    # Retrieve all AtomsModel instances from the 'Water Simulation' project
    water_models = session.query(AtomsModel).filter(AtomsModel.project == 'Water Simulation').all()

    # Retrieve all Trajectory instances from the 'Molecular Dynamics' project
    md_trajectories = session.query(Trajectory).filter(Trajectory.project == 'Molecular Dynamics').all()

This approach allows for efficient organization and retrieval of project-specific data, ensuring that queries are streamlined and manageable.
