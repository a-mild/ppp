import ipyvuetify as v
from traitlets import traitlets

from pension_planner.bootstrap import bus
from pension_planner.domain.commands import CreateSingleOrder, CreateStandingOrder
from pension_planner.domain.orders import ORDER_TYPES
from pension_planner.frontend.ipyvuetify.components import COMPONENTS_DIR


class PlaceOrder(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "sidebar" / "tab_item_orders" / "place_order_template.vue")

    order_names = traitlets.List(default_value=list(ORDER_TYPES.keys())).tag(sync=True)

    def vue_place_order(self, name: str):
        if name == "SingleOrder":
            command = CreateSingleOrder()
        elif name == "StandingOrder":
            command = CreateStandingOrder()
        bus.handle(command)
