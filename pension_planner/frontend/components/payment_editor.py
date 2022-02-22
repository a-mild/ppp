import ipyvuetify as v

from pension_planner.frontend.components import COMPONENTS_DIR


class PaymentEditor(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "payment_editor_template.vue")
