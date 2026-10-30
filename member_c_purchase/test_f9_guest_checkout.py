# F9 Guest Checkout - test cases for T009
# Tester: Zoe Ziying Zhao

import re  # used to check that the page URL contains a certain word
from playwright.sync_api import Page, expect  # Page = a browser tab, expect = used to check results

BASE_URL = "https://opencart.abstracta.us/"  # home page of the website under test
IPHONE_URL = BASE_URL + "index.php?route=product/product&product_id=40"  # iPhone product page (MacBook is out of stock)
CHECKOUT_URL = BASE_URL + "index.php?route=checkout/checkout"  # checkout page


def wait_for_ajax(page: Page) -> None:
    # Helper: wait until the website has finished all background (AJAX) requests
    # Without this, the test clicked faster than the website could save each checkout step
    page.wait_for_function("() => window.jQuery && jQuery.active === 0")  # jQuery.active = number of requests still running


def start_guest_checkout(page: Page) -> None:
    # Helper: add an iPhone to the cart, open checkout, choose Guest Checkout
    page.goto(IPHONE_URL, wait_until="domcontentloaded", timeout=60000)  # open the iPhone product page
    page.get_by_role("button", name="Add to Cart", exact=True).click()  # exact=True so it does not click another product's button
    expect(page.locator("#cart-total")).to_contain_text("1 item(s)")  # wait until the iPhone is in the cart

    page.goto(CHECKOUT_URL, wait_until="domcontentloaded", timeout=60000)  # open the checkout page
    page.get_by_role("radio", name="Guest Checkout").check()  # Step 1: choose Guest Checkout (the default is Register Account)
    page.locator("#button-account").click()  # Step 1: click Continue
    wait_for_ajax(page)  # wait until Step 2 is loaded


def fill_billing_details(page: Page, email: str = "guest.tester@example.com") -> None:
    # Helper: fill in Step 2 Billing Details with test data
    # The e-mail can be changed when calling this function (Scenario 2 uses an empty e-mail)
    page.get_by_role("textbox", name="* First Name").fill("Test")  # required field
    page.get_by_role("textbox", name="* Last Name").fill("User")  # required field
    page.get_by_role("textbox", name="* E-Mail").fill(email)  # required field, uses the value passed in
    page.get_by_role("textbox", name="* Telephone").fill("0400000000")  # required field
    page.get_by_role("textbox", name="* Address").fill("1 Test Street")  # Address 1, required field
    page.get_by_role("textbox", name="* City").fill("Sydney")  # required field
    page.get_by_role("textbox", name="* Post Code").fill("2000")  # Post Code
    page.get_by_label("Country").select_option(label="Australia")  # choose the country from the drop-down list
    wait_for_ajax(page)  # wait until the website loads the list of Australian states
    page.get_by_label("Region / State").select_option(label="New South Wales")  # choose the state


def test_f9_s1_guest_checkout_success(page: Page) -> None:
    # Scenario 1: complete a guest checkout with valid data

    # Arrange: the cart has an iPhone and Guest Checkout is selected
    start_guest_checkout(page)

    # Act: fill in billing details and go through each checkout step
    fill_billing_details(page)  # use the default test data
    page.locator("#button-guest").click()  # Step 2: Billing Details, click Continue
    wait_for_ajax(page)  # wait until Step 4 is loaded (Step 3 is skipped because delivery address = billing address)
    page.locator("#button-shipping-method").click()  # Step 4: Delivery Method, keep the default and click Continue
    wait_for_ajax(page)  # wait until Step 5 is loaded
    page.locator("input[name='agree']").check()  # Step 5: tick "I have read and agree to the Terms & Conditions"
    page.locator("#button-payment-method").click()  # Step 5: Payment Method, click Continue
    wait_for_ajax(page)  # wait until Step 6 is loaded
    page.locator("#button-confirm").click()  # Step 6: click Confirm Order

    # Assert: the order is placed and the cart is now empty
    expect(page).to_have_url(re.compile("checkout/success"), timeout=15000)  # the page moves to the success page
    expect(page.locator("#content h1")).to_have_text("Your order has been placed!")  # the success heading is shown
    expect(page.locator("#cart-total")).to_contain_text("0 item(s)")  # the cart is cleared after the order


def test_f9_s2_missing_email(page: Page) -> None:
    # Scenario 2: leave the required E-Mail field empty

    # Arrange: the cart has an iPhone and Guest Checkout is selected
    start_guest_checkout(page)

    # Act: fill in all billing details except the e-mail, then click Continue
    fill_billing_details(page, email="")  # pass an empty e-mail
    page.locator("#button-guest").click()  # Step 2: click Continue
    wait_for_ajax(page)  # wait for the website to check the form

    # Assert: an e-mail error is shown and the checkout does not move to the next step
    expect(page.locator(".text-danger").first).to_be_visible()  # red error text is shown under a field
    expect(page.locator(".text-danger").first).to_contain_text("E-Mail")  # the error is about the e-mail field
    expect(page.locator("#button-shipping-method")).to_have_count(0)  # Step 4 is not loaded, so the user cannot continue


def test_f9_s3_terms_not_agreed(page: Page) -> None:
    # Scenario 3: do not tick the Terms & Conditions box
    # This is the same as Scenario 1, except the "agree" box is not ticked

    # Arrange: the cart has an iPhone and Guest Checkout is selected
    start_guest_checkout(page)

    # Act: complete the billing and delivery steps, but do NOT tick the Terms & Conditions box
    fill_billing_details(page)  # use the default test data
    page.locator("#button-guest").click()  # Step 2: Billing Details, click Continue
    wait_for_ajax(page)  # wait until Step 4 is loaded
    page.locator("#button-shipping-method").click()  # Step 4: Delivery Method, click Continue
    wait_for_ajax(page)  # wait until Step 5 is loaded
    page.locator("#button-payment-method").click()  # Step 5: click Continue without ticking the box
    wait_for_ajax(page)  # wait for the website to check the step

    # Assert: a warning about the Terms & Conditions is shown and the order cannot be confirmed
    warning = page.locator(".alert-danger")  # the red warning box
    expect(warning).to_be_visible()  # the warning is shown
    expect(warning).to_contain_text("Terms & Conditions")  # the warning is about the Terms & Conditions
    expect(page.locator("#button-confirm")).to_have_count(0)  # Step 6 is not loaded, so the order cannot be confirmed
