import ipyvuetify as v
import ipywidgets as w
from traitlets import traitlets

from src.pension_planner.frontend import COMPONENTS_DIR


class Main(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "main" / "main_template.vue")

    figure = traitlets.Any().tag(sync=True, **w.widget_serialization)
