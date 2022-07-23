import ipyvuetify as v
import ipywidgets as w
import traitlets
from src.pension_planner.frontend import COMPONENTS_DIR
from src.pension_planner.frontend.ipyvuetify.components.sidebar.tab_item_accounts.tab_item_accounts import TabItemAccounts
from src.pension_planner.frontend import TabItemOrders
from pension_planner.service_layer.messagebus import MessageBus


class SideBar(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "sidebar" / "sidebar_template.vue")

    drawer_open = traitlets.Bool(default_value=False).tag(sync=True)

    tab = traitlets.Int().tag(sync=True)

    tab_item_accounts: TabItemAccounts = traitlets.Any().tag(sync=True, **w.widget_serialization)
    tab_item_orders: TabItemOrders = traitlets.Any().tag(sync=True, **w.widget_serialization)

    def __init__(self, bus: MessageBus):
        self.bus = bus
        self.tab_item_accounts = TabItemAccounts(bus)
        self.tab_item_orders = TabItemOrders(bus)
        super().__init__()

    def toggle_drawer(self):
        self.drawer_open = not self.drawer_open
