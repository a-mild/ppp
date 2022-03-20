import ipyvuetify as v
from traitlets import traitlets

from pension_planner.domain.commands import CreateSingleOrder, CreateStandingOrder
from pension_planner.domain.orders import ORDER_TYPES
from pension_planner.frontend.ipyvuetify.components import COMPONENTS_DIR
from pension_planner.service_layer.messagebus import MessageBus


class PlaceOrder(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "sidebar" / "tab_item_orders" / "place_order_template.vue")

    order_names = traitlets.List(default_value=list(ORDER_TYPES.keys())).tag(sync=True)
    output = traitlets.Unicode().tag(sync=True)

    def __init__(self, bus: MessageBus):
        self.bus = bus
        super().__init__()

    def vue_place_order(self, name: str):
        if name == "SingleOrder":
            command = CreateSingleOrder()
        elif name == "StandingOrder":
            command = CreateStandingOrder()
        self.output = f"{command!r}"
        self.bus.handle(command)
