import logging

import ipyvuetify as v
from traitlets import traitlets

from pension_planner.frontend.components import COMPONENTS_DIR
from pension_planner.domain.orders import PAYMENT_TYPES
from pension_planner.service_layer.events import PaymentAdded
from pension_planner.service_layer.messagebus import handle

PAYMENT_NAMES = list(PAYMENT_TYPES.keys())


class AddPaymentDiv(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "add_payment_div_template.vue")
    menu = traitlets.Bool(False).tag(sync=True)
    payment_names = traitlets.List(default_value=PAYMENT_NAMES).tag(sync=True)

    def __init__(self):
        logging.debug(f"{PAYMENT_NAMES!r}")
        super().__init__()
        logging.debug("Add payment initialized")

    def add_payment(self, payment_name: str):
        event = PaymentAdded(type_=payment_name)
        handle(event)
