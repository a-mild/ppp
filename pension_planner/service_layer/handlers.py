from dataclasses import asdict
from uuid import UUID

from pension_planner import views
from pension_planner.domain import commands, events
from pension_planner.domain.account import Account
from pension_planner.domain.orders import SingleOrder, StandingOrder
from pension_planner.frontend import utils
from pension_planner.service_layer.unit_of_work import AbstractUnitOfWork


class ToggleDrawerHandler:

    def __call__(self, command: commands.ToggleDrawer):
        from pension_planner.frontend.app import THE_APP

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


class PlaceSingleOrderHandler:

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def __call__(self, command: commands.CreateSingleOrder) -> UUID:
        with self.uow:
            single_order = SingleOrder(**asdict(command))
            self.uow.orders.add(single_order)
            return single_order.id_


class PlaceStandingOrderHandler:

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def __call__(self, command: commands.CreateStandingOrder) -> UUID:
        with self.uow:
            standing_order = StandingOrder(**asdict(command))
            self.uow.orders.add(standing_order)
            return standing_order.id_


class UpdateOrderEditor:

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def __call__(self, event: events.AccountOpened):
        from pension_planner.frontend.app import THE_APP

        tab_item_orders = THE_APP.sidebar.tab_item_orders
        order = views.fetch_order(event.id_, self.uow)
        accounts = views.fetch_all_accounts(self.uow)
        tab_item_orders.selected_id = str(event.id_)
        tab_item_orders.control_widgets = utils.build_widgets_list(order, accounts, tab_item_orders)


class UpdateOrderAttributeHandler:

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def __call__(self, command: commands.UpdateOrderAttribute):
        with self.uow:
            self.uow.orders.update(
                id_=command.id_,
                attribute=command.attribute,
                new_value=command.new_value)


COMMAND_HANDLERS = {
    commands.ToggleDrawer: ToggleDrawerHandler,
    commands.OpenAccount: OpenAccountHandler,
    commands.UpdateAccountAttribute: UpdateAccountAttributeHandler,
    commands.CreateSingleOrder: PlaceSingleOrderHandler,
    commands.CreateStandingOrder: PlaceStandingOrderHandler,
    commands.UpdateOrderAttribute: UpdateOrderAttributeHandler
}

EVENT_HANDLERS = {
    events.AccountOpened: [UpdateOrderEditor],
    events.OrderCreated: [UpdateOrderEditor],
}
