from __future__ import annotations

import itertools
from collections import Counter
from collections.abc import Mapping

import ase
import numpy as np
import sqlalchemy as sa
from ase.calculators.calculator import Calculator as AseCalculator
from ase.calculators.singlepoint import SinglePointCalculator
from sqlalchemy.orm import Mapped, mapped_column, relationship

from asedb.abstract import Base, NamedArray
from asedb.properties import ArrayProperties, ValueProperties
from asedb.time_utils import get_posix_timestamp
from asedb.utils import float_or_none

CASCADE_DELETE_ALL = "all, delete-orphan"

ASE_CONSTRUCTOR_TRANSLATION = {
    "initial_charges": "charges",
    "initial_magmoms": "magmoms",
}


class AtomsArray(NamedArray):
    __tablename__ = "atoms_array"
    # Only 1 array with a particular atoms_id/name combo
    __table_args__ = (sa.UniqueConstraint("atoms_id", "name"),)

    atoms_id: Mapped[int] = mapped_column(
        sa.ForeignKey("atoms.id"),
        index=True,
        nullable=False,
    )


class CalcArray(NamedArray):
    __tablename__ = "calc_array"
    # Only 1 array with a particular calc_id/name combo
    __table_args__ = (sa.UniqueConstraint("calc_id", "name"),)

    calc_id: Mapped[int] = mapped_column(
        sa.ForeignKey("calculation.id"),
        index=True,
        nullable=False,
    )


