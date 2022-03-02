from datetime import date
from typing import Any

import ipywidgets as w
import ipyvuetify as v

labels = {
    "name": "Name",
    "from_acc_id": "Von:",
    "target_acc_id": "Nach:",
    "date": "Datum:",
    "start_date": "Anfangsdatum:",
    "end_date": "Enddatum",
    "amount": "Betrag",
}


def obtain_widget(attribute_name):
        match attribute_name:
            case "name":
                widget = v.TextField(label=labels["name"], v_model=None)
                return widget
            case "from_acc_id":
                options = [("Außenwelt", None)]
                return w.Dropdown(options=options, description=labels["from_acc_id"])
            case "target_acc_id":
                options = [("Außenwelt", None)]
                return w.Dropdown(options=options, description=labels["target_acc_id"])
            case "date" | "start_date" | "end_date":
                return w.DatePicker(description=labels[attribute_name], value=date.today())
            case "amount":
                return v.TextField(label=labels["amount"], v_model=None, type="number", prefix="€")
