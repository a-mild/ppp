import logging

import ipyvuetify as v
import ipywidgets as w
import traitlets

from pension_planner.frontend.components import COMPONENTS_DIR
from pension_planner.frontend.components.payment_editor import PaymentEditor


class SideBar(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "sidebar_template.vue")

    parts = traitlets.Dict(default_value={
        "editor": PaymentEditor()
    }).tag(sync=True, **w.widget_serialization)

    drawer_open = traitlets.Bool(default_value=True).tag(sync=True)

    tabs = traitlets.List().tag(sync=True)

    def __init__(self):
        super().__init__()
        logging.debug("SideBar Initialized")

    def toggle_drawer(self):
        logging.debug(f"State drawer open before: {self.drawer_open}")
        self.drawer_open = not self.drawer_open
        logging.debug(f"State drawer open after: {self.drawer_open}")