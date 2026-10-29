import re
from playwright.sync_api import Page, expect

BASE_URL = "https://opencart.abstracta.us/"
IPHONE_URL = BASE_URL + "index.php?route=product/product&product_id=40"
CHECKOUT_URL = BASE_URL + "index.php?route=checkout/checkout"


def wait_for_ajax(page: Page) -> None:
    # Helper: wait until the website has finished all background (AJAX) requests
    page.wait_for_function("() => window.jQuery && jQuery.active === 0")


def start_guest_checkout(page: Page) -> None:
    # Helper: add an iPhone to the cart, open checkout, choose Guest Checkout
    page.goto(IPHONE_URL, wait_until="domcontentloaded", timeout=60000)
    page.get_by_role("button", name="Add to Cart", exact=True).click()
    expect(page.locator("#cart-total")).to_contain_text("1 item(s)")

    page.goto(CHECKOUT_URL, wait_until="domcontentloaded", timeout=60000)
    page.get_by_role("radio", name="Guest Checkout").check()
    page.locator("#button-account").click()
    wait_for_ajax(page)


def fill_billing_details(page: Page, email: str = "guest.tester@example.com") -> None:
    # Helper: fill in Step 2 Billing Details with test data
    page.get_by_role("textbox", name="* First Name").fill("Test")
    page.get_by_role("textbox", name="* Last Name").fill("User")
    page.get_by_role("textbox", name="* E-Mail").fill(email)
    page.get_by_role("textbox", name="* Telephone").fill("0400000000")
    page.get_by_role("textbox", name="* Address").fill("1 Test Street")
    page.get_by_role("textbox", name="* City").fill("Sydney")
    page.get_by_role("textbox", name="* Post Code").fill("2000")
    page.get_by_label("Country").select_option(label="Australia")
    wait_for_ajax(page)
    page.get_by_label("Region / State").select_option(label="New South Wales")


def test_f9_s1_guest_checkout_success(page: Page) -> None:
    # Arrange: the cart has an iPhone and Guest Checkout is selected
    start_guest_checkout(page)

    # Act: fill in billing details and go through each checkout step
    fill_billing_details(page)
    page.locator("#button-guest").click()               # Step 2: Billing Details
    wait_for_ajax(page)
    page.locator("#button-shipping-method").click()     # Step 4: Delivery Method
    wait_for_ajax(page)
    page.locator("input[name='agree']").check()         # Step 5: agree to Terms & Conditions
    page.locator("#button-payment-method").click()      # Step 5: Payment Method
    wait_for_ajax(page)
    page.locator("#button-confirm").click()             # Step 6: Confirm Order

    # Assert: the order is placed and the cart is now empty
    expect(page).to_have_url(re.compile("checkout/success"), timeout=15000)
    expect(page.locator("#content h1")).to_have_text("Your order has been placed!")
    expect(page.locator("#cart-total")).to_contain_text("0 item(s)")
