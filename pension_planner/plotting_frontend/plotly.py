from datetime import date

import plotly.express as px
import plotly.graph_objects as go

from pension_planner.frontend.ipyvuetify.components.main.main import Main
from pension_planner.plotting_frontend.interface import AbstractPlottingFrontend


class PlotlyPlottingFrontend(AbstractPlottingFrontend):

    def __init__(self, main: Main) -> None:
        self.main = main
        fig = go.FigureWidget()
        fig.add_scatter(y=list(range(10)))
        self.main.figure = fig

    def update_with(self, x: list[date], y: list[float]) -> None:
        trace = self.main.figure.data[0]
        trace.x = x
        trace.y = y
