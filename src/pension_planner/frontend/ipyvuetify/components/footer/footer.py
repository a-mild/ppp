import ipyvuetify as v
from traitlets import traitlets

from src.pension_planner.frontend import COMPONENTS_DIR


class Footer(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "footer" / "footer_template.vue")

    output = traitlets.Unicode("Hallo Welt :)").tag(sync=True)
