import pytest

from pension_planner.frontend.components.sidebar import TabItemAccounts


@pytest.fixture
def tab_item_accounts() -> TabItemAccounts:
    return TabItemAccounts()


class TestTabItemAccounts:

    def test_open_account(self, tab_item_accounts):
        tab_item_accounts.vue_open_account()
        assert len(tab_item_accounts.accounts) > 0
