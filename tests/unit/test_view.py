from dataclasses import asdict

from pension_planner import views
from pension_planner.service_layer.unit_of_work import SQLAlchemyUnitOfWork


def test_all_accounts(session_factory, base_account):
    uow = SQLAlchemyUnitOfWork(session_factory)
    with uow:
        uow.accounts.add(base_account)
    accounts = views.fetch_all_accounts(uow)
    assert accounts == [(base_account.name, base_account.id_)]


def test_fetch_order(session_factory, standing_order):
    uow = SQLAlchemyUnitOfWork(session_factory)
    with uow:
        uow.orders.add(standing_order)
    order = views.fetch_order(standing_order.id_, uow)
    for key, value in asdict(standing_order).items():
        if key == "events":
            continue
        assert order[key] == value, f"Test {key}"

