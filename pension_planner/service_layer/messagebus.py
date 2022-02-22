import pension_planner.service_layer.events as events
from pension_planner.service_layer import handlers
from pension_planner.service_layer.unit_of_work import AbstractUnitOfWork


def handle(event: events.Event, uow: AbstractUnitOfWork | None = None):
    results = []
    queue = [event]
    while queue:
        event = queue.pop(0)
        for handler in HANDLERS[type(event)]:
            results.append(handler(event, uow=uow))
            queue.extend(uow.collect_new_events())
    return results


HANDLERS = {
    events.ToggleDrawer: [handlers.toggle_drawer],
    events.BankAccountCreated: [handlers.add_bank_account]
}
