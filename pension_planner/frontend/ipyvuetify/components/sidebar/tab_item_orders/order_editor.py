import logging
from typing import Any

import ipyvuetify as v
import ipywidgets as w
from traitlets import traitlets

from pension_planner.domain.commands import UpdateOrderAttribute
from pension_planner.domain.orders import ORDER_ATTRIBUTES
from pension_planner.frontend.ipyvuetify.components import COMPONENTS_DIR
from pension_planner.frontend.ipyvuetify.utils import obtain_widget


class OrderEditor(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "sidebar" / "tab_item_orders" / "order_editor_template.vue")

    output = traitlets.Unicode().tag(sync=True)

    def __init__(self, *args, **kwargs):
        self.stop_commands = None
        # dynamically construct widgets
        widgets = {parameter_name: obtain_widget(parameter_name)
                   for parameter_name in ORDER_ATTRIBUTES}
        new_traits = {parameter_name: traitlets.Any(widget).tag(sync=True, **w.widget_serialization)
                      for parameter_name, widget in widgets.items()}
        self.current_id = None
        super().__init__(*args, **kwargs)
        self.add_traits(**new_traits)
        # link widgets
        self.name.observe(lambda e: self.on_attribute_change("name", e), names="v_model")
        self.from_acc_id.observe(lambda e: self.on_attribute_change("from_acc_id", e), names="value")
        self.target_acc_id.observe(lambda e: self.on_attribute_change("target_acc_id", e), names="value")
        self.date.observe(lambda e: self.on_attribute_change("date", e), names="value")
        self.start_date.observe(lambda e: self.on_attribute_change("start_date", e), names="value")
        self.end_date.observe(lambda e: self.on_attribute_change("end_date", e), names="value")
        self.amount.observe(lambda e: self.on_attribute_change("amount", e), names="v_model")

    def __enter__(self):
        # used for stopping commands when having to reset values in handlers
        self.stop_commands = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_commands = False

    def on_attribute_change(self, attribute: str, change: Any):
        if self.stop_commands is True:
            return
        from pension_planner.bootstrap import bus

        command = UpdateOrderAttribute(
            id_=self.current_id,
            attribute=attribute,
            new_value=change["new"])
        bus.handle(command)

