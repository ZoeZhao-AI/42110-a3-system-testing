from playwright.sync_api import Page, expect

BASE_URL = "https://opencart.abstracta.us/"
MACBOOK_URL = BASE_URL + "index.php?route=product/product&product_id=43"
CART_URL = BASE_URL + "index.php?route=checkout/cart"


def add_macbook_and_open_cart(page: Page) -> None:
    # Helper: put one MacBook in the cart, then open the cart page
    page.goto(MACBOOK_URL, wait_until="domcontentloaded", timeout=60000)
    page.get_by_role("button", name="Add to Cart").click()
    expect(page.locator("#cart-total")).to_contain_text("1 item(s)")
    page.goto(CART_URL, wait_until="domcontentloaded", timeout=60000)


def test_f8_s1_update_quantity(page: Page) -> None:
    # Arrange: the cart has one MacBook
    add_macbook_and_open_cart(page)

    # Act: change the quantity from 1 to 3 and click the Update button
    page.locator("input[name^='quantity']").fill("3")
    page.locator("#content .input-group button.btn-primary").click()

    # Assert: the cart is updated with the new quantity and the correct total
    expect(page.locator(".alert-success")).to_contain_text("You have modified your shopping cart")
    expect(page.locator("input[name^='quantity']")).to_have_value("3")
    expect(page.locator("#content")).to_contain_text("$1,806.00")


def test_f8_s2_remove_product(page: Page) -> None:
    # Arrange: the cart has one MacBook
    add_macbook_and_open_cart(page)

    # Act: click the red Remove button
    page.locator("#content .input-group button.btn-danger").click()

    # Assert: the cart becomes empty
    expect(page.locator("#content")).to_contain_text("Your shopping cart is empty!", timeout=15000)
    expect(page.locator("#cart-total")).to_contain_text("0 item(s)")
