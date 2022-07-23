import ipyvuetify as v
from traitlets import traitlets

from src.pension_planner.domain import CreateSingleOrder, CreateStandingOrder
from src.pension_planner.domain import ORDER_TYPES
from src.pension_planner.frontend import COMPONENTS_DIR
from pension_planner.service_layer.messagebus import MessageBus


class PlaceOrder(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "sidebar" / "tab_item_orders" / "place_order_template.vue")

    order_names = traitlets.List(default_value=list(ORDER_TYPES.keys())).tag(sync=True)

    def __init__(self, bus: MessageBus):
        self.bus = bus
        super().__init__()

    def vue_place_order(self, name: str):
        if name == "SingleOrder":
            command = CreateSingleOrder()
        elif name == "StandingOrder":
            command = CreateStandingOrder()
        self.bus.handle(command)
