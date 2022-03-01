from dataclasses import asdict
from uuid import UUID

from pension_planner.domain import commands
from pension_planner.domain.account import Account
from pension_planner.service_layer.unit_of_work import AbstractUnitOfWork


class ToggleDrawerHandler:

    def __call__(self, command: commands.ToggleDrawer):
        from pension_planner.frontend import THE_APP

        THE_APP.sidebar.toggle_drawer()


class OpenAccountHandler:

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def __call__(self, command: commands.OpenAccount) -> UUID:
        with self.uow:
            kwargs = {k: v for k, v in asdict(command).items() if v is not None}
            account = Account(**kwargs)
            self.uow.accounts.add(account)
            return account.id_


class UpdateAccountAttributeHandler:

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def __call__(self, command: commands.UpdateAccountAttribute):
        with self.uow:
            self.uow.accounts.update(
                id_=command.id_,
                attribute=command.attribute,
                new_value=command.new_value)


COMMAND_HANDLERS = {
    commands.ToggleDrawer: ToggleDrawerHandler,
    commands.OpenAccount: OpenAccountHandler,
    commands.UpdateAccountAttribute: UpdateAccountAttributeHandler,
}

EVENT_HANDLERS = {

}
