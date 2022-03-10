from pension_planner.frontend.interface import AbstractFrontendInterface
from pension_planner.frontend.ipyvuetify.components.app import App


class IPyVuetifyFrontend(AbstractFrontendInterface):
    app = App()

    def handle_toggle_drawer(self):
        self.app.sidebar.toggle_drawer()

    def handle_account_opened(self):
        pass

    def show(self):
        return self.app
