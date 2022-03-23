import ipyvuetify as v
import ipywidgets as w
from traitlets import traitlets

from pension_planner.frontend.ipyvuetify.components import COMPONENTS_DIR


class Main(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "main" / "main_template.vue")

    figure = traitlets.Any().tag(sync=True, **w.widget_serialization)

    x = traitlets.Unicode().tag(sync=True)
    y = traitlets.Unicode().tag(sync=True)
