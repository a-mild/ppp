from datetime import datetime
from typing import Union
from uuid import UUID

import ipyvuetify as v
import ipywidgets as w
from traitlets import traitlets

from pension_planner import views
from pension_planner.domain import commands
from pension_planner.frontend.ipyvuetify.components import COMPONENTS_DIR
from pension_planner.frontend.ipyvuetify.utils import MutableDict
from pension_planner.service_layer.messagebus import MessageBus


def get_options(accounts, exclude: str):
    if exclude == "None":
        exclude = None
    else:
        exclude = UUID(exclude)
    options = [
        {"value": str(id_), "text": name, "disabled": True if id_ == exclude else False}
        for id_, name in accounts
    ]
    options = [{"text": "", "value": "None", "disabled": False}] + options
    return options


class SingleOrderEditor(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "sidebar" / "tab_item_orders" / "single_order_template.vue")

    name = traitlets.Unicode().tag(sync=True)

    from_acc_id = traitlets.Unicode().tag(sync=True)
    from_acc_id_options = traitlets.List().tag(sync=True)
    target_acc_id = traitlets.Unicode().tag(sync=True)
    target_acc_id_options = traitlets.List().tag(sync=True)

    datepicker_menu = traitlets.Bool(False).tag(sync=True)
    date = traitlets.Unicode().tag(sync=True)

    amount = traitlets.Float().tag(sync=True)

    def __init__(self, bus: MessageBus, id_: UUID, *args, **kwargs):
        self.bus = bus
        self.id_ = id_
        super().__init__(*args, **kwargs)
        self.update_dropdown_options()

    def vue_update_name(self, data=None):
        command = commands.UpdateOrderAttribute(
            id_=self.id_,
            attribute="name",
            new_value=self.name,
        )
        self.bus.handle(command)

    def vue_update_from_acc_id(self, from_acc_id: str):
        new_value = None if from_acc_id == "None" else UUID(from_acc_id)
        command = commands.UpdateOrderAttribute(
            id_=self.id_,
            attribute="from_acc_id",
            new_value=new_value,
        )
        self.bus.handle(command)

    def vue_update_target_acc_id(self, target_acc_id: str):
        new_value = None if target_acc_id == "None" else UUID(target_acc_id)
        command = commands.UpdateOrderAttribute(
            id_=self.id_,
            attribute="target_acc_id",
            new_value=new_value,
        )
        self.bus.handle(command)

    def vue_update_date(self, date_string: str):
        date = datetime.strptime(date_string, "%Y-%m")
        command = commands.UpdateOrderAttribute(
            id_=self.id_,
            attribute="date",
            new_value=date,
        )
        self.bus.handle(command)

    def vue_update_amount(self, amount=None):
        command = commands.UpdateOrderAttribute(
            id_=self.id_,
            attribute="amount",
            new_value=float(amount),
        )
        self.bus.handle(command)

    def update_dropdown_options(self):
        accounts = views.fetch_all_accounts(self.bus.uow)
        self.from_acc_id_options = get_options(accounts, exclude=self.target_acc_id)
        self.target_acc_id_options = get_options(accounts, exclude=self.from_acc_id)


class StandingOrderEditor(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "sidebar" / "tab_item_orders" / "standing_order_template.vue")

    name = traitlets.Unicode().tag(sync=True)

    from_acc_id = traitlets.Unicode().tag(sync=True)
    from_acc_id_options = traitlets.List().tag(sync=True)
    target_acc_id = traitlets.Unicode().tag(sync=True)
    target_acc_id_options = traitlets.List().tag(sync=True)

    start_date_menu = traitlets.Bool(False).tag(sync=True)
    start_date = traitlets.Unicode().tag(sync=True)

    end_date_menu = traitlets.Bool(False).tag(sync=True)
    end_date = traitlets.Unicode().tag(sync=True)

    amount = traitlets.Float().tag(sync=True)

    def __init__(self, bus: MessageBus, id_: UUID, *args, **kwargs):
        self.bus = bus
        self.id_ = id_
        super().__init__(*args, **kwargs)
        self.update_dropdown_options()

    def vue_update_name(self, data=None):
        command = commands.UpdateOrderAttribute(
            id_=self.id_,
            attribute="name",
            new_value=self.name,
        )
        self.bus.handle(command)

    def vue_update_from_acc_id(self, from_acc_id: str):
        new_value = None if from_acc_id == "None" else UUID(from_acc_id)
        command = commands.UpdateOrderAttribute(
            id_=self.id_,
            attribute="from_acc_id",
            new_value=new_value,
        )
        self.bus.handle(command)

    def vue_update_target_acc_id(self, target_acc_id: str):
        new_value = None if target_acc_id == "None" else UUID(target_acc_id)
        command = commands.UpdateOrderAttribute(
            id_=self.id_,
            attribute="target_acc_id",
            new_value=new_value,
        )
        self.bus.handle(command)

    def vue_update_start_date(self, date_string: str):
        date = datetime.strptime(date_string, "%Y-%m")
        command = commands.UpdateOrderAttribute(
            id_=self.id_,
            attribute="start_date",
            new_value=date,
        )
        self.bus.handle(command)

    def vue_update_end_date(self, date_string: str):
        date = datetime.strptime(date_string, "%Y-%m")
        command = commands.UpdateOrderAttribute(
            id_=self.id_,
            attribute="end_date",
            new_value=date,
        )
        self.bus.handle(command)

    def vue_update_amount(self, amount=None):
        command = commands.UpdateOrderAttribute(
            id_=self.id_,
            attribute="amount",
            new_value=float(amount),
        )
        self.bus.handle(command)

    def update_dropdown_options(self):
        accounts = views.fetch_all_accounts(self.bus.uow)
        self.from_acc_id_options = get_options(accounts, exclude=self.target_acc_id)
        self.target_acc_id_options = get_options(accounts, exclude=self.from_acc_id)


class OrderEditor(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "sidebar" / "tab_item_orders" / "order_editor_template.vue")

    tab = traitlets.Int().tag(sync=True)
    orders = MutableDict().tag(sync=True, **w.widget_serialization)

    def __init__(self, bus: MessageBus):
        self.bus = bus
        super().__init__()

    def add_order(self, id_: UUID):
        order = views.fetch_order(id_, self.bus.uow)
        if order["type"] == "single_order":
            widget = SingleOrderEditor(
                bus=self.bus,
                id_=order["id_"],
                name=order["name"],
                from_acc_id=str(order["from_acc_id"]),
                target_acc_id=str(order["target_acc_id"]),
                date=order["date"].strftime("%Y-%m"),
                amount=order["amount"],
            )
        elif order["type"] == "standing_order":
            widget = StandingOrderEditor(
                bus=self.bus,
                id_=order["id_"],
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
        command = commands.DeleteOrder(UUID(id_))
        self.bus.handle(command)

    def delete_order(self, id_: UUID):
        self.orders.pop(str(id_))

    def update_dropdowns(self):
        for order in self.orders.values():
            widget: Union[SingleOrderEditor, StandingOrderEditor] = order["widget"]
            widget.update_dropdown_options()
