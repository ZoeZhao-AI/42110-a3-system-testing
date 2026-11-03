import time
from playwright.sync_api import Page

BASE = "https://opencart.abstracta.us"
PASSWORD = "Test@12345"

def register_user(page: Page) -> str:
    email = f"tester{int(time.time() * 1000)}@example.com"
    page.goto(f"{BASE}/index.php?route=account/register")
    page.fill("#input-firstname", "Test")
    page.fill("#input-lastname", "User")
    page.fill("#input-email", email)
    page.fill("#input-telephone", "0400000000")
    page.fill("#input-password", PASSWORD)
    page.fill("#input-confirm", PASSWORD)
    page.check("input[name='agree']")
    page.click("input[value='Continue']")
    page.wait_for_url("**account/success**")
    return email

def logout(page: Page):
    page.goto(f"{BASE}/index.php?route=account/logout")

def login(page: Page, email: str, password: str = PASSWORD):
    page.goto(f"{BASE}/index.php?route=account/login")
    page.fill("#input-email", email)
    page.fill("#input-password", password)
    page.click("input[value='Login']")