class Element(Base):
    __tablename__ = "elements"
    __table_args__ = (sa.UniqueConstraint("atoms_id", "symbol"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    atoms_id: Mapped[int] = mapped_column(
        sa.ForeignKey("atoms.id"),
        index=True,
        nullable=False,
    )

    symbol: Mapped[str] = mapped_column(index=True)
    count: Mapped[int] = mapped_column()


class Calculation(Base):
    __tablename__ = "calculation"

    id: Mapped[int] = mapped_column(primary_key=True)
    atoms_id: Mapped[int] = mapped_column(
        sa.ForeignKey("atoms.id"),
        index=True,
        nullable=False,
        unique=True,
    )

    energy: Mapped[float] = mapped_column(nullable=True)
    free_energy: Mapped[float] = mapped_column(nullable=True)
    magmom: Mapped[float] = mapped_column(nullable=True)
    fmax: Mapped[float] = mapped_column(nullable=True)

    arrays: Mapped[list[CalcArray]] = relationship(cascade=CASCADE_DELETE_ALL)

    @classmethod
    def from_calc(cls, calc: AseCalculator) -> Calculation:
        """Construct a Calculation object from an ASE Calculator.
        Extracts the following properties:
        As floats:

            * energy
            * free_energy
            * magmom

        As arrays:

            * forces
            * stress
            * stresses
            * charges
            * magmoms
        """
        new: Calculation = cls()
        res = calc.results
        for prop in ValueProperties.iter():
            value = float_or_none(res.get(prop, None))
            setattr(new, prop, value)
        for array_prop in ArrayProperties.iter():
            value = res.get(array_prop, None)
            if value is not None:
                new.add_array(array_prop, value)
        return new

    def add_array(self, name: str, array: np.ndarray) -> None:
        self.arrays.append(CalcArray.from_np_array(name, array))
        if name == ArrayProperties.FORCES:
            self.fmax = np.linalg.norm(array, axis=1).max()

    def drop_array(self, name: str) -> None:
        for idx, array in enumerate(self.arrays):
            if array.name == name:
                break
        else:
            raise ValueError(f"Didn't find array with name: {name}")
        del self.arrays[idx]
        if name == ArrayProperties.FORCES:
            self.fmax = None

    def get_calc_kwargs(self) -> Mapping[str, float | np.ndarray]:
        kwargs = {}
        for prop in ValueProperties.iter():
            if (value := getattr(self, prop)) is not None:
                kwargs[prop] = value

        for array in self.arrays:
            kwargs[array.name] = array.get_array()
        return kwargs


class AtomsModel(Base):
    __tablename__ = "atoms"

    id: Mapped[int] = mapped_column(primary_key=True)

    project: Mapped[str] = mapped_column(nullable=True, index=True)
    natoms: Mapped[int] = mapped_column(nullable=False)
    pbc_int: Mapped[int] = mapped_column(nullable=False)

    last_updated: Mapped[float] = mapped_column(default=get_posix_timestamp, nullable=False)
    creation_time: Mapped[float] = mapped_column(
        default=get_posix_timestamp,
        nullable=False,
    )

    arrays: Mapped[list[AtomsArray]] = relationship(cascade=CASCADE_DELETE_ALL)
    elements: Mapped[list[Element]] = relationship(cascade=CASCADE_DELETE_ALL)
    calculation: Mapped[Calculation] = relationship(cascade=CASCADE_DELETE_ALL, uselist=False)

    @property
    def pbc(self) -> np.ndarray:
        """The full period boundary conditions."""
        return _decode_pbc(self.pbc_int)

    @property
    def has_calc(self) -> bool:
        return self.calculation is not None

    def to_atoms(self) -> ase.Atoms:
        """Export the SQL Alchemy object as an ASE Atoms object."""

        kwargs = {"pbc": self.pbc}
        # Rebuild the Atoms arrays
        for array_obj in self.arrays:
            kwargs[_atoms_array_remapper(array_obj.name)] = array_obj.get_array()

        atoms = ase.Atoms(**kwargs)
        if self.has_calc:
            calc = SinglePointCalculator(atoms, **self.calculation.get_calc_kwargs())
            atoms.calc = calc
        return atoms

    @classmethod
    def from_atoms(cls, atoms: ase.Atoms, import_calculation: bool = True) -> AtomsModel:
        atoms_sql = cls()
        atoms_sql.set_atoms(atoms, import_calculation=import_calculation)
        return atoms_sql

    def set_atoms(self, atoms: ase.Atoms, import_calculation: bool = True) -> None:
        """Read the current Atoms configurations, including the calculator,
        and save the state in the current AtomsModel instance.

        If import_calculation is True, then the calculator object will also be
        serialized into a Calculation object, otherwise the calculator will be ignored.
        """
        self.natoms = len(atoms)
        self.pbc_int = _encode_pbc(atoms.pbc)

        # Handle the meta-table with element counts
        self._set_elements(atoms)

        # Update the Atoms related arrays.
        self._set_arrays(atoms)

        if import_calculation:
            # Deal with the calculator
            self.set_calculation(atoms)
        self.last_updated = get_posix_timestamp()

    def _set_arrays(self, atoms: ase.Atoms) -> None:
        array_map = {array_obj.name: array_obj for array_obj in self.arrays}

        for name, arr in itertools.chain(
            atoms.arrays.items(),
            # Cell is not included in the "arrays" dict
            [("cell", atoms.cell)],
        ):
            if name in array_map:
                # Update the existing array object
                array_map[name].set_array(arr)
            else:
                # New array object
                self.arrays.append(AtomsArray.from_np_array(name, arr))

    def _set_elements(self, atoms: ase.Atoms) -> None:
        current_counts = Counter(atoms.symbols)
        elem_dct = {elem.symbol: elem for elem in self.elements}
        for sym, cnt in current_counts.items():
            if sym in elem_dct:
                elem_dct.pop(sym).count = cnt

            else:
                self.elements.append(Element(symbol=sym, count=cnt))
        if elem_dct:
            # We have symbols which weren't popped out, i.e. count is now 0
            for sym in elem_dct:
                self._drop_element(sym)

    def _drop_element(self, sym: str):
        for idx, elem in enumerate(self.elements):
            if elem.symbol == sym:
                del self.elements[idx]
                return
        raise ValueError(f"Element {sym} not found.")

    def get_element_counts(self) -> int:
        """Get the number of times a particular element occurs in the model."""
        counts = {}
        for elem in self.elements:
            counts[elem.symbol] = elem.count
        return counts

    def set_calculation(self, atoms: ase.Atoms) -> None:
        """Update the calculation cache for an Atoms object."""
        if calc := atoms.calc:
            self.calculation = Calculation.from_calc(calc)
        else:
            self.calculation = None


def _encode_pbc(pbc: np.ndarray) -> int:
    if len(pbc) != 3:
        raise ValueError(f"Expected 3 dimensions, got {len(pbc)}")
    return int(np.dot(pbc, [1, 2, 4]))


def _decode_pbc(pbc_int: int) -> list[bool]:
    return (pbc_int & np.array([1, 2, 4])).astype(bool)


def _atoms_array_remapper(name: str):
    """Translate an array name into the name required in the Atoms
    constructor."""
    return ASE_CONSTRUCTOR_TRANSLATION.get(name, name)
