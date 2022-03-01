from pension_planner import views
from pension_planner.service_layer.unit_of_work import SQLAlchemyUnitOfWork


def test_all_accounts(session_factory, base_account):
    uow = SQLAlchemyUnitOfWork(session_factory)
    with uow:
        uow.accounts.add(base_account)
    accounts = views.fetch_all_accounts(uow)
    assert accounts == [(base_account.name, base_account.id_)]
