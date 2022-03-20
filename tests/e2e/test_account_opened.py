import pytest

pytestmark = pytest.mark.usefixtures("run_voila")


def test_open_account(main_page):
    # The user opens the sidebar
    sidebar = main_page.toggle_sidebar()
    # and the account tab is already active
    assert "active" in sidebar.accounts_tab.get_attribute("class")
    tab = sidebar.open_accounts_tab()   # get the subpage
    # Currently there are no accounts
    assert len(tab.accounts) == 0
    # so the user clicks on the "open account" button
    tab.open_account()
    # and a tab element along with an editor opens
    assert len(tab.accounts) == 1
    # he gets to see input fields for the name of the account and its interest rate
    controller = tab.accounts[0]
    assert "Konto" in controller.account_name
    assert float(controller.interest_rate) == 0.0

