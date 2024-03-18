from __future__ import annotations

import io
import json
from typing import Any, TypeVar

import numpy as np
import sqlalchemy as sa
from ase.cell import Cell
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

from asedb.time_utils import get_posix_timestamp

T_Arr = TypeVar("T_Arr", bound="NamedArray")

ALLOW_PICKLE = False


Base = declarative_base(metadata=sa.MetaData(schema="asedb"))


class ArrayType(sa.types.TypeDecorator):
    """Custom type for saving/loading NumPy arrays."""

    impl = sa.LargeBinary

    def process_bind_param(self, value, dialect):
        """Convert the array going into the database."""
        if value is not None:
            if not isinstance(value, np.ndarray):
                raise TypeError(f"value must be numpy.ndarray, got {value!r}")
            return _serialize_array(value)
        return value

    def process_result_value(self, value, dialect):
        """Convert the result coming from the database."""
        if value is not None:
            value = _deserialize_array(value)
        return value

    def compare_values(self, x: Any, y: Any) -> bool:
        if x is None and y is None:
            return True
        if x is None or y is None:
            # Only 1 value is None
            return False
        if isinstance(x, np.ndarray) and isinstance(y, np.ndarray):
            if x.shape != y.shape:
                return False
            if x.dtype != y.dtype:
                return False
            return np.equal(x, y)
        return super().compare_values(x, y)
        # raise TypeError(f"x and y must be None or NumPy arrays, got {x!r} and {y!r}")


class NamedArray(Base):
    """Base table object for storing a NumPy array along with a name and some metadata."""

    __abstract__ = True

    id: Mapped[int] = mapped_column(
        sa.BigInteger().with_variant(sa.Integer, "sqlite"),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(nullable=False, index=True)

    array_meta_json: Mapped[str] = mapped_column(nullable=True)
    array_obj: Mapped[np.ndarray] = mapped_column(ArrayType, nullable=True)
    last_update_time: Mapped[float] = mapped_column(default=get_posix_timestamp, nullable=False)

    def get_array(self) -> np.ndarray:
        """Access the NumPy array object from the model."""
        return self.array_obj

    @classmethod
    def from_np_array(cls: type[T_Arr], name: str, array: np.ndarray) -> T_Arr:
        """Construct an instance of the NamedArray model from a NumPy array."""
        instance = cls(name=name)
        instance.set_array(array)
        return instance

    def set_array(self, array: np.ndarray | Cell) -> None:
        """Update the blob representing a NumPy array. The array
        will be serialized to a binary blob using the NumPy save function.

        Note: Arbitrary Python objects are not allowed, as Pickle serialization is
        disabled by default for security purposes. Change the asedb.abstract.ALLOW_PICKLE
        variable to True to allow pickle serialization.
        """
        if isinstance(array, Cell):
            # Adapt the ASE Cell object
            array = array.array
        if not isinstance(array, np.ndarray):
            raise TypeError(f"Expected a NumPy array, got {array!r}")
        self.array_meta_json = json.dumps(_get_array_metadata(array))
        self.array_obj = array
        self.last_update_time = get_posix_timestamp()

    @property
    def array_meta(self) -> None | dict[str, Any]:
        if self.array_meta_json is None:
            return None
        return json.loads(self.array_meta_json)

    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        kwargs = {
            "id": self.id,
            "name": self.name,
        }
        if (meta := self.array_meta) is not None:
            kwargs.update(**meta)
        s = ", ".join([f"{k}='{v}'" for k, v in kwargs.items()])
        return f"{cls_name}({s})"


def _serialize_array(array: np.ndarray) -> bytes:
    """Get the array serialized in bytes."""
    memfile = io.BytesIO()
    np.save(memfile, array, allow_pickle=ALLOW_PICKLE)
    return memfile.getvalue()


def _deserialize_array(blob: bytes) -> np.ndarray:
    """Load the NumPy array from the serialized bytes."""
    memfile = io.BytesIO(blob)
    return np.load(memfile, allow_pickle=ALLOW_PICKLE)


def _get_array_metadata(array: np.ndarray) -> dict[str, Any]:
    """Extract some metadata about the array."""
    meta = {
        "size": array.size,
        "shape": array.shape,
        "dtype": array.dtype.str,
    }
    return meta
