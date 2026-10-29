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


def test_f7_s2_add_same_product_twice(page: Page) -> None:
    # Arrange: open the MacBook product page
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=60000)
    page.get_by_role("link", name="MacBook").first.click()

    # Act: click Add to Cart two times
    add_button = page.get_by_role("button", name="Add to Cart")
    cart_total = page.locator("#cart-total")

    add_button.click()
    expect(cart_total).to_contain_text("1 item(s)")

    add_button.click()
    expect(cart_total).to_contain_text("2 item(s)")

    # Assert: the cart page shows MacBook once, with quantity 2
    page.goto(BASE_URL + "index.php?route=checkout/cart", wait_until="domcontentloaded", timeout=60000)
    quantity_box = page.locator("input[name^='quantity']")
    expect(quantity_box).to_have_count(1)
    expect(quantity_box).to_have_value("2")
