# F6 Wish List - test cases for T006
# Tester: Quang Huy Vu

from playwright.sync_api import Page, expect  # expect = used to check results

from helpers import PASSWORD, add_from_search, go, login, logout, register_user

IPHONE = "iPhone"
WISHLIST_TITLE = "My Wish List"  # the tab title of the wish list page
LOGIN_TITLE = "Account Login"  # the tab title of the login page
MUST_LOGIN = "You must login or create an account"  # the message a guest gets
MODIFIED = "modified your wish list"  # part of the success message after removing
EMPTY = "Your wish list is empty."  # message shown when nothing is saved


def names(page: Page):
    # the product names on the wish list page (the "Product Name" column)
    return page.locator("#content table td.text-left a")


def test_f6_s1_add_while_logged_in(page: Page) -> None:
    # Scenario 1: a logged-in user adds the iPhone and finds it on the wish list
    register_user(page)  # create an account (this also logs in)
    name = add_from_search(page, "iphone", "wishlist")  # click the heart on the first search result
    go(page, "account/wishlist")  # open the wish list

    expect(page).to_have_title(WISHLIST_TITLE)  # we are on the wish list page
    expect(names(page)).to_have_text([name])  # the product is listed, and it is the only one
    expect(names(page)).to_have_text([IPHONE])  # and it is the iPhone


def test_f6_s2_guest_adds(page: Page) -> None:
    # Scenario 2: a guest tries to add the iPhone
    add_from_search(page, "iphone", "wishlist")  # nobody is logged in

    expect(page.locator(".alert")).to_contain_text(MUST_LOGIN)  # the site asks the guest to log in or register

    go(page, "account/wishlist")  # try to open the wish list as a guest
    expect(page).to_have_title(LOGIN_TITLE)  # redirected to the login page, nothing was saved


def test_f6_s3_remove_product(page: Page) -> None:
    # Scenario 3: remove the only product from the wish list
    register_user(page)
    add_from_search(page, "iphone", "wishlist")
    go(page, "account/wishlist")
    expect(names(page)).to_have_count(1)  # wait until the iPhone is listed

    page.locator("#content table a.btn-danger").click()  # the red "Remove" button

    expect(page.locator(".alert-success")).to_contain_text(MODIFIED)  # green success box
    expect(page.locator("#content")).to_contain_text(EMPTY)  # the empty-list message
    expect(names(page)).to_have_count(0)  # and no product rows are left


def test_f6_s4_persistence(page: Page) -> None:
    # Scenario 4: the wish list is still there after logging out and back in
    email = register_user(page)
    name = add_from_search(page, "iphone", "wishlist")

    logout(page)  # end the session
    login(page, email, PASSWORD)  # a real login with the same account
    go(page, "account/wishlist")

    expect(names(page)).to_have_text([name])  # the product is still listed