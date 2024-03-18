.. _asedb-documentation:

ASEDB Library Documentation
===========================

The ``asedb`` library provides a comprehensive ORM model for storing and querying atomic simulations using
`SQLAlchemy <https://www.sqlalchemy.org/>`_ and `ASE <https://wiki.fysik.dtu.dk/ase/>`_ (Atomic Simulation Environment).
It allows efficient storage and retrieval of atomic structures and their associated calculations.

Installation
------------

The module can be installed via pip:

.. code-block:: bash

    pip install asedb

Models Overview
---------------

The core models in the ``asedb`` library include:

- ``AtomsModel``: Represents atomic structures.
- ``Element``: Stores information about elements within an atomic structure.
- ``Calculation``: Holds calculation results associated with an atomic structure.

For more information on how to use the ``asedb`` package, see the :ref:`quickstart`.

.. toctree::
    :maxdepth: 1
    :caption: Contents:

    quickstart
    api
    license
