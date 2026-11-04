import os, pytest

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "ignore_https_errors": True}

@pytest.fixture(autouse=True)
def slow_site_timeouts(page):
    page.set_default_timeout(60000)
    page.set_default_navigation_timeout(60000)

@pytest.fixture(autouse=True)
def pause_after_test(page):
    yield
    if os.getenv("PAUSE"):
        page.pause()