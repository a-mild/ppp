import logging
from datetime import datetime
from typing import Any
from uuid import UUID

import ipyvuetify as v
import ipywidgets as w
from traitlets import traitlets

from pension_planner import views
from pension_planner.domain.commands import UpdateOrderAttribute
from pension_planner.domain.orders import ORDER_ATTRIBUTES
from pension_planner.frontend.ipyvuetify.components import COMPONENTS_DIR
from pension_planner.frontend.ipyvuetify.utils import obtain_widget, MutableDict
from pension_planner.service_layer.messagebus import MessageBus


class SingleOrderEditor(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "sidebar" / "tab_item_orders" / "single_order_template.vue")

    name = traitlets.Unicode().tag(sync=True)

    from_acc_id_options = traitlets.List([{"text": letter, "value": number} for letter, number in zip("abc", range(3))]).tag(sync=True)
    from_acc_id_selected = traitlets.Any().tag(sync=True)
    target_acc_id_options = traitlets.List([{"text": letter, "value": number} for letter, number in zip("abc", range(3))]).tag(sync=True)
    target_acc_id_selected = traitlets.Any().tag(sync=True)

    datepicker_menu = traitlets.Bool(False).tag(sync=True)
    date = traitlets.Unicode(datetime.today().strftime("%Y-%m")).tag(sync=True)

    amount = traitlets.Float().tag(sync=True)

    output = traitlets.Unicode().tag(sync=True)

    def __init__(self, bus: MessageBus, *args, **kwargs):
        self.bus = bus
        super().__init__(*args, **kwargs)

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



class StandingOrderEditor(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "sidebar" / "tab_item_orders" / "standing_order_template.vue")

    name = traitlets.Unicode().tag(sync=True)

    from_acc_id_options = traitlets.List([{"text": letter, "value": number} for letter, number in zip("abc", range(3))]).tag(sync=True)
    from_acc_id_selected = traitlets.Any().tag(sync=True)

    target_acc_id_options = traitlets.List([{"text": letter, "value": number} for letter, number in zip("abc", range(3))]).tag(sync=True)
    target_acc_id_selected = traitlets.Any().tag(sync=True)

    start_date_menu = traitlets.Bool(False).tag(sync=True)
    start_date = traitlets.Unicode(datetime.today().strftime("%Y-%m")).tag(sync=True)

    end_date_menu = traitlets.Bool(False).tag(sync=True)
    end_date = traitlets.Unicode(datetime.today().strftime("%Y-%m")).tag(sync=True)

    amount = traitlets.Float().tag(sync=True)

    output = traitlets.Unicode().tag(sync=True)

    def __init__(self, bus: MessageBus, *args, **kwargs):
        self.bus = bus
        super().__init__(*args, **kwargs)

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
    orders = MutableDict().tag(sync=True, **w.widget_serialization)

    output = traitlets.Unicode().tag(sync=True)

    def __init__(self, bus: MessageBus):
        self.bus = bus
        super().__init__()

    def add_order(self, id_: UUID):
        order = views.fetch_order(id_, self.bus.uow)
        order.pop("id_")
        self.output = f"{order!r}"
        if order["type"] == "single_order":
            widget = SingleOrderEditor(
                bus=self.bus,
                name=order["name"],
                from_acc_id=str(order["from_acc_id"]),
                target_acc_id=str(order["target_acc_id"]),
                date=order["date"].strftime("%Y-%m"),
                amount=order["amount"],
            )
        elif order["type"] == "standing_order":
            widget = StandingOrderEditor(
                bus=self.bus,
                name=order["name"],
                from_acc_id=str(order["from_acc_id"]),
                target_acc_id=str(order["target_acc_id"]),
                start_date=order["start_date"].strftime("%Y-%m"),
                end_date=order["end_date"].strftime("%Y-%m"),
                amount=order["amount"],
            )
        self.orders[str(id_)] = {
            "name": order["name"],
            "widget": widget,
        }

    def vue_delete_order(self, id_: str):
        self.output = f"Delete {id_!r}"
