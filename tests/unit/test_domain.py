from pension_planner.domain import events


def test_new_account_has_account_opened_event(base_account):
    assert events.AccountOpened(base_account.id_) in base_account.events


def test_changing_attribute_puts_event(base_account):
    old_name = base_account.name
    new_name = "Girokonto #2"
    base_account.name = new_name
    event = events.AccountAttributeUpdated(
        id_=base_account.id_,
        attribute="name",
        old_value=old_name,
        new_value=new_name,
    )
    assert event in base_account.events
