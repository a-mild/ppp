import logging

import ipyvuetify as v
import ipywidgets as w
import traitlets

from pension_planner.frontend.components import COMPONENTS_DIR

from pension_planner.domain.orders import ORDER_TYPES


MENU_DICT = [
    {"color": "grey",
     "text": "Einzahlung",
     "side": "deposit"},
    {"color": "red lighten-2",
     "text": "Auszahlung",
     "side": "payout"},
]


class SideBar(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "sidebar_template.vue")
    order_types = traitlets.List(default_value=list(ORDER_TYPES.keys())).tag(sync=True)

    drawer_open = traitlets.Bool(default_value=False).tag(sync=True)
    menu_deposit = traitlets.Bool(False).tag(sync=True)
    menu_payout = traitlets.Bool(False).tag(sync=True)

    menus = traitlets.List(MENU_DICT).tag(sync=True)

    def __init__(self):
        super().__init__()
        logging.debug("SideBar Initialized")

    def toggle_drawer(self):
        logging.debug(f"State drawer open before: {self.drawer_open}")
        self.drawer_open = not self.drawer_open
        logging.debug(f"State drawer open after: {self.drawer_open}")

    def vue_add_order(self, data):
        logging.debug(f"{data!r}")
