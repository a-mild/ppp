from io import BytesIO

import traitlets

import ipywidgets as w
import ipyvuetify as v
from ipyvuetify.extra import FileInput
from IPython.display import HTML, clear_output, display
from base64 import b64encode

from pension_planner.domain import events
from pension_planner.frontend.ipyvuetify.components import COMPONENTS_DIR
from pension_planner.domain.commands import ToggleDrawer
from pension_planner.service_layer.messagebus import MessageBus

"""
download stolen from https://github.com/voila-dashboards/voila/issues/711
"""


class AppBar(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "appbar" / "appbar_template.vue")

    loaded_filename = traitlets.Unicode(default_value="No file loaded").tag(sync=True)

    upload_widget = traitlets.Any(FileInput()).tag(sync=True, **w.widget_serialization)
    download_output_dummy = traitlets.Any(w.Output()).tag(sync=True, **w.widget_serialization)

    output = traitlets.Unicode().tag(sync=True)

    def __init__(self, bus: MessageBus):
        self.bus = bus
        self.upload_widget.observe(self.file_uploaded, names="file_info")
        super().__init__()

    def vue_toggle_drawer(self, _):
        command = ToggleDrawer()
        self.bus.handle(command)

    def vue_download_db(self, data=None):
        # see https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs for details
        # TODO: load current db file, not hardcoded file
        filename = "default.db"
        with open(filename, mode="rb") as f:
            content_b64 = b64encode(f.read()).decode()
            data_url = f'data:application/octet-stream;base64,{content_b64}'
            js_code = f"""
                    var a = document.createElement('a');
                    a.setAttribute('download', '{filename}');
                    a.setAttribute('href', '{data_url}');
                    a.click()
                """
        with self.download_output_dummy:
            clear_output()
            display(HTML(f'<script>{js_code}</script>'))

    def file_uploaded(self, data=None):
        files = self.upload_widget.get_files()
        file = files[0]
        file["file_obj"].seek(0)
        data = file["file_obj"].read()
        with open("default.db", "wb") as f:
            f.write(data)
        self.upload_widget.clear()
        event = events.DatabaseUploaded()
        self.bus.handle(event)
