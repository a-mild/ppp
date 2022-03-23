from dataclasses import asdict
from uuid import UUID

from pension_planner.domain import commands
from pension_planner.domain.account import Account
from pension_planner.domain.orders import StandingOrder, SingleOrder
from pension_planner.service_layer.unit_of_work import AbstractUnitOfWork


class OpenAccountHandler:

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def __call__(self, command: commands.OpenAccount) -> UUID:
        account = Account(
            name=command.name,
            interest_rate=command.interest_rate,
            assets=command.assets,
            liabilities=command.liabilities,
        )
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


class PlaceSingleOrderHandler:

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def __call__(self, command: commands.CreateSingleOrder) -> UUID:
        single_order = SingleOrder(**asdict(command))
        with self.uow:
            self.uow.orders.add(single_order)
            return single_order.id_


class PlaceStandingOrderHandler:

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def __call__(self, command: commands.CreateStandingOrder) -> UUID:
        standing_order = StandingOrder(**asdict(command))
        with self.uow:
            self.uow.orders.add(standing_order)
            return standing_order.id_


class DeleteOrderHandler:

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def __call__(self, command: commands.DeleteOrder) -> None:
        with self.uow:
            self.uow.orders.delete(command.id_)


class UpdateOrderAttributeHandler:

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def __call__(self, command: commands.UpdateOrderAttribute):
        with self.uow:
            self.uow.orders.update(
                id_=command.id_,
                attribute=command.attribute,
                new_value=command.new_value)
