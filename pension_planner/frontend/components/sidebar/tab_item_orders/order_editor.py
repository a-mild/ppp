from typing import Any
from uuid import UUID

import ipyvuetify as v
import ipywidgets as w
from ipyvue import VueWidget
from traitlets import traitlets

from pension_planner.bootstrap import bus
from pension_planner.domain.commands import UpdateOrderAttribute
from pension_planner.domain.orders import ORDER_ATTRIBUTES
from pension_planner.frontend.components import COMPONENTS_DIR
from pension_planner.frontend.utils import obtain_widget


class OrderEditor(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "sidebar" / "tab_item_orders" / "order_editor_template.vue")

    def __init__(self, *args, **kwargs):
        self.loading_new_order = None
        # dynamically construct widgets
        widgets = {parameter_name: obtain_widget(parameter_name)
                   for parameter_name in ORDER_ATTRIBUTES}
        # link widgets
        for parameter_name, widget in widgets.items():
            if isinstance(widget, VueWidget):
                names = "v_model"
            else:
                names = "value"
            widget.observe(lambda e: self.on_attribute_change(parameter_name, e), names=names)
        new_traits = {parameter_name: traitlets.Any(widget).tag(sync=True, **w.widget_serialization)
                      for parameter_name, widget in widgets.items()}
        self.add_traits(**new_traits)
        super().__init__(*args, **kwargs)

    def on_attribute_change(self, attribute: str, change: Any):
        if self.loading_new_order:
            return
        command = UpdateOrderAttribute(
            id_=UUID(self.order_id),
            attribute=attribute,
            new_value=change["new"])
        bus.handle(command)
    #
    # def update_dropdown_options(self, uow: AbstractUnitOfWork = bus.uow):
    #     accounts = views.fetch_all_accounts(uow)
    #     options = [("Außenwelt", None)] + [(name, id_) for name, id_ in accounts.items()]
    #     self.from_acc_id.options = options
    #     self.target_acc_id.options = options

