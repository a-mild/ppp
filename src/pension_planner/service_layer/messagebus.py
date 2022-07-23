import logging
from typing import Union, Any

import src.pension_planner.domain.commands as commands
import src.pension_planner.domain.events as events
from pension_planner.service_layer import handlers
from pension_planner.service_layer.unit_of_work import AbstractUnitOfWork


bus_logger = logging.getLogger("bus_logger")
file_handler = logging.FileHandler("bus.log")
bus_logger.addHandler(file_handler)
bus_logger.setLevel(logging.DEBUG)

Message = Union[commands.Command, events.Event]


class MessageBus:

    def __init__(self,
                 uow: AbstractUnitOfWork,
                 command_handlers,
                 event_handlers):
        self.uow = uow
        self.command_handlers = command_handlers
        self.event_handlers = event_handlers
        self.queue = None
        self.command_history = []
        self.event_history = []

    def handle(self, message: Message):
        results = []
        self.queue = [message]
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, events.Event):
                self.handle_event(message)
            elif isinstance(message, commands.Command):
                cmd_result = self.handle_command(message)
                results.append(cmd_result)
        return results

    def handle_event(self, event: events.Event) -> None:
        for handler in self.event_handlers[type(event)]:
            bus_logger.debug(f"Handling event {event!r} with handler {handler!r}")
            try:
                handler(event)
                self.queue.extend(self.uow.collect_new_events())
            except Exception:
                bus_logger.exception(f"Exception handling {event!r}")
                continue
        else:
            self.event_history.append(event)

    def handle_command(self, command: commands.Command) -> Any:
        bus_logger.debug(f"Handling command {command!r}")
        try:
            handler = self.command_handlers[type(command)]
            result = handler(command)
            self.queue.extend(self.uow.collect_new_events())
        except Exception:
            bus_logger.exception(f"Exception handling {command!r}")
            raise
        else:
            self.command_history.append(command)
            return result
