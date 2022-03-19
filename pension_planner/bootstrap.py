from inspect import signature

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pension_planner import config
from pension_planner.adapters import orm
from pension_planner.domain.bank_statement_service import PandasBankStatementRepository, AbstractBankStatementRepository
from pension_planner.frontend.interface import AbstractFrontendInterface
from pension_planner.frontend.ipyvuetify.main import IPyVuetifyFrontend
from pension_planner.service_layer import handlers
from pension_planner.service_layer.messagebus import MessageBus
from pension_planner.service_layer.unit_of_work import AbstractUnitOfWork, SQLAlchemyUnitOfWork

engine = create_engine(config.get_sqlite_uri())


default_dependencies = {
    AbstractUnitOfWork: SQLAlchemyUnitOfWork(
        session_factory=sessionmaker(bind=engine, future=True, expire_on_commit=False)),
    AbstractFrontendInterface: IPyVuetifyFrontend(),
}


def bootstrap(
        start_orm=True,
        dependencies=default_dependencies,
) -> MessageBus:
    if start_orm:
        orm.metadata.create_all(engine)
        orm.start_mappers()
    command_handlers = {command: inject_dependency(handler_cls, dependencies)
                        for command, handler_cls in handlers.COMMAND_HANDLERS.items()}
    event_handlers = {event: [inject_dependency(handler_cls, dependencies) for handler_cls in handler_classes]
                      for event, handler_classes in handlers.EVENT_HANDLERS.items()}
    return MessageBus(
        uow=dependencies[AbstractUnitOfWork],
        command_handlers=command_handlers,
        event_handlers=event_handlers
    )


def inject_dependency(handler_cls, dependency_mapping):
    parameters = signature(handler_cls).parameters
    args = {arg_name: dependency_mapping[parameter.annotation]
            for arg_name, parameter in parameters.items()}
    return handler_cls(**args)
