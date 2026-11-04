# F6 Wish List - test cases for T006
# Tester: Quang Huy Vu

from playwright.sync_api import Page, expect  # expect = used to check results

from helpers import PASSWORD, add_product, go, login, logout, register_user

IPHONE = "iPhone"
WISHLIST_TITLE = "My Wish List"  # the tab title of the wish list page
LOGIN_TITLE = "Account Login"  # the tab title of the login page
MUST_LOGIN = "You must login or create an account"  # the message a guest gets
MODIFIED = "modified your wish list"  # part of the success message after removing
EMPTY = "is empty"  # message shown when nothing is saved


def names(page: Page):
    # the product names in the "Product Name" column of the wish list table
    # (ignores the menu, the header, and the image link in the first column)
    return page.locator(
        '#content table:has(thead td:text-is("Product Name")) tbody td:nth-child(2) a'
    )

# ----------------- Main test functions ------------------------------------

def test_f6_s1_add_while_logged_in(page: Page) -> None:
    # Scenario 1: a logged-in user adds the iPhone and finds it on the wish list
    register_user(page)  # create an account (this also logs in)
    add_product(page, IPHONE, "wishlist")  # click the heart on the box named exactly "iPhone"
    go(page, "account/wishlist")  # open the wish list

    expect(page).to_have_title(WISHLIST_TITLE)  # Ensure that we are on the wish list page by verifying its title
    expect(page.locator(".breadcrumb li:last-child")).to_have_text("My Wish List")  # the breadcrumb ends with "My Wish List"
    expect(names(page)).to_have_text([IPHONE])  # Ensure that exactly one product is listed, and it is the iPhone


def test_f6_s2_guest_adds(page: Page) -> None:
    # Scenario 2: A guest tries to add the iPhone to the wishlist
    add_product(page, IPHONE, "wishlist")  # Add a product to the wishlist without logging in

    expect(page.locator(".alert")).to_contain_text(MUST_LOGIN)  # the site will display an alert at the top of the page asking the guest to log in or register

    go(page, "account/wishlist")  # The guest tries to open the wish list as a gues
    expect(page).to_have_title(LOGIN_TITLE)  # The website should redirect the guest to the login page, and nothing should be saved


def test_f6_s3_remove_product(page: Page) -> None:
    # Scenario 3: Remove the only product from the wish list
    register_user(page)
    add_product(page, IPHONE, "wishlist")
    go(page, "account/wishlist")
    expect(names(page)).to_have_text([IPHONE])  # Wait until the iPhone is listed in the wish list properly

    page.locator("#content table a.btn-danger").click()  # Look for the red "Remove" button

    expect(page.locator(".alert-success")).to_contain_text(MODIFIED)  # green success box
    expect(page.locator("#content")).to_contain_text(EMPTY)  # the empty-list message
    expect(names(page)).to_have_count(0)  # and no product rows are left


def test_f6_s4_persistence(page: Page) -> None:
    # Scenario 4: The wish list should be saved after the user logs out and and then logs back in
    email = register_user(page)
    add_product(page, IPHONE, "wishlist")

    logout(page)  # end the session
    login(page, email, PASSWORD)  # a real login with the same account
    go(page, "account/wishlist")

    expect(names(page)).to_have_text([IPHONE])  # Ensure that the iPhone is still listed