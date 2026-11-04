# F3 Change Password - test cases for T003
# Tester: Akriti Saxena

from playwright.sync_api import Page, expect  # expect = used to check results

from helpers import PASSWORD, go, login, logout, register_user

# ---------------- Variables ---------------------
NEW_PASSWORD = "NewPass@12345"  # The new password we will change to
MY_ACCOUNT_TITLE = "My Account"  # The page title after a successful login or password change - the site will navigate us to the "My Account" page
CHANGE_PASSWORD_TITLE = "Change Password"  # The title of the Change Password page
SUCCESS = "Success: Your password has been successfully updated."  # The success message displayed after we successfully change password
MISMATCH = "Password confirmation does not match password!"  # The error message displayed when the two input boxes differ
TOO_SHORT = "Password must be between 4 and 20 characters!"  # The error message displayed when the length of the password is not satisfied

# ---------------- Child function to perform password change ---------------
def change_password(page: Page, new: str, confirm: str) -> None:
    # open the Change Password page, fill in both boxes with the new password and click Continue
    go(page, "account/password")
    page.locator("#input-password").fill(new)  # new password
    page.locator("#input-confirm").fill(confirm)  # new password again
    page.locator("input[value='Continue']").click()  # submit the form

# ----------------- Main test functions ------------------------------------
def test_f3_s1_valid_change(page: Page) -> None:
    # Scenario 1: change to a valid new password, then log in with it
    email = register_user(page)  # Create an account (this also logs in)
    change_password(page, NEW_PASSWORD, NEW_PASSWORD)

    expect(page.locator(".alert-success")).to_contain_text(SUCCESS)  # Find the green box with the success message displayed at the top of the page
    expect(page).to_have_title(MY_ACCOUNT_TITLE)  # Ensure that the website redirects us to the My Account page

    logout(page)  # Log out from the previous session first
    login(page, email, NEW_PASSWORD)  # log in with the NEW password

    expect(page).to_have_title(MY_ACCOUNT_TITLE)  # Ensure that the website redirects us to the My Account page - which means the log in is successful
    expect(page.locator("#column-right").get_by_role("link", name="Logout")).to_be_visible()  # Find the Log out link in the new page - meaning that the user has successfully log in


def test_f3_s2_confirmation_mismatch(page: Page) -> None:
    # Scenario 2: the two password boxes do not match
    register_user(page)  # create an account (this also logs in)
    change_password(page, NEW_PASSWORD, "MismatchPass@999")  # Change the password to a different password - on the condition that two boxes are filled with different password strings

    expect(page.locator(".text-danger")).to_contain_text(MISMATCH)  # Find the red box with an error message displayed under the confirm box
    expect(page).to_have_title(CHANGE_PASSWORD_TITLE)  # Ensure that the browser isstill on the change password page and not redirected anywhere


def test_f3_s3_password_too_short(page: Page) -> None:
    # Scenario 3: the new password is 3 characters (the minimum is 4)
    register_user(page)  # create an account (this also logs in)
    change_password(page, "abc", "abc")  # Change the account password to a new password that only has 3 characters (below the limit)

    expect(page.locator(".text-danger")).to_contain_text(TOO_SHORT)  # Find the red box with an error message displayed under the confirm box
    expect(page).to_have_title(CHANGE_PASSWORD_TITLE)  # Ensure that the browser isstill on the change password page and not redirected anywhere