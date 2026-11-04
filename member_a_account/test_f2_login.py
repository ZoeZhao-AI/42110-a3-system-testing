# F2 User Login - test cases for T002
# Tester: <your name>

from playwright.sync_api import Page, expect  # expect = used to check results

from helpers import PASSWORD, login, logout, register_user, unique_email

MY_ACCOUNT_TITLE = "My Account"  # the tab title after a successful login
LOGIN_TITLE = "Account Login"  # the tab title of the login page
NO_MATCH = "No match for E-Mail Address and/or Password."  # the website's one warning for every bad login


def test_f2_s1_valid_login(page: Page) -> None:
    # Scenario 1: log in with a registered email and the correct password
    email = register_user(page)  # create an account (this also logs into that newly created account)
    logout(page)  # log out so the login below is a real login
    login(page, email)  # enter email and password, click Login

    expect(page).to_have_title(MY_ACCOUNT_TITLE)  # My Account page is shown after login
    expect(page.locator("#column-right").get_by_role("link", name="Logout")).to_be_visible()  # Find the Logout link, since this only shows when the user is logged in (which means account created successfully)


def test_f2_s2_wrong_password(page: Page) -> None:
    # Scenario 2: the email is registered but the password is wrong
    email = register_user(page)  # create an account
    logout(page)
    login(page, email, "Wrong@99999")  # Enter the right email but a wrong wrong password

    expect(page.locator(".alert-danger")).to_contain_text(NO_MATCH)  # Find the red warning box at the top
    expect(page).to_have_title(LOGIN_TITLE)  # still on the login page, not logged in


def test_f2_s3_unregistered_email(page: Page) -> None:
    # Scenario 3: the email has never been registered
    login(page, unique_email(), PASSWORD)  # a new email that no account uses

    expect(page.locator(".alert-danger")).to_contain_text(NO_MATCH) # Find the red warning box at the top (the warning text for this scenario is the same as the previous one)
    expect(page).to_have_title(LOGIN_TITLE)  # Make sure that the browser is still on the login page since the login was not successful


def test_f2_s4_empty_fields(page: Page) -> None:
    # Scenario 4: both boxes are left blank
    login(page, "", "")  # click Login with nothing entered

    expect(page.locator(".alert-danger")).to_contain_text(NO_MATCH)  # Find the red warning box at the top (the warning text for this scenario is the same as the previous one)
    expect(page).to_have_title(LOGIN_TITLE) # Make sure that the browser is still on the login page since the login was not successful