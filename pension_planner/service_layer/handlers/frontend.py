from pension_planner.domain import events, commands
from pension_planner.frontend.interface import AbstractFrontendInterface




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
