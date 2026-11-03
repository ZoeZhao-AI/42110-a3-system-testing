from playwright.sync_api import Page, expect
from helpers import BASE, register_user, login, logout

def test_f1_registration(page: Page):
    register_user(page)
    expect(page.get_by_role("heading", name="Your Account Has Been Created!")).to_be_visible()