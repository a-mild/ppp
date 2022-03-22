import functools

import pandas as pd

from pension_planner.domain import events, commands
from pension_planner.domain.bank_statement_service import produce_bankstatement, concat_series, merge
from pension_planner.frontend.interface import AbstractFrontendInterface
from pension_planner.service_layer.unit_of_work import AbstractUnitOfWork


class ToggleDrawerHandler:

    def __init__(self, frontend: AbstractFrontendInterface):
        self.frontend = frontend

    def __call__(self, command: commands.ToggleDrawer):
        self.frontend.handle_toggle_drawer()


class UpdateFrontendAfterAccountOpened:

    def __init__(self, frontend: AbstractFrontendInterface):
        self.frontend = frontend

    def __call__(self, event: events.AccountOpened):
        self.frontend.handle_account_opened(event.id_)


class UpdateFrontendAfterAccountClosed:

    def __init__(self, frontend: AbstractFrontendInterface):
        self.frontend = frontend

    def __call__(self, event: events.AccountOpened):
        self.frontend.handle_account_closed(event.id_)


class UpdateFrontendAfterOrderCreated:

    def __init__(self, frontend: AbstractFrontendInterface):
        self.frontend = frontend

    def __call__(self, event: events.OrderCreated):
        self.frontend.handle_order_created(event.id_)


class UpdateFrontendAfterOrderDeleted:

    def __init__(self, frontend: AbstractFrontendInterface):
        self.frontend = frontend

    def __call__(self, event: events.OrderDeleted):
        self.frontend.handle_order_deleted(event.id_)


class UpdatePlottingFrontend:

    def __init__(self, uow: AbstractUnitOfWork, frontend: AbstractFrontendInterface):
        self.uow = uow
        self.frontend = frontend

    def __call__(self, event: events.Event):
        with self.uow:
            accounts = self.uow.accounts.list()
            bank_statements = [produce_bankstatement(account) for account in accounts]
            totals = merge([bstmt["total"] for bstmt in bank_statements])
            total: pd.Series = totals.sum(axis=1)
        self.frontend.update_plotting_frontend(x=total.index.tolist(), y=total.tolist())
