from inspect import signature

from sqlalchemy import create_engine

from pension_planner import config
from pension_planner.adapters import orm
from pension_planner.frontend.interface import AbstractFrontendInterface
from pension_planner.service_layer import msg2handler
from pension_planner.service_layer.messagebus import MessageBus
from pension_planner.service_layer.unit_of_work import AbstractUnitOfWork

engine = create_engine(config.get_sqlite_uri())


def bootstrap(
        unit_of_work: AbstractUnitOfWork,
        frontend: AbstractFrontendInterface,
        start_orm=True,
) -> MessageBus:
    dependencies = {
        AbstractUnitOfWork: unit_of_work,
        AbstractFrontendInterface: frontend,
    }
    if start_orm:
        orm.metadata.create_all(engine)
        orm.start_mappers()
    command_handlers = {command: inject_dependency(handler_cls, dependencies)
                        for command, handler_cls in msg2handler.COMMAND_HANDLERS.items()}
    event_handlers = {event: [inject_dependency(handler_cls, dependencies) for handler_cls in handler_classes]
                      for event, handler_classes in msg2handler.EVENT_HANDLERS.items()}
    bus = MessageBus(
        uow=dependencies[AbstractUnitOfWork],
        command_handlers=command_handlers,
        event_handlers=event_handlers
    )
    frontend = dependencies[AbstractFrontendInterface]
    frontend.setup(bus)
    return bus


def inject_dependency(handler_cls, dependency_mapping):
    parameters = signature(handler_cls).parameters
    args = {arg_name: dependency_mapping[parameter.annotation]
            for arg_name, parameter in parameters.items()}
    return handler_cls(**args)
