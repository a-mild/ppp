import logging
from typing import Union, Any

import pension_planner.domain.commands as commands
import pension_planner.domain.events as events
from pension_planner.service_layer import handlers
from pension_planner.service_layer.unit_of_work import AbstractUnitOfWork


Message = Union[commands.Command, events.Event]


def handle(message: Message, uow: AbstractUnitOfWork):
    results = []
    queue = [message]
    while queue:
        message = queue.pop(0)
        if isinstance(message, events.Event):
            handle_event(message, queue, uow)
        elif isinstance(message, commands.Command):
            cmd_result = handle_command(message, queue, uow)
            results.append(cmd_result)
    return results


def handle_event(event: events.Event, queue: list[Message], uow: AbstractUnitOfWork) -> None:
    for handler in EVENT_HANDLERS[type(event)]:
        logging.debug(f"Handling event {event!r} with handler {handler!r}")
        try:
            handler(event, uow)
            queue.extend(uow.collect_new_events())
        except Exception:
            logging.exception(f"Exception handling {event!r}")
            continue


def handle_command(command: commands.Command, queue: list[Message], uow: AbstractUnitOfWork) -> Any:
    logging.debug(f"Handling command {command!r}")
    try:
        handler = COMMAND_HANDLERS[type(command)]
        result = handler(command, uow)
        queue.extend(uow.collect_new_events())
        return result
    except Exception:
        logging.exception(f"Exception handling {command!r}")
        raise


COMMAND_HANDLERS = {
    commands.ToggleDrawer: handlers.toggle_drawer,
    commands.OpenAccount: handlers.open_account,
}

EVENT_HANDLERS = {

}
