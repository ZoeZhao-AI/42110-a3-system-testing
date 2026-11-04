# F1 User Registration - test cases for T001
# Tester: Quang Huy Vu

from playwright.sync_api import Page, expect

from helpers import logout, register_user, submit_registration

SUCCESS_TITLE = "Your Account Has Been Created!"  # the success page shows this as its tab title, not as a heading
REGISTER_TITLE = "Register Account"  # the tab title of the registration page


def test_f1_s1_valid_registration(page: Page) -> None:
    # Scenario 1: register with valid details and check the account is created
    submit_registration(page)  # fill in the form and click Continue

    expect(page).to_have_title(SUCCESS_TITLE)  # success page is shown
    expect(page.locator("#content")).to_contain_text("successfully created")  # Find the "Your new account has been successfully created!" on the page
    expect(page.locator("#column-right").get_by_role("link", name="Logout")).to_be_visible()  # Find the Logout link, since this only shows when the user is logged in (which means account created successfully)


def test_f1_s2_duplicate_email(page: Page) -> None:
    # Scenario 2: register again with an email that is already registered
    email = register_user(page)  # first perform the registration (also logs in)
    logout(page) # then log out
    submit_registration(page, email=email)  # the try to create a new account with the same email again

    expect(page.locator(".alert-danger")).to_contain_text("E-Mail Address is already registered!")  # Find the red warning box at the top
    expect(page).to_have_title(REGISTER_TITLE)  # Confirm that we are still on the same page and that no second account created


def test_f1_s3_password_mismatch(page: Page) -> None:
    # Scenario 3: the confirm password is different from the password
    submit_registration(page, confirm="Different@999")

    expect(page.locator(".text-danger")).to_have_text("Password confirmation does not match password!")  # Find the red warning box at the top under the confirm box
    expect(page).to_have_title(REGISTER_TITLE)  # Confirm that we are still on the same page and that no account created


def test_f1_s4_privacy_policy_not_ticked(page: Page) -> None:
    # Scenario 4: everything valid, but the Privacy Policy box is left unticked
    submit_registration(page, agree=False)

    expect(page.locator(".alert-danger")).to_contain_text("You must agree to the Privacy Policy!")  # Find the red warning box at the top
    expect(page).to_have_title(REGISTER_TITLE)  # Confirm that we are still on the same page and that no account created