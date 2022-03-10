from pension_planner.domain import events


def test_new_account_has_account_opened_event(account_factory):
    account = account_factory()
    assert events.AccountOpened(account.id_) in account.events


def test_changing_attribute_puts_event(account_factory):
    account = account_factory()
    old_name = account.name
    new_name = "Girokonto #2"
    account.name = new_name
    event = events.AccountAttributeUpdated(
        id_=account.id_,
        attribute="name",
        old_value=old_name,
        new_value=new_name,
    )
    assert event in account.events
