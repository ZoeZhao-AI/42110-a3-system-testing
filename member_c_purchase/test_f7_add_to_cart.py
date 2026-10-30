# F7 Add to Cart - test cases for T007
# Tester: Zoe Ziying Zhao

from playwright.sync_api import Page, expect  # Page = a browser tab, expect = used to check results

BASE_URL = "https://opencart.abstracta.us/"  # home page of the website under test


def test_f7_s1_add_single_product(page: Page) -> None:
    # Scenario 1: add one MacBook to the cart and check the success message

    # Arrange: open the home page
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=60000)  # wait until the main page content is loaded (max 60s)

    # Act: open the MacBook product page and click Add to Cart
    page.get_by_role("link", name="MacBook").first.click()  # click the first link named "MacBook" to open its product page
    page.get_by_role("button", name="Add to Cart").click()  # click the Add to Cart button (default quantity is 1)

    # Assert: a success message appears and mentions MacBook
    success_alert = page.locator(".alert-success")  # the green success message box at the top of the page
    expect(success_alert).to_be_visible()  # check that the success message is shown
    expect(success_alert).to_contain_text("You have added MacBook to your shopping cart")  # check that it names the right product


def test_f7_s2_add_same_product_twice(page: Page) -> None:
    # Scenario 2: add the same product twice and check that the cart shows one row with quantity 2

    # Arrange: open the MacBook product page
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=60000)  # open the home page
    page.get_by_role("link", name="MacBook").first.click()  # open the MacBook product page

    # Act: click Add to Cart two times
    add_button = page.get_by_role("button", name="Add to Cart")  # save the Add to Cart button so it can be used twice
    cart_total = page.locator("#cart-total")  # the black cart button at the top right, e.g. "1 item(s) - $602.00"

    add_button.click()  # first click
    expect(cart_total).to_contain_text("1 item(s)")  # wait until the first item is added before clicking again

    add_button.click()  # second click
    expect(cart_total).to_contain_text("2 item(s)")  # check that the cart now has 2 items

    # Assert: the cart page shows MacBook once, with quantity 2
    page.goto(BASE_URL + "index.php?route=checkout/cart", wait_until="domcontentloaded", timeout=60000)  # open the shopping cart page
    quantity_box = page.locator("input[name^='quantity']")  # quantity boxes in the cart (one box for each product row)
    expect(quantity_box).to_have_count(1)  # only one row, so MacBook is not listed twice
    expect(quantity_box).to_have_value("2")  # the quantity in that row is 2


def test_f7_s3_add_with_zero_quantity(page: Page) -> None:
    # Scenario 3: try to add a product with quantity 0 (invalid input)
    # Expected: an error is shown and nothing is added to the cart

    # Arrange: open the MacBook product page
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=60000)  # open the home page
    page.get_by_role("link", name="MacBook").first.click()  # open the MacBook product page

    # Act: change the quantity to 0 and click Add to Cart
    page.locator("#input-quantity").fill("0")  # clear the Qty box and type 0
    page.get_by_role("button", name="Add to Cart").click()  # click Add to Cart

    # Wait until the website shows some kind of message
    page.locator(".alert, .text-danger").first.wait_for()  # wait for any message box or red error text to appear

    # Assert 1: an error message is shown
    expect(page.locator(".alert-danger, .text-danger").first).to_be_visible()  # red error box or red error text should be visible

    # Assert 2: no success message is shown
    expect(page.locator(".alert-success")).to_have_count(0)  # the green success box should not appear

    # Assert 3: the shopping cart is still empty
    page.goto(BASE_URL + "index.php?route=checkout/cart", wait_until="domcontentloaded", timeout=60000)  # open the shopping cart page
    expect(page.locator("#content")).to_contain_text("Your shopping cart is empty!")  # the cart should have no products
