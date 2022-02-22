import logging

import traitlets

import ipywidgets as widgets
import ipyvuetify as v
from IPython.core.display import display

from IPython.display import HTML, clear_output
from base64 import b64encode

from pension_planner.domain.bank_account import BankAccount
from pension_planner.frontend.components import COMPONENTS_DIR
from pension_planner.service_layer import handlers, events
from pension_planner.service_layer.events import ToggleDrawer
from pension_planner.service_layer.messagebus import handle
from pension_planner.service_layer.unit_of_work import InMemoryBankAccountRepositoryUnitOfWork

"""
download stolen from https://github.com/voila-dashboards/voila/issues/711
"""


class AppBar(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "appbar_template.vue")

    reset_traces_dialog = traitlets.Bool(default_value=False).tag(sync=True)

    loaded_filename = traitlets.Unicode(default_value="No file loaded").tag(sync=True)
    file_upload_widget = traitlets.Any(widgets.FileUpload(
        description="",
        multiple=False
    )).tag(sync=True, **widgets.widget_serialization)
    file_download_dummy_outputwidget = traitlets.Any(widgets.Output()).tag(sync=True, **widgets.widget_serialization)
    file = traitlets.Any().tag(sync=True)

    accounts = traitlets.List().tag(sync=True)
    active_tab = traitlets.Any().tag(sync=True)

    def __init__(self):
        super().__init__()
        self.file_upload_widget.observe(self.upload_traces, "value")

    def vue_toggle_drawer(self, data):
        logging.debug("Toggle drawer clicked")
        event = events.ToggleDrawer()
        handle(event)

    def vue_active_tab_changed(self, data):
        logging.debug(f"Tab changed: {data!r}")
        logging.debug(f"Active tab: {self.active_tab!r}")


    def vue_select_account(self, id_: str):
        pass

    def vue_add_bank_account(self, data):
        event = events.BankAccountCreated()
        uow = InMemoryBankAccountRepositoryUnitOfWork()
        results: list[BankAccount] = handle(event, uow)
        new_accounts = [{"id_": str(acc.id_), "name": acc.name} for acc in results]
        self.accounts = self.accounts + new_accounts

    def vue_reset_traces(self, data=None):
        self.reset_traces_dialog = False

    def upload_traces(self, change) -> None:
        res = {filename: f["content"] for filename, f in self.file_upload_widget.value.items()}
        filename, content = res.popitem()
        #result = upload_traces.send(self, filename=filename, content=content)
        #self.loaded_filename = f"{result[0][1]}"

    def trigger_file_download(self, text: str, filename: str, kind: str = 'text/json'):
        # see https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs for details
        content_b64 = b64encode(text.encode()).decode()
        data_url = f'data:{kind};charset=utf-8;base64,{content_b64}'
        js_code = f"""
            var a = document.createElement('a');
            a.setAttribute('download', '{filename}');
            a.setAttribute('href', '{data_url}');
            a.click()
        """
        with self.file_download_dummy_outputwidget:
            clear_output()
            display(HTML(f'<script>{js_code}</script>'))

    def vue_save_traces(self, event):
        """Save the state of all traces to a .json file"""
        #save_traces.send()
        pass
