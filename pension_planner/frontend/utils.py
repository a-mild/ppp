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


def obtain_widget(order, accounts, parent_widget):
    for attr_name, value in order.items():
        match attr_name:
            case "name":
                widget = v.TextField(label=labels["name"], v_model=value)
                widget.observe(parent_widget.on_name_change, names="v_model")
                yield widget
            case "from_acc_id":
                without_selected = [(acc_name, str(id_))
                                    for acc_name, id_ in accounts.items()
                                    if not id_ == order["target_acc_id"]]
                options = [("Außenwelt", "None")] + without_selected
                yield w.Dropdown(options=options, value=str(value), description=labels["from_acc_id"])
            case "target_acc_id":
                without_from_acc_id = [(acc_name, str(id_))
                                       for acc_name, id_ in accounts.items()
                                       if not id_ == order["from_acc_id"]]
                options = [("Außenwelt", "None")] + without_from_acc_id
                yield w.Dropdown(options=options, value=str(value), description=labels["target_acc_id"])
            case "date" | "start_date" | "end_date":
                yield w.DatePicker(description=labels[attr_name], disabled=False, value=value)
            case "amount":
                yield v.TextField(label=labels["amount"], v_model=value, type="number", prefix="€")


def build_widgets_list(order, accounts, parent_widget):
    return list(obtain_widget(order, accounts, parent_widget))
