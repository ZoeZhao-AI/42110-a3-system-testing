# F3 Change Password - test cases for T003
# Tester: Akriti Saxena

from playwright.sync_api import Page, expect  # expect = used to check results

from helpers import PASSWORD, go, login, logout, register_user

NEW_PASSWORD = "New@12345"  # the password we change to
MY_ACCOUNT_TITLE = "My Account"  # the tab title after a successful login or password change
CHANGE_PASSWORD_TITLE = "Change Password"  # the tab title of the change password page
SUCCESS = "Success: Your password has been successfully updated."  # the website's success message
MISMATCH = "Password confirmation does not match password!"  # error when the two boxes differ
TOO_SHORT = "Password must be between 4 and 20 characters!"  # error when the length is wrong


def change_password(page: Page, new: str, confirm: str) -> None:
    # open the Change Password page, fill in both boxes and click Continue
    go(page, "account/password")
    page.locator("#input-password").fill(new)  # new password
    page.locator("#input-confirm").fill(confirm)  # new password again
    page.locator("input[value='Continue']").click()  # submit the form


def test_f3_s1_valid_change(page: Page) -> None:
    # Scenario 1: change to a valid new password, then log in with it
    email = register_user(page)  # create an account (this also logs in)
    change_password(page, NEW_PASSWORD, NEW_PASSWORD)

    expect(page.locator(".alert-success")).to_contain_text(SUCCESS)  # green success message at the top
    expect(page).to_have_title(MY_ACCOUNT_TITLE)  # the website returns to My Account

    logout(page)  # log out so the login below is a real login
    login(page, email, NEW_PASSWORD)  # log in with the NEW password

    expect(page).to_have_title(MY_ACCOUNT_TITLE)  # My Account page is shown
    expect(page.locator("#column-right").get_by_role("link", name="Logout")).to_be_visible()  # Logout link = user is logged in


def test_f3_s2_confirmation_mismatch(page: Page) -> None:
    # Scenario 2: the two password boxes do not match
    register_user(page)  # create an account (this also logs in)
    change_password(page, NEW_PASSWORD, "Different@999")  # confirmation differs from the new password

    expect(page.locator(".text-danger")).to_contain_text(MISMATCH)  # red message under the confirm box
    expect(page).to_have_title(CHANGE_PASSWORD_TITLE)  # still on the form, password not changed


def test_f3_s3_password_too_short(page: Page) -> None:
    # Scenario 3: the new password is 3 characters (the minimum is 4)
    register_user(page)  # create an account (this also logs in)
    change_password(page, "abc", "abc")  # 3 characters, one below the limit

    expect(page.locator(".text-danger")).to_contain_text(TOO_SHORT)  # red message under the password box
    expect(page).to_have_title(CHANGE_PASSWORD_TITLE)  # still on the form, password not changed