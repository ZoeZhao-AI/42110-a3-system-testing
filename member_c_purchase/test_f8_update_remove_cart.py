# F8 Update/Remove Cart Items - test cases for T008
# Tester: Zoe Ziying Zhao

from playwright.sync_api import Page, expect  # Page = a browser tab, expect = used to check results

BASE_URL = "https://opencart.abstracta.us/"  # home page of the website under test
MACBOOK_URL = BASE_URL + "index.php?route=product/product&product_id=43"  # MacBook product page (product id 43)
CART_URL = BASE_URL + "index.php?route=checkout/cart"  # shopping cart page


def add_macbook_and_open_cart(page: Page) -> None:
    # Helper (not a test): put one MacBook in the cart, then open the cart page
    # All three scenarios use this as their first step
    page.goto(MACBOOK_URL, wait_until="domcontentloaded", timeout=60000)  # open the MacBook product page
    page.get_by_role("button", name="Add to Cart").click()  # add one MacBook to the cart
    expect(page.locator("#cart-total")).to_contain_text("1 item(s)")  # wait until the cart button shows 1 item
    page.goto(CART_URL, wait_until="domcontentloaded", timeout=60000)  # open the shopping cart page


def test_f8_s1_update_quantity(page: Page) -> None:
    # Scenario 1: change the quantity from 1 to 3 and check the new total

    # Arrange: the cart has one MacBook
    add_macbook_and_open_cart(page)

    # Act: change the quantity from 1 to 3 and click the Update button
    page.locator("input[name^='quantity']").fill("3")  # type 3 in the quantity box of the MacBook row
    page.locator("#content .input-group button.btn-primary").click()  # click the blue Update button next to the quantity box

    # Assert: the cart is updated with the new quantity and the correct total
    expect(page.locator(".alert-success")).to_contain_text("You have modified your shopping cart")  # success message after updating
    expect(page.locator("input[name^='quantity']")).to_have_value("3")  # the quantity box now shows 3
    expect(page.locator("#content")).to_contain_text("$1,806.00")  # total = $602.00 x 3 = $1,806.00


def test_f8_s2_remove_product(page: Page) -> None:
    # Scenario 2: remove the product from the cart with the Remove button

    # Arrange: the cart has one MacBook
    add_macbook_and_open_cart(page)

    # Act: click the red Remove button
    page.locator("#content .input-group button.btn-danger").click()  # the red X button next to the quantity box

    # Assert: the cart becomes empty
    expect(page.locator("#content")).to_contain_text("Your shopping cart is empty!", timeout=15000)  # the page reloads after removing, so wait up to 15s
    expect(page.locator("#cart-total")).to_contain_text("0 item(s)")  # the cart button at the top shows 0 items


def test_f8_s3_update_quantity_to_zero(page: Page) -> None:
    # Scenario 3: change the quantity to 0 in the cart
    # Expected: the product is removed, because 0 in the cart means the user no longer wants it

    # Arrange: the cart has one MacBook
    add_macbook_and_open_cart(page)

    # Act: change the quantity to 0 and click the Update button
    page.locator("input[name^='quantity']").fill("0")  # type 0 in the quantity box
    page.locator("#content .input-group button.btn-primary").click()  # click the blue Update button

    # Assert: the product is removed and the cart becomes empty
    expect(page.locator("#content")).to_contain_text("Your shopping cart is empty!", timeout=15000)  # wait up to 15s for the page to reload
    expect(page.locator("#cart-total")).to_contain_text("0 item(s)")  # the cart button at the top shows 0 items
