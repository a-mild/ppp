import logging
from datetime import datetime
from typing import Any

import ipyvuetify as v
import ipywidgets as w
from traitlets import traitlets

from pension_planner.domain.commands import UpdateOrderAttribute
from pension_planner.domain.orders import ORDER_ATTRIBUTES
from pension_planner.frontend.ipyvuetify.components import COMPONENTS_DIR
from pension_planner.frontend.ipyvuetify.utils import obtain_widget
from pension_planner.service_layer.messagebus import MessageBus


class SingleOrder(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "sidebar" / "tab_item_orders" / "single_order_template.vue")

    name = traitlets.Unicode("Hallo Welt").tag(sync=True)

    from_acc_id_options = traitlets.List([{"text": letter, "value": number} for letter, number in zip("abc", range(3))]).tag(sync=True)
    from_acc_id_selected = traitlets.Any().tag(sync=True)
    target_acc_id_options = traitlets.List([{"text": letter, "value": number} for letter, number in zip("abc", range(3))]).tag(sync=True)
    target_acc_id_selected = traitlets.Any().tag(sync=True)

    datepicker_menu = traitlets.Bool(False).tag(sync=True)
    date = traitlets.Unicode(datetime.today().strftime("%Y-%m")).tag(sync=True)

    amount = traitlets.Unicode("100").tag(sync=True)

    output = traitlets.Unicode().tag(sync=True)

    def vue_update_name(self, data=None):
        self.output = f"{data!r}"

    def vue_update_from_acc_id(self, data=None):
        self.output = f"{data!r}"

    def vue_update_target_acc_id(self, data=None):
        self.output = f"{data!r}"

    def vue_update_date(self, data=None):
        self.output = f"{data!r}"

    def vue_update_amount(self, data=None):
        self.output = f"{data!r}"



class StandingOrder(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "sidebar" / "tab_item_orders" / "standing_order_template.vue")

    name = traitlets.Unicode("Hallo Welt").tag(sync=True)

    from_acc_id_options = traitlets.List([{"text": letter, "value": number} for letter, number in zip("abc", range(3))]).tag(sync=True)
    from_acc_id_selected = traitlets.Any().tag(sync=True)

    target_acc_id_options = traitlets.List([{"text": letter, "value": number} for letter, number in zip("abc", range(3))]).tag(sync=True)
    target_acc_id_selected = traitlets.Any().tag(sync=True)

    start_date_menu = traitlets.Bool(False).tag(sync=True)
    start_date = traitlets.Unicode(datetime.today().strftime("%Y-%m")).tag(sync=True)

    end_date_menu = traitlets.Bool(False).tag(sync=True)
    end_date = traitlets.Unicode(datetime.today().strftime("%Y-%m")).tag(sync=True)

    amount = traitlets.Unicode("100").tag(sync=True)

    output = traitlets.Unicode().tag(sync=True)

    def vue_update_name(self, data=None):
        self.output = f"{data!r}"

    def vue_update_from_acc_id(self, data=None):
        self.output = f"{data!r}"

    def vue_update_target_acc_id(self, data=None):
        self.output = f"{data!r}"

    def vue_update_start_date(self, data=None):
        self.output = f"{data!r}"

    def vue_update_end_date(self, data=None):
        self.output = f"{data!r}"

    def vue_update_amount(self, data=None):
        self.output = f"{data!r}"


class OrderEditor(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "sidebar" / "tab_item_orders" / "order_editor_template.vue")

    tab = traitlets.Int().tag(sync=True)
    orders = traitlets.Dict({"1": StandingOrder()}).tag(sync=True, **w.widget_serialization)

    output = traitlets.Unicode().tag(sync=True)

    def __init__(self, bus: MessageBus):
        self.bus = bus
        super().__init__()
