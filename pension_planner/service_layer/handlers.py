from dataclasses import asdict

from pension_planner.domain.bank_account import BankAccount
from pension_planner.service_layer.events import Event
from pension_planner.service_layer.unit_of_work import AbstractUnitOfWork


def toggle_drawer(event: Event, *args, **kwargs):
    from pension_planner.frontend import THE_APP

    THE_APP.sidebar.toggle_drawer()


def add_bank_account(event: Event, uow: AbstractUnitOfWork) -> str:
    with uow:
        kwargs = {k: v for k, v in asdict(event).items() if v is not None}
        bank_account = BankAccount(**kwargs)
        uow.accounts.add(bank_account)
        return bank_account

