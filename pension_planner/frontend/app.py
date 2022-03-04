import logging

from pension_planner.frontend.components.main.main import Main
from pension_planner.frontend.components.sidebar.sidebar import SideBar

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

import ipyvuetify as v
import ipywidgets as w
import traitlets

from pension_planner.frontend.components.appbar import AppBar


class App(v.VuetifyTemplate):
    sidebar = traitlets.Any().tag(sync=True, **w.widget_serialization)
    appbar = traitlets.Any().tag(sync=True, **w.widget_serialization)
    main = traitlets.Any().tag(sync=True, **w.widget_serialization)
    drawer_open = traitlets.Bool(default_value=True).tag(sync=True)

    template = traitlets.Unicode("""
        <template>
            <v-app>
                <jupyter-widget :widget="sidebar" />
                <jupyter-widget :widget="appbar" />
                <jupyter-widget :widget="main" />
            </v-app>
        </template>
    """).tag(sync=True)

    def __init__(self):
        self.sidebar = SideBar()
        self.appbar = AppBar()
        self.main = Main()
        super().__init__()


THE_APP = App()
