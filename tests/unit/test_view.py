from dataclasses import asdict

import pytest

from pension_planner import views
from pension_planner.service_layer.unit_of_work import SQLAlchemyUnitOfWork


pytestmark = pytest.mark.usefixtures("mappers")


def test_all_accounts(session_factory, account_factory):
    account = account_factory()
    uow = SQLAlchemyUnitOfWork(session_factory)
    with uow:
        uow.accounts.add(account)
    accounts = views.fetch_all_accounts(uow)
    assert accounts == [(account.name, account.id_)]


def test_fetch_order(session_factory, single_order_factory, standing_order_factory):
    single_order = single_order_factory()
    standing_order = standing_order_factory()
    saved_single_order = asdict(single_order)
    saved_single_order.pop("events")
    saved_standing_order = asdict(standing_order)
    saved_standing_order.pop("events")
    uow = SQLAlchemyUnitOfWork(session_factory)
    with uow:
        single_order_id = uow.orders.add(single_order)
        standing_order_id = uow.orders.add(standing_order)

    revived_single_order = views.fetch_order(single_order_id, uow)
    revived_standing_order = views.fetch_order(standing_order_id, uow)

    assert revived_single_order["type"] == "single_order"
    for key, value in saved_single_order.items():
        assert revived_single_order[key] == value
    assert revived_standing_order["type"] == "standing_order"
    for key, value in saved_standing_order.items():
        assert revived_standing_order[key] == value
