import plotly.express as px
import plotly.graph_objects as go

import ipyvuetify as v
import ipywidgets as w
from traitlets import traitlets

from pension_planner.frontend.ipyvuetify.components import COMPONENTS_DIR
import matplotlib.pyplot as plt

df = px.data.medals_wide()
fig = go.FigureWidget(px.bar(df, x="nation", y=["gold", "silver", "bronze"], title="Wide-Form Input"))
# fig, ax = plt.subplots()
# ln, = ax.plot(range(5))



class Main(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "main" / "main_template.vue")

    figure = traitlets.Any(fig).tag(sync=True, **w.widget_serialization)



