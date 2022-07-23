import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.pension_planner.frontend.ipyvuetify.components.main.main import Main
from pension_planner.plotting_frontend.interface import AbstractPlottingFrontend


class PlotlyPlottingFrontend(AbstractPlottingFrontend):


    def __init__(self, main: Main) -> None:
        self.main = main
        self.main.figure = go.FigureWidget()

    # TODO: prettify the plot
    def update_with(self, df: pd.DataFrame) -> None:
        fig = px.bar(df, x=df.index, y="value", color="variable")
        self.main.figure = go.FigureWidget(fig)
