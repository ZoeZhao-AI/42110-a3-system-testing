from playwright.sync_api import Page, expect

def test_homepage_loads(page: Page):
    page.goto(
        "https://opencart.abstracta.us/",
        wait_until="domcontentloaded",
        timeout=60000,
    )
    expect(page).to_have_title("Your Store")
