# Helper functions reused by the F1 to F6 tests

import time  # used to make a new email address every run
from typing import Optional  # lets older Python versions accept "str or None"

from playwright.sync_api import Page  # Page = a browser tab

BASE_URL = "https://opencart.abstracta.us/"  # home page of the website under test
PASSWORD = "Test@12345"  # default password for every test account to be created

# the website's address (and the button prefix) for each "add" action
ADD_ACTIONS = {
    "compare": "product/compare/add",
    "wishlist": "account/wishlist/add",
}


def go(page: Page, route: str) -> None:
    # open a page of the website, e.g. go(page, "account/login")
    page.goto(f"{BASE_URL}index.php?route={route}", wait_until="domcontentloaded", timeout=60000)


def unique_email() -> str:
    # generate a new email with a random number on every run to avoid the "already registered" errors
    return f"tester{int(time.time() * 1000)}@example.com"


def submit_registration(page: Page, agree: bool = True, **overrides) -> dict:
    # fill in the registration form with valid details and click Continue
    # to test bad input, override a field: submit_registration(page, confirm="Different@999")
    # use agree=False to leave the Privacy Policy box unticked
    data = {
        "firstname": "Test",
        "lastname": "User",
        "email": unique_email(),
        "telephone": "0400000000",
        "password": PASSWORD,
        "confirm": PASSWORD,
    }
    data.update(overrides)  # replace any field the test wants to change

    go(page, "account/register")
    for field, value in data.items():
        page.locator(f"#input-{field}").fill(value)  # the form boxes are named #input-firstname, #input-email, ...
    if agree:
        page.locator("input[name='agree']").check()  # tick the Privacy Policy box
    page.locator("input[name='agree']").evaluate("el => el.form.noValidate = true")  # so the website's own error messages are tested
    page.locator("input[value='Continue']").click()
    return data  # the details used, e.g. data["email"]


def register_user(page: Page) -> str:
    # register a valid new user (this also logs them in) and return the email
    data = submit_registration(page)
    page.wait_for_url("**account/success**")  # wait for the success page
    return data["email"]


def logout(page: Page) -> None:
    go(page, "account/logout")


def login(page: Page, email: str, password: str = PASSWORD) -> None:
    go(page, "account/login")
    page.locator("#input-email").fill(email)
    page.locator("#input-password").fill(password)
    page.locator("input[value='Login']").click()


def search(page: Page, term: str) -> None:
    # type a word in the search box on the home page and click the search button
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=60000)
    page.locator("input[name='search']").fill(term)
    page.locator("#search button").click()


def add_from_search(page: Page, term: str, action: str, index: int = 0, pick: Optional[str] = None) -> str:
    # search for a word, click "compare" or "wishlist" on one result and return that product's name
    # by default the result is chosen by position (`index`), e.g. add_from_search(page, "mac", "compare")
    # to choose by name instead, pass pick, e.g. add_from_search(page, "iphone", "wishlist", pick="iPhone")
    go(page, f"product/search&search={term}")
    cards = page.locator(".product-thumb")  # one product box per search result
    if pick:
        # keep only the box whose product name is exactly `pick` (no "MacBook Air" when asking for "MacBook")
        card = cards.filter(has=page.get_by_role("link", name=pick, exact=True)).first
    else:
        card = cards.nth(index)
    name = card.locator("h4 a").inner_text().strip()
    with page.expect_response(lambda r: ADD_ACTIONS[action] in r.url):  # wait until the website has saved it
        card.locator(f"button[onclick^='{action}.add']").click()
    return name


def add_product(page: Page, name: str, action: str) -> str:
    # search for a product by its exact name and click "compare" or "wishlist" on the box with that name
    # e.g. add_product(page, "iPhone", "wishlist")
    return add_from_search(page, name, action, pick=name)