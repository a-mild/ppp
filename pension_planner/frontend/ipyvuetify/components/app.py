import logging

from pension_planner.service_layer.messagebus import MessageBus

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

import ipyvuetify as v
import ipywidgets as w
import traitlets

# from pension_planner.frontend.ipyvuetify.components.main.main import Main
from pension_planner.frontend.ipyvuetify.components.sidebar.sidebar import SideBar
from pension_planner.frontend.ipyvuetify.components.appbar.appbar import AppBar


class App(v.VuetifyTemplate):
    sidebar = traitlets.Any().tag(sync=True, **w.widget_serialization)
    appbar = traitlets.Any().tag(sync=True, **w.widget_serialization)
    main = traitlets.Any().tag(sync=True, **w.widget_serialization)

    template = traitlets.Unicode("""
        <template>
            <v-app>
                <jupyter-widget :widget="sidebar" />
                <jupyter-widget :widget="appbar" />
                <jupyter-widget :widget="main" />
            </v-app>
        </template>
    """).tag(sync=True)

    def __init__(self, bus: MessageBus):
        self.sidebar = SideBar(bus)
        self.appbar = AppBar(bus)
        # self.main = Main(bus)
        super().__init__()