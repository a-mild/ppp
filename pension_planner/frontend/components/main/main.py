import plotly.express as px
import plotly.graph_objects as go

import ipyvuetify as v
import ipywidgets as w
from traitlets import traitlets

from pension_planner.frontend.components import COMPONENTS_DIR

df = px.data.medals_wide()
test_figure = go.FigureWidget(px.bar(df, x="nation", y=["gold", "silver", "bronze"], title="Wide-Form Input"))


class Main(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "main" / "main_template.vue")

    figure = traitlets.Any(test_figure).tag(sync=True, **w.widget_serialization)
