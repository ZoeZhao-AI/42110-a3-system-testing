# F1 User Registration - test cases for T001
# Tester: Quang Huy Vu

from playwright.sync_api import Page, expect  # expect = used to check results

from shared_helpers import go, logout, register_user, submit_registration


def test_f1_s1_valid_registration(page: Page) -> None:
    # Scenario 1: register with valid details and check the account is created
    submit_registration(page)  # fill in the form and click Continue

    expect(page.get_by_role("heading", name="Your Account Has Been Created!")).to_be_visible()  # success page
    go(page, "account/account")  # open My Account
    expect(page.get_by_role("heading", name="My Account", exact=True)).to_be_visible()  # logged in, not sent to login


def test_f1_s2_duplicate_email(page: Page) -> None:
    # Scenario 2: register again with an email that is already registered
    email = register_user(page)  # first registration (also logs in)
    logout(page)
    submit_registration(page, email=email)  # same email again

    expect(page.locator(".alert-danger")).to_contain_text("already registered")  # red warning box at the top


def test_f1_s3_password_mismatch(page: Page) -> None:
    # Scenario 3: the confirm password is different from the password
    submit_registration(page, confirm="Different@999")

    expect(page.locator("#content")).to_contain_text("Password confirmation does not match password!")  # error under the confirm box
    expect(page.get_by_role("heading", name="Your Account Has Been Created!")).to_have_count(0)  # no account created


def test_f1_s4_privacy_policy_not_ticked(page: Page) -> None:
    # Scenario 4: everything valid, but the Privacy Policy box is left unticked
    submit_registration(page, agree=False)

    expect(page.locator(".alert-danger")).to_contain_text("You must agree to the Privacy Policy!")  # red warning box at the top
    expect(page.get_by_role("heading", name="Your Account Has Been Created!")).to_have_count(0)  # no account created