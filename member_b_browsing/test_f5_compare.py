# F5 Product Compare - test cases for T005
# Tester: Quang Huy Vu

from playwright.sync_api import Page, expect  # expect = used to check results

from helpers import add_from_search, go

IPHONE = "iPhone"
IMAC = "iMac"
ATTRIBUTES = ["Price", "Model", "Brand", "Availability"]  # Some criteria shown for each product on the comparison page
FIVE_PRODUCTS = ["iPhone", "iMac", "MacBook Air", "MacBook Pro", "iPod Classic"]  # Five different products, added in this order
LIMIT = 4  # the most products the comparison page can hold


def names(page: Page):
    # the product names in the "Product" row of the table below the "Product Comparison" h1
    # (ignores the menu, the header and any other link in the table)
    return page.locator(
        '#content h1:text-is("Product Comparison") ~ table tr:has(td:text-is("Product")) a strong'
    )

# ----------------- Main test functions ------------------------------------

def test_f5_s1_two_products(page: Page) -> None:
    # Scenario 1: add the iPhone and the iMac, then open the comparison page
    add_from_search(page, IPHONE, "compare")  # add the iPhone
    add_from_search(page, IMAC, "compare")  # add the iMac
    go(page, "product/compare")  # Open the comparison page

    expect(page.get_by_role("heading", name="Product Comparison", exact=True)).to_be_visible()  # we are on the comparison page
    expect(names(page)).to_have_text([IPHONE, IMAC])  # Ensure that both products are shown side by side
    for label in ATTRIBUTES:
        expect(page.locator("#content table")).to_contain_text(label)  # and their attributes are listed


def test_f5_s2_remove_one(page: Page) -> None:
    # Scenario 2: Remove the iMac, only the iPhone should remain
    add_from_search(page, IPHONE, "compare")
    add_from_search(page, IMAC, "compare")
    go(page, "product/compare")
    expect(names(page)).to_have_count(2)  # wait until both products are shown

    column = names(page).all_inner_texts().index(IMAC)  # which column the iMac is in
    page.locator("#content table a.btn-danger").nth(column).click()  # click "Remove" under the iMac

    expect(page.locator(".alert-success")).to_contain_text("modified your product comparison")  # Ensure the green success box appears after the operation
    expect(names(page)).to_have_text([IPHONE])  # Ensure that only the iPhone is left
    expect(names(page).filter(has_text=IMAC)).to_have_count(0)  # and the iMac has been removed


def test_f5_s3_over_the_limit(page: Page) -> None:
    # Scenario 3: add five products, the page keeps only the newest four
    added = [add_from_search(page, term, "compare") for term in FIVE_PRODUCTS]  # Add the names of the five products, in the order added
    go(page, "product/compare")

    expect(names(page)).to_have_count(LIMIT)  # Make sure that at most four are shown
    expect(names(page)).to_have_text(added[1:])  # Ensure that the four products on the page are the last four added
    expect(names(page).filter(has_text=added[0])).to_have_count(0)  # Ensure that the first one added was dropped


def test_f5_s4_same_product_twice(page: Page) -> None:
    # Scenario 4: add the iPhone two times, it should be listed once
    add_from_search(page, IPHONE, "compare")  # first time
    add_from_search(page, IPHONE, "compare")  # second time
    go(page, "product/compare")

    expect(names(page)).to_have_count(1)  # ensure that the page only displays one column only
    expect(names(page)).to_have_text([IPHONE])  # and it is the iPhone
    expect(page.locator("#compare-total")).to_contain_text("(1)")  # the header counter says "Product Compare (1)"