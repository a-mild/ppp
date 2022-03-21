from dataclasses import asdict
from uuid import UUID

from pension_planner.domain import commands
from pension_planner.domain.account import Account
from pension_planner.service_layer.unit_of_work import AbstractUnitOfWork


class OpenAccountHandler:

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def __call__(self, command: commands.OpenAccount) -> UUID:
        kwargs = {k: v for k, v in asdict(command).items() if v is not None}
        account = Account(**kwargs)
        with self.uow:
            self.uow.accounts.add(account)
        return account.id_


class CloseAccountHandler:

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def __call__(self, command: commands.CloseAccount):
        with self.uow:
            self.uow.accounts.delete(command.id_)



class UpdateAccountAttributeHandler:

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def __call__(self, command: commands.UpdateAccountAttribute):
        with self.uow:
            self.uow.accounts.update(
                id_=command.id_,
                attribute=command.attribute,
                new_value=command.new_value)
