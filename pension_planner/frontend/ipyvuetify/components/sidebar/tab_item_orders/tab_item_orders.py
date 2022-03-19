import ipyvuetify as v
import ipywidgets as w
from traitlets import traitlets

from pension_planner.frontend.ipyvuetify.components import COMPONENTS_DIR
from pension_planner.frontend.ipyvuetify.components.sidebar.tab_item_orders.order_editor import OrderEditor
from pension_planner.frontend.ipyvuetify.components.sidebar.tab_item_orders.overview import Overview
from pension_planner.frontend.ipyvuetify.components.sidebar.tab_item_orders.place_order import PlaceOrder


class TabItemOrders(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "sidebar" / "tab_item_orders" / "tab_item_orders_template.vue")

    place_order = traitlets.Any().tag(sync=True, **w.widget_serialization)
    order_editor = traitlets.Any().tag(sync=True, **w.widget_serialization)
    overview = traitlets.Any().tag(sync=True, **w.widget_serialization)

    def __init__(self):
        self.place_order = PlaceOrder()
        self.order_editor = OrderEditor()
        self.overview = Overview()
