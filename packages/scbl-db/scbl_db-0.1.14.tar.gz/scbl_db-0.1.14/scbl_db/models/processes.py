from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..bases import Process

__all__ = ['Platform', 'Assay']


class Platform(Process, kw_only=True):
    __tablename__ = 'platform'


class Assay(Process, kw_only=True):
    __tablename__ = 'assay'

    # Parent foreign keys
    platform_name: Mapped[str] = mapped_column(
        ForeignKey('platform.name'), default=None, repr=False
    )
