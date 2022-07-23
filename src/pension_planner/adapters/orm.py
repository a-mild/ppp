"""
With inspiration from https://stackoverflow.com/questions/66921914/using-polymorphic-classes-in-classic-mappings-style


"""
import uuid
from uuid import UUID

from sqlalchemy import Table, Column, TypeDecorator, CHAR, Unicode, Float, ForeignKey, Date, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import registry, relationship, backref

from pension_planner.domain import events
from pension_planner.domain.account import Account
from pension_planner.domain.orders import OrderBase, SingleOrder, StandingOrder


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


account_table = Table(
    "accounts",
    metadata,
    Column("id_", GUID(), primary_key=True),
    Column("name", Unicode),
    Column("interest_rate", Float),
)

orders_table = Table(
    "orders",
    metadata,
    Column("id_", GUID(), primary_key=True),
    Column("name", Unicode),
    Column("from_acc_id", ForeignKey("accounts.id_",
                                     ondelete='SET NULL'
                                     )),
    Column("target_acc_id", ForeignKey("accounts.id_",
                                       ondelete='SET NULL'
                                       )),
    Column("amount", Float),
    Column("type", Unicode)
)

single_order_table = Table(
    "single_orders",
    metadata,
    Column("id_", ForeignKey("orders.id_",
                             # ondelete="CASCADE"
                             ), primary_key=True),
    Column("date", Date),
)

standing_order_table = Table(
    "standing_orders",
    metadata,
    Column("id_", ForeignKey("orders.id_",
                             # ondelete="CASCADE"
                             ), primary_key=True),
    Column("start_date", Date),
    Column("end_date", Date),
)


def start_mappers():
    mapper_registry.map_imperatively(
        Account,
        account_table,
        properties={
            "assets": relationship(
                OrderBase,
                backref=backref("target_acc"),
                foreign_keys="OrderBase.target_acc_id",
                # cascade="all"
            ),
            "liabilities": relationship(
                OrderBase,
                backref=backref("from_acc"),
                foreign_keys="OrderBase.from_acc_id",
                # cascade="all"
            ),
        }
        )
    orders_mapping = mapper_registry.map_imperatively(
        OrderBase,
        orders_table,
        polymorphic_on=orders_table.c.type,
        with_polymorphic='*',
    )
    single_order_mapping = mapper_registry.map_imperatively(
        SingleOrder,
        single_order_table,
        inherits=orders_mapping,
        polymorphic_identity="single_order"
    )
    standing_order_mapping = mapper_registry.map_imperatively(
        StandingOrder,
        standing_order_table,
        inherits=orders_mapping,
        polymorphic_identity="standing_order"
    )


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
    # dbapi_connection.commit()


@event.listens_for(Account, "load")
@event.listens_for(SingleOrder, "load")
@event.listens_for(StandingOrder, "load")
def receive_load(entity, _):
    entity.events = []
    entity._initialized = True


@event.listens_for(Account, 'before_delete')
def receive_before_delete(mapper, connection, target: Account):
    target.events.append(events.AccountClosed(target.id_))


@event.listens_for(SingleOrder, 'before_delete')
@event.listens_for(StandingOrder, 'before_delete')
def receive_before_delete(mapper, connection, target: OrderBase):
    target.events.append(events.OrderDeleted(target.id_))
