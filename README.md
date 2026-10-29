# 42110 Assessment Task 3 - System Testing

Automated tests for the OpenCart demo website: https://opencart.abstracta.us/
(The original LambdaTest site is down, so we use the alternative site from the TA's announcement on Canvas.)

## Tools
- Python 3.12
- pytest
- Playwright (Chromium)

## Setup (macOS)
1. Clone this repo and go into the folder:
   git clone <repo link>
   cd a3-system-testing
2. Create and activate a virtual environment:
   python3 -m venv venv
   source venv/bin/activate
3. Install the packages:
   pip install -r requirements.txt
4. Install the browser for Playwright:
   playwright install chromium
5. Run the smoke test to check everything works:
   python -m pytest test_smoke.py --headed

On Windows, use `python` instead of `python3`, and activate the virtual environment with `venv\Scripts\activate`.

Note: please use `python -m pytest` instead of `pytest`, otherwise the Playwright plugin may not load.

## Folders
- member_a_account/  : F1 Registration, F2 Login, F3 Edit Account / Change Password
- member_b_browsing/ : F4 Product Search, F5 Product Compare, F6 Wishlist
- member_c_purchase/ : F7 Add to Cart, F8 Update/Remove Cart Items, F9 Guest Checkout

Each member puts their own test files in their folder.
