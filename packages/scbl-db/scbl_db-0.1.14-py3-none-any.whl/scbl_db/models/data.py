from datetime import date
from typing import ClassVar, Literal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..bases import Data
from ..custom_types import samplesheet_str, stripped_str
from .entities import Lab, Person
from .processes import Assay, Platform

__all__ = ['DataSet', 'Sample']


class DataSet(Data, kw_only=True):
    __tablename__ = 'data_set'

    # DataSet attributes
    name: Mapped[samplesheet_str] = mapped_column(index=True)
    ilab_request_id: Mapped[stripped_str] = mapped_column(
        index=True
    )  # TODO: ilab request ID validation
    date_initialized: Mapped[date] = mapped_column(repr=False)

    # Parent foreign keys
    assay_name: Mapped[str] = mapped_column(
        ForeignKey('assay.name'), repr=False, default=None
    )
    lab_id: Mapped[int] = mapped_column(
        ForeignKey('lab.id'), default=None, repr=False, init=False
    )
    platform_name: Mapped[str] = mapped_column(ForeignKey('platform.name'), init=False)
    submitter_id: Mapped[int] = mapped_column(
        ForeignKey('person.id'), default=None, repr=False, init=False
    )

    # Parent models
    lab: Mapped[Lab] = relationship()
    submitter: Mapped[Person] = relationship()

    # Model metadata
    id_date_col: ClassVar[Literal['date_initialized']] = 'date_initialized'

    __mapper_args__ = {
        'polymorphic_on': 'platform_name',
    }

    def __post_init__(self):
        self.name = self.lab.name + self.assay_name + self.date_initialized.isoformat()


class Sample(Data, kw_only=True):
    __tablename__ = 'sample'

    # Sample attributes
    name: Mapped[samplesheet_str] = mapped_column(index=True)
    date_received: Mapped[date] = mapped_column(repr=False)

    # Parent foreign keys
    data_set_id: Mapped[int] = mapped_column(
        ForeignKey('data_set.id'), default=None, repr=False, init=False
    )
    platform_name: Mapped[str] = mapped_column(ForeignKey('platform.name'), init=False)

    # Model metadata
    id_date_col: ClassVar[Literal['date_received']] = 'date_received'

    __mapper_args__ = {'polymorphic_on': 'platform_name'}
