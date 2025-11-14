import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://www.baidu.com/")
    page.locator("#hotsearch-refresh-btn").click()
    page.locator("#hotsearch-refresh-btn").click()
    page.locator("#hotsearch-refresh-btn").click()
    page.get_by_role("textbox").click()
    page.get_by_role("textbox").fill("周杰伦")
    page.get_by_role("button", name="百度一下").click()
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="周杰伦", exact=True).click()
    page1 = page1_info.value
    with page1.expect_popup() as page2_info:
        page1.get_by_role("link", name="青花瓷").first.click()
    page2 = page2_info.value
    with page2.expect_popup() as page3_info:
        page2.get_by_role("definition").filter(has_text="钟兴民").get_by_role("link").click()
    page3 = page3_info.value
