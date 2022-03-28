from pension_planner.domain import commands, events
from pension_planner.service_layer.handlers.crud import OpenAccountHandler, CloseAccountHandler, \
    UpdateAccountAttributeHandler, PlaceSingleOrderHandler, PlaceStandingOrderHandler, DeleteOrderHandler, \
    UpdateOrderAttributeHandler
from pension_planner.service_layer.handlers.frontend import UpdateFrontendAfterAccountOpened, \
    UpdateFrontendAfterAccountClosed, ToggleDrawerHandler, UpdateFrontendAfterOrderCreated, \
    UpdateFrontendAfterOrderDeleted, UpdatePlottingFrontend, UpdateFrontendAfterAccountAttributeUpdated, \
    UpdateFrontendAfterOrderAttributeUpdated, UpdateFrontendAfterDatabaseUploaded


# class AddAccountToOverview:
#
#     def __init__(self, uow: AbstractUnitOfWork):
#         self.uow = uow
#
#     def __call__(self, event: events.AccountOpened):
#         from pension_planner.frontend.ipyvuetify.components.app import THE_APP
#
#         overview = THE_APP.sidebar.tab_item_orders.overview
#
#         account = views.fetch_account(event.id_, self.uow)
#         overview.output = f"{account!r}"
#         # TypeError: keys must be str, int, float, bool or None, not UUID ...
#         overview.accounts[str(account["id_"])] = AccountExpansionPanel(name=account["name"])
#
#
# class UpdateOrderEditor:
#
#     def __init__(self, uow: AbstractUnitOfWork):
#         self.uow = uow
#
#     def __call__(self, event: events.OrderCreated):
#         from pension_planner.frontend.ipyvuetify.components.app import THE_APP
#
#         order_editor = THE_APP.sidebar.tab_item_orders.order_editor
#         order = views.fetch_order(event.id_, self.uow)
#         order_editor.current_id = event.id_
#         order_editor.loading_new_order = True
#         for attribute, value in order.items():
#             if attribute not in ORDER_ATTRIBUTES:
#                 continue
#             widget = getattr(order_editor, attribute)
#             if isinstance(widget, VueWidget):
#                 setattr(widget, "v_model", value)
#             else:
#                 setattr(widget, "value", value)
#         order_editor.loading_new_order = False
#
#
# class UpdateDropdownOptions:
#
#     def __init__(self, uow: AbstractUnitOfWork):
#         self.uow = uow
#
#     def __call__(self, event: Union[events.AccountOpened, events.OrderAttributeUpdated]):
#         from pension_planner.frontend.ipyvuetify.components.app import THE_APP
#         with THE_APP.sidebar.tab_item_orders.order_editor as editor:
#             accounts = views.fetch_all_accounts(self.uow)
#             if isinstance(event, events.AccountOpened):
#                 temp = editor.from_acc_id.value
#                 from_acc_options = [("", None)] + [(name, id_)
#                                                    for name, id_ in accounts.items()
#                                                    if not id_ == editor.target_acc_id.value]
#                 editor.from_acc_id.options = from_acc_options
#                 editor.from_acc_id.value = temp
#                 temp = editor.target_acc_id.value
#                 target_acc_options = [("", None)] + [(name, id_)
#                                                      for name, id_ in accounts.items()
#                                                      if not id_ == editor.from_acc_id.value]
#                 editor.target_acc_id.options = target_acc_options
#                 editor.target_acc_id.value = temp
#                 return
#             if isinstance(event, events.OrderAttributeUpdated):
#                 editor.output = f"Order attr updated: {event!r}"
#                 if event.attribute == "from_acc_id":
#                     temp = editor.target_acc_id.value
#                     editor.target_acc_id.options = [("", None)] + [(name, id_)
#                                                                    for name, id_ in accounts.items()
#                                                                    if not id_ == event.new_value]
#                     editor.target_acc_id.value = temp
#                 elif event.attribute == "target_acc_id":
#                     temp = editor.from_acc_id.value
#                     editor.from_acc_id.options = [("", None)] + [(name, id_)
#                                                                  for name, id_ in accounts.items()
#                                                                  if not id_ == event.new_value]
#                     editor.from_acc_id.value = temp
#                 else:
#                     return
#
#
# class UpdateOverview:
#
#     def __init__(self, uow: AbstractUnitOfWork):
#         self.uow = uow
#
#     def __call__(self, event: events.OrderAttributeUpdated):
#         from pension_planner.frontend.ipyvuetify.components.app import THE_APP
#         overview = THE_APP.sidebar.tab_item_orders.overview
#
#         logging.debug(f"{event!r}")
#         overview.output = f"{event!r}"
#
#         order = views.fetch_order(event.order_id, self.uow)
#         if event.attribute == "from_acc_id":
#             # remove from old acc
#             if event.old_value is not None:
#                 overview.output = f"Popping {event.order_id}"
#                 overview.accounts[str(event.old_value)].liabilities.pop(str(event.order_id))
#             # add to new acc
#             if event.new_value is not None:
#                 overview.output = f"Adding {event.order_id}"
#                 card = OrderCard(
#                     id_=order["id_"],
#                     name=order["name"]
#                 )
#                 overview.accounts[str(event.new_value)].liabilities[str(event.order_id)] = card
#         elif event.attribute == "target_acc_id":
#             # remove from old acc
#             if event.old_value is not None:
#                 overview.output = f"Popping {event.order_id}"
#                 overview.accounts[str(event.old_value)].assets.pop(str(event.order_id))
#             # add to new acc
#             if event.new_value is not None:
#                 card = OrderCard(
#                     id_=order["id_"],
#                     name=order["name"]
#                 )
#                 overview.accounts[str(event.new_value)].assets[str(event.order_id)] = card
#
#
# class UpdatePlot:
#
#     def __init__(self, bank_statement_repo: AbstractBankStatementRepository):
#         self.bank_statement_repo = bank_statement_repo
#
#     def __call__(self, event):
#         from pension_planner.frontend.ipyvuetify.components.app import THE_APP
#
#         total = self.bank_statement_repo.get_total()
#         fig = go.FigureWidget(px.bar(total))
#         THE_APP.main.figure = fig


