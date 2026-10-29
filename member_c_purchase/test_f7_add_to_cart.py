from playwright.sync_api import Page, expect

BASE_URL = "https://opencart.abstracta.us/"


def test_f7_s1_add_single_product(page: Page) -> None:
    # Arrange: open the home page
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=60000)

    # Act: open the MacBook product page and click Add to Cart
    page.get_by_role("link", name="MacBook").first.click()
    page.get_by_role("button", name="Add to Cart").click()

    # Assert: a success message appears and mentions MacBook
    success_alert = page.locator(".alert-success")
    expect(success_alert).to_be_visible()
    expect(success_alert).to_contain_text("You have added MacBook to your shopping cart")
