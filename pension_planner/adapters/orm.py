import uuid
from uuid import UUID

from sqlalchemy import MetaData, Table, Column, TypeDecorator, CHAR, Unicode, Float
from sqlalchemy.orm import registry

from pension_planner.domain.account import Account


class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value


mapper_registry = registry()
metadata = mapper_registry.metadata


account = Table(
    "account",
    metadata,
    Column("id_", GUID(), primary_key=True),
    Column("name", Unicode),
    Column("interest_rate", Float)
)




def start_mappings():
    mapper_registry.map_imperatively(Account, account)
