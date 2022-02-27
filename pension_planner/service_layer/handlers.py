from dataclasses import asdict

from pension_planner.domain.account import Account
from pension_planner.domain.commands import Command
from pension_planner.service_layer.unit_of_work import AbstractUnitOfWork


def toggle_drawer(command: Command, uow: AbstractUnitOfWork):
    from pension_planner.frontend import THE_APP

    THE_APP.sidebar.toggle_drawer()


def open_account(command: Command, uow: AbstractUnitOfWork) -> Account:
    with uow:
        kwargs = {k: v for k, v in asdict(command).items() if v is not None}
        bank_account = Account(**kwargs)
        uow.accounts.add(bank_account)
        return bank_account

