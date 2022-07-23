import ipyvuetify as v
import ipywidgets as w
from traitlets import traitlets

from src.pension_planner.frontend import COMPONENTS_DIR
from src.pension_planner.frontend.ipyvuetify.components.sidebar.tab_item_orders.order_editor import OrderEditor
from src.pension_planner.frontend import PlaceOrder
from pension_planner.service_layer.messagebus import MessageBus


class TabItemOrders(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "sidebar" / "tab_item_orders" / "tab_item_orders_template.vue")

    place_order = traitlets.Any().tag(sync=True, **w.widget_serialization)
    order_editor = traitlets.Any().tag(sync=True, **w.widget_serialization)
    #overview = traitlets.Any().tag(sync=True, **w.widget_serialization)

    def __init__(self, bus: MessageBus):
        self.place_order = PlaceOrder(bus)
        self.order_editor = OrderEditor(bus)
        # self.overview = Overview()
        super().__init__()
