import pytest

from pension_planner.adapters.payments_repo import BalanceSheet


@pytest.fixture
def balance_sheet() -> BalanceSheet:
    return BalanceSheet()


def test_add_payment(balance_sheet, single_payment) -> None:
    sheet = balance_sheet
    payment = single_payment
    sheet.add_payment(payment)
    assert payment.id_ in sheet.data


def test_delete_payment(balance_sheet, single_payment) -> None:
    sheet = balance_sheet
    payment = single_payment
    sheet.add_payment(payment)
    deleted_payment = sheet.delete_payment(payment.id_)
    assert payment.id_ not in sheet.data
    assert payment is deleted_payment
