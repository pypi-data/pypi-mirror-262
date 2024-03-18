from __future__ import annotations

import ase
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from asedb.abstract import Base
from asedb.atoms_model import CASCADE_DELETE_ALL, AtomsModel

atoms_trajectory_mapping = sa.Table(
    "atoms_trajectory_mapping",
    Base.metadata,
    sa.Column("atoms_id", sa.Integer, sa.ForeignKey("atoms.id")),
    sa.Column("trajectory_id", sa.Integer, sa.ForeignKey("trajectory.id")),
    sa.UniqueConstraint("trajectory_id", "atoms_id"),
)


class Trajectory(Base):
    __tablename__ = "trajectory"
    id: Mapped[int] = mapped_column(primary_key=True)

    project: Mapped[str] = mapped_column(nullable=True, index=True)
    atoms_list: Mapped[list[AtomsModel]] = relationship(
        secondary=atoms_trajectory_mapping,
        cascade=CASCADE_DELETE_ALL,
        single_parent=True,  # 1 atoms object can only belong to 1 trajectory. TODO: Is this what we want?
    )

    def add_atoms(self, atoms: ase.Atoms) -> AtomsModel:
        model = AtomsModel.from_atoms(atoms)
        self.atoms_list.append(model)
        return model

    def to_atoms_list(self) -> list[ase.Atoms]:
        return [model.to_atoms() for model in self.atoms_list]
