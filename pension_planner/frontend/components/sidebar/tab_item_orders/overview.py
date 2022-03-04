from uuid import UUID

import ipywidgets as w
import ipyvuetify as v
from traitlets import traitlets

from pension_planner.frontend.components import COMPONENTS_DIR
from pension_planner.frontend.utils import MutableDict


class OrderCard(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "sidebar" / "tab_item_orders" / "order_card_template.vue")

    name = traitlets.Unicode().tag(sync=True)
    show_details = traitlets.Bool(False).tag(sync=True)
    id_ = traitlets.Any()


class AccountExpansionPanel(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "sidebar" / "tab_item_orders" / "account_expansion_panel_template.vue")

    name = traitlets.Unicode().tag(sync=True)

    assets = MutableDict().tag(sync=True, **w.widget_serialization)
    liabilities = MutableDict().tag(sync=True, **w.widget_serialization)


class Overview(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "sidebar" / "tab_item_orders" / "overview_template.vue")

    accounts = MutableDict().tag(sync=True, **w.widget_serialization)

    output = traitlets.Unicode().tag(sync=True)