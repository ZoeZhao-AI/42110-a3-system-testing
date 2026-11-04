# F4 Product Search - test cases for T004
# Tester: Quang Huy Vu

import re

from playwright.sync_api import Page, expect  # expect = used to check results

from helpers import search

SEARCH_HEADING = "Search"  # the h2 directly above the results (the h1 is "Search - <term>" and below it are input parameters, so match this one exactly)
NO_MATCH = "Your shopping cart is empty!"  # The website's message when nothing is found (I don't know why this message is displayed but it is what is shown, so let's just use it)
DESCRIPTION_TEXT = "Intel Core 2 Duo"  # this text is only inside the MacBook's description (not in any product name), used to test the 'search in description' function


def results(page: Page):
    # The product names below the "Search" h2 heading (ignores the h1, the search boxes and the menu)
    # After this function, the test will search for product titles below this heading (which are the search results), not above it or anywhere else
    # We use this so that the test will not look for the search term anywhere else on the webpage (otherwise it may find the search term elsewhere, for example in h1 "Search - <term>")
    return page.locator(f'#content h2:text-is("{SEARCH_HEADING}") ~ .row .product-thumb h4 a')

# -------------------- Main test functions -------------------------------
def test_f4_s1_exact_name(page: Page) -> None:
    # Scenario 1: search for the exact product name "iPhone"
    search(page, "iPhone") # Run the search

    expect(page.get_by_role("heading", level=2, name=SEARCH_HEADING, exact=True)).to_be_visible()  # Find the results section on the page
    expect(results(page).filter(has_text="iPhone").first).to_be_visible()  # Ensure that a product with the title iPhone is listed under that heading


def test_f4_s2_no_match(page: Page) -> None:
    # Scenario 2: Search for a word that matches no product
    search(page, "600D")

    expect(page.locator("#content")).to_contain_text(NO_MATCH)  # Find the message that says nothing was found
    expect(page.locator(".product-thumb")).to_have_count(0)  # Ensure that no products are shown


def test_f4_s3_partial_keyword(page: Page) -> None:
    # Scenario 3: Search for part of a name, "mac"
    search(page, "mac")

    expect(results(page).filter(has_text="MacBook").first).to_be_visible()  # The MacBook family is listed
    expect(results(page).filter(has_text="iMac").first).to_be_visible()  # and the iMac too


def test_f4_s4_search_in_descriptions(page: Page) -> None:
    # Scenario 4: Search in product descriptions
    search(page, DESCRIPTION_TEXT)  # In the first search, we have the box unticked (default)
    expect(page.locator("#content")).to_contain_text(NO_MATCH)  # Ensure that no product NAME contains these words

    page.locator("#description").check()  # In the second search, tick "Search in product descriptions"
    page.locator("#button-search").click()  # Search again with the box ticked
    expect(results(page).filter(has_text="MacBook").first).to_be_visible()  # Ensure that now the MacBook is found (the one with Core 2 Duo in the description)

    page.locator("#description").uncheck()  # In the third search, we try unticking the box again
    page.locator("#button-search").click()  # search again with the box unticked
    expect(page.locator("#content")).to_contain_text(NO_MATCH)  # back to no match
    expect(page.locator(".product-thumb")).to_have_count(0)  # and no product box is shown

def test_f4_s5_search_in_category(page: Page) -> None:
    # Scenario 5: Search for products in a specific category only
    search(page, "iPhone")  # First search covers all categories

    page.locator("select[name='category_id']").select_option(label="Phones & PDAs")  # choose a category that contains the iPhone
    page.locator("#button-search").click()  # search again inside that category
    expect(page).to_have_url(re.compile(r"category_id=24"))  # wait until the new results page has loaded
    expect(results(page).filter(has_text="iPhone").first).to_be_visible()  # the iPhone is still listed

    page.locator("select[name='category_id']").select_option(label="Tablets")  # choose a category that does not contain the iPhone
    page.locator("#button-search").click()  # search again inside that category
    expect(page).to_have_url(re.compile(r"category_id=57"))  # wait until the new results page has loaded
    expect(page.locator("#content")).to_contain_text(NO_MATCH)  # Ensure that nothing is found
    expect(page.locator(".product-thumb")).to_have_count(0)  # And also ensure that no product box is shown

def test_f4_s6_search_in_subcategory(page: Page) -> None:
    # Scenario 6: a product that sits only in a subcategory is found only when "Search in subcategories" is ticked
    search(page, "iMac")  # first search covers all categories
    expect(page.locator("input[name='sub_category']")).to_be_disabled()  # the box cannot be used until a category is chosen

    page.locator("select[name='category_id']").select_option(value="20")  # Now we choose the parent category "Desktops"
    expect(page.locator("input[name='sub_category']")).to_be_enabled()  # Choosing a category switches the "Search in category" box on (not in "disabled" state anymore), ensure that happens but unticked
    page.locator("#button-search").click()  # Now we will click on the search button to perform the search inside Desktops
    expect(page).to_have_url(re.compile(r"category_id=20"))  # Wait until the new results page has loaded
    expect(page.locator("input[name='sub_category']")).not_to_be_checked()  # Make sure that the "Search in category" the box is unticked, so only Desktops itself is searched
    expect(page.locator("#content")).to_contain_text(NO_MATCH)  # the iMac is not directly in Desktops
    expect(page.locator(".product-thumb")).to_have_count(0)  # and no product is shown in the results area

    page.locator("input[name='sub_category']").check()  # Now we try to search in subcategories by ticking "Search in subcategories"
    page.locator("#button-search").click()  # Search again, now including the Mac subcategory
    expect(page).to_have_url(re.compile(r"sub_category=true"))  # wait until the new results page has loaded
    expect(page.locator("input[name='sub_category']")).to_be_checked()  # Now we tick the "Search in subcategories" box, so the Mac subcategory is included
    expect(results(page).filter(has_text="iMac").first).to_be_visible()  # the iMac is found in the Mac subcategory

