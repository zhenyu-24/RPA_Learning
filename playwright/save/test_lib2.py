import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(channel="msedge", headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.baidu.com/")
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="百度热搜").locator("img").click()
    page1 = page1_info.value
    page1.get_by_role("link", name="更多").nth(1).click()
    with page1.expect_popup() as page2_info:
        page1.get_by_role("link", name="习近平总书记海南广东之行纪实").click()
    page2 = page2_info.value
    with page2.expect_popup() as page3_info:
        page2.get_by_role("link", name="习近平总书记海南广东之行纪实", exact=True).click()
    page3 = page3_info.value
    page3.close()
    page2.close()
    page1.close()
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
