from sqlalchemy import select, text

from pension_planner.service_layer.unit_of_work import SQLAlchemyUnitOfWork


def test_uow_can_insert_account(session_factory, base_account):
    uow = SQLAlchemyUnitOfWork(session_factory)
    with uow:
        uow.accounts.add(base_account)

    stmt = text("SELECT * FROM accounts")
    with session_factory() as session:
        result = session.execute(stmt).all()
        assert len(result) > 0

def test_uow_can_update_attributes(session_factory, single_order):
    id_ = single_order.id_
    uow = SQLAlchemyUnitOfWork(session_factory)
    with uow:
        uow.orders.add(single_order)
    with uow:
        uow.orders.update(id_, "amount", 200)
        assert len(list(uow.collect_new_events())) > 0
    with uow:
        order = uow.orders.get(id_)
    assert order is not None
    assert order.amount == 200


def test_uow_can_get_backrefs(session_factory, base_account, single_order):
    id_ = base_account.id_
    uow = SQLAlchemyUnitOfWork(session_factory)
    with uow:
        uow.accounts.add(base_account)
        uow.orders.add(single_order)
    with uow:
        acc = uow.accounts.get(id_)
    assert acc is not None
    assert acc.assets == [single_order]
