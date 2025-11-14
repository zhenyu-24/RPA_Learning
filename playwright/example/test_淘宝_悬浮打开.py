import re
from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(channel="msedge", headless=False)
    context = browser.new_context(storage_state="taobao")
    page = context.new_page()
    page.goto("https://www.taobao.com/")
    # 关闭可能的弹窗
    try:
        page.get_by_label("关闭").locator("img").click(timeout=5000)
    except:
        print("没有找到关闭弹窗或已关闭")
    # 第一步：鼠标悬浮在"电脑"分类上
    print("正在悬浮在'电脑'分类上...")
    computer_link = page.locator("#ice-container").get_by_role("link", name="电脑", exact=True)
    computer_link.hover()
    page.wait_for_timeout(2000)  # 等待下拉菜单出现
    # 第二步：点击出现的"DIY电脑"链接
    print("正在点击'DIY电脑'...")
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="DIY电脑").click()
    page1 = page1_info.value
    print("成功打开DIY电脑页面")
    # 等待新页面加载
    page1.wait_for_load_state("networkidle")
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
