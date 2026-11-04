# F4 Product Search - test cases for T004
# Tester: Quang Huy Vu

from playwright.sync_api import Page, expect  # expect = used to check results

from helpers import go, search

SEARCH_HEADING = "Search"  # the h2 above the results (the h1 is "Search - <term>", so match this one exactly)
NO_MATCH = "Your shopping cart is empty!"  # the website's message when nothing is found
DESCRIPTION_TEXT = "Intel Core 2 Duo"  # this text is only inside the MacBook's description, not in any product name


def results(page: Page):
    # the product names below the "Search" h2 heading (ignores the h1, the search boxes and the menu)
    return page.locator(f'#content h2:text-is("{SEARCH_HEADING}") ~ .row .product-thumb h4 a')

# -------------------- Main test functions -------------------------------
def test_f4_s1_exact_name(page: Page) -> None:
    # Scenario 1: search for the exact product name "iPhone"
    search(page, "iPhone")

    expect(page.get_by_role("heading", level=2, name=SEARCH_HEADING, exact=True)).to_be_visible()  # the results section is shown
    expect(results(page).filter(has_text="iPhone").first).to_be_visible()  # the iPhone is listed under that heading


def test_f4_s2_no_match(page: Page) -> None:
    # Scenario 2: search for a word that matches no product
    search(page, "600D")

    expect(page.locator("#content")).to_contain_text(NO_MATCH)  # the website says nothing was found
    expect(page.locator(".product-thumb")).to_have_count(0)  # and no product box is shown


def test_f4_s3_partial_keyword(page: Page) -> None:
    # Scenario 3: search for part of a name, "mac"
    search(page, "mac")

    expect(results(page).filter(has_text="MacBook").first).to_be_visible()  # the MacBook family is listed
    expect(results(page).filter(has_text="iMac").first).to_be_visible()  # and the iMac too


def test_f4_s4_search_in_descriptions(page: Page) -> None:
    # Scenario 4: the same words are found only when "Search in product descriptions" is ticked
    search(page, DESCRIPTION_TEXT)  # first search has the box unticked (default)
    expect(page.locator("#content")).to_contain_text(NO_MATCH)  # no product NAME contains these words

    page.locator("#description").check()  # tick "Search in product descriptions"
    page.locator("#button-search").click()  # search again with the box ticked
    expect(results(page).filter(has_text="MacBook").first).to_be_visible()  # now the MacBook is found

    page.locator("#description").uncheck()  # untick the box again
    page.locator("#button-search").click()  # search again with the box unticked
    expect(page.locator("#content")).to_contain_text(NO_MATCH)  # back to no match
    expect(page.locator(".product-thumb")).to_have_count(0)  # and no product box is shown