class LoadDatabaseHandler:
    pass


COMMAND_HANDLERS = {
    commands.ToggleDrawer: ToggleDrawerHandler,
    commands.OpenAccount: OpenAccountHandler,
    commands.CloseAccount: CloseAccountHandler,
    commands.UpdateAccountAttribute: UpdateAccountAttributeHandler,
    commands.CreateSingleOrder: PlaceSingleOrderHandler,
    commands.CreateStandingOrder: PlaceStandingOrderHandler,
    commands.DeleteOrder: DeleteOrderHandler,
    commands.UpdateOrderAttribute: UpdateOrderAttributeHandler,
}


EVENT_HANDLERS = {
    events.AccountOpened: [
        UpdateFrontendAfterAccountOpened,
        UpdatePlottingFrontend,
    ],
    events.AccountClosed: [
        UpdateFrontendAfterAccountClosed,
        UpdatePlottingFrontend,
    ],
    events.AccountAttributeUpdated: [
        UpdateFrontendAfterAccountAttributeUpdated,
        UpdatePlottingFrontend,
    ],
    events.OrderCreated: [
        UpdateFrontendAfterOrderCreated,
        UpdatePlottingFrontend,
    ],
    events.OrderDeleted: [
        UpdateFrontendAfterOrderDeleted,
        UpdatePlottingFrontend,
    ],
    events.OrderAttributeUpdated: [
        UpdateFrontendAfterOrderAttributeUpdated,
        UpdatePlottingFrontend,
    ],
    events.DatabaseUploaded: [
        UpdateFrontendAfterDatabaseUploaded,
        UpdatePlottingFrontend,
    ]
}
