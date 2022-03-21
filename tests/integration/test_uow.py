import pytest
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from pension_planner.domain import events
from pension_planner.domain.account import Account
from pension_planner.domain.orders import OrderBase


pytestmark = pytest.mark.usefixtures("mappers")


def test_uow_can_add_entities(sa_uow, session, account_factory, single_order_factory, standing_order_factory):
    account = account_factory()
    single_order = single_order_factory()
    standing_order = standing_order_factory()
    with sa_uow:
        # prevent objects from being detached
        sa_uow.session.expire_on_commit = False
        account_id = sa_uow.accounts.add(account)
        single_order_id = sa_uow.orders.add(single_order)
        standing_order_id = sa_uow.orders.add(standing_order)

    with session:
        stmt = (select(Account)
                .filter_by(id_=account_id)
                .options(joinedload(Account.assets), joinedload(Account.liabilities))
                )
        account_revived, = session.execute(stmt).first()
        stmt = select(OrderBase).filter_by(id_=single_order_id)
        single_order_revived, = session.execute(stmt).first()
        stmt = select(OrderBase).filter_by(id_=standing_order_id)
        standing_order_revived, = session.execute(stmt).first()
        assert account_revived == account
        assert single_order_revived == single_order
        assert standing_order_revived == standing_order


def test_uow_can_collect_entity_created_events(sa_uow, account_factory, single_order_factory):
    account = account_factory()
    single_order = single_order_factory()
    with sa_uow:
        account_id = sa_uow.accounts.add(account)
        single_order_id = sa_uow.orders.add(single_order)
    account_created_event = events.AccountOpened(id_=account_id)
    order_created_event = events.OrderCreated(id_=single_order_id)
    collected_events = list(sa_uow.collect_new_events())
    assert account.events == []
    assert single_order.events == []
    assert len(collected_events) == 2
    assert account_created_event in collected_events
    assert order_created_event in collected_events


def test_uow_can_collect_entity_deleted_events(sa_uow, account_factory, single_order_factory):
    account = account_factory()
    single_order = single_order_factory()
    with sa_uow:
        account_id = sa_uow.accounts.add(account)
        single_order_id = sa_uow.orders.add(single_order)

    # delete again
    with sa_uow:
        sa_uow.accounts.delete(account_id)

    account_closed_event = events.AccountClosed(account_id)
    collected_events = list(sa_uow.collect_new_events())
    assert account_closed_event in collected_events


def test_uow_can_collect_entity_updated_events(sa_uow, account_factory, single_order_factory):
    account = account_factory()
    old_account_name = account.name
    single_order = single_order_factory()
    old_order_name = single_order.name
    with sa_uow:
        account_id = sa_uow.accounts.add(account)
        single_order_id = sa_uow.orders.add(single_order)
    list(sa_uow.collect_new_events())   # empty the event lists
    with sa_uow:
        sa_uow.accounts.update(account_id, "name", "Blackrock Konto #100")
        sa_uow.orders.update(single_order_id, "name", "Riesiger Auftrag")
    account_updated_event = events.AccountAttributeUpdated(
        id_=account_id,
        attribute="name",
        old_value=old_account_name,
        new_value="Blackrock Konto #100"
    )
    order_updated_event = events.OrderAttributeUpdated(
        id_=single_order_id,
        attribute="name",
        old_value=old_order_name,
        new_value="Riesiger Auftrag"
    )
    collected_events = list(sa_uow.collect_new_events())
    assert len(collected_events) == 2
    assert account_updated_event in collected_events
    assert order_updated_event in collected_events
