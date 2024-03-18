from __future__ import annotations

import enum
from collections.abc import Iterator


class _PropertyBase(str, enum.Enum):
    @classmethod
    def iter(cls) -> Iterator[str]:
        """An iterator over the string values of the enum.

        Yields:
            Iterator[str]: The string value of each property.
        """
        for entry in cls:
            yield entry.value

    def __str__(self) -> str:
        """Ensure calling str(...) on the enum returns the string value."""
        return self.value


class ValueProperties(_PropertyBase):
    ENERGY = "energy"
    FREE_ENERGY = "free_energy"
    MAGMOM = "magmom"


class ArrayProperties(_PropertyBase):
    FORCES = "forces"
    STRESS = "stress"
    STRESSES = "stresses"
    CHARGES = "charges"
    MAGMOMS = "magmoms"
