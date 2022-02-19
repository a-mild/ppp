from uuid import UUID

from pension_planner.domain.payments import payment_factory
from pension_planner.service_layer.unit_of_work import AbstractPaymentsUnitOfWork, AbstractBankStatementUnitOfWork


def add_payment(payments_uow: AbstractPaymentsUnitOfWork,
                bank_statement_uow: AbstractBankStatementUnitOfWork,
                **payment_attrs) -> None:
    with (
            payments_uow,
            bank_statement_uow
    ):
        payment_type = payment_attrs.pop("type")
        payment = payment_factory(payment_type, **payment_attrs)
        payments_uow.payments.add_payment(payment)
        timeseries = payment.get_timeseries()
        bank_statement_uow.bank_statement.upsert_payment(payment.id_, timeseries)


def delete_payment(payments_uow: AbstractPaymentsUnitOfWork,
                   bank_statement_uow: AbstractBankStatementUnitOfWork,
                   id_: UUID) -> None:
    with (
        payments_uow,
        bank_statement_uow
    ):
        payments_uow.payments.delete_payment(id_)
        bank_statement_uow.bank_statement.delete_payment(id_)
