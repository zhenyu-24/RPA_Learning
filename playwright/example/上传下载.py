import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(channel="msedge", headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://cdkm.com/cn/")

    # 监听文件选择器弹出
    with page.expect_file_chooser() as fc_info:
        page.get_by_role("button", name=" 选择文件").click()
    # 获取文件选择器并设置文件
    file_chooser = fc_info.value
    file_chooser.set_files([r'E:\code\PyQt-Fluent-Widgets\PyQt-Fluent-Widgets\README.md'])

    # 点击转换按钮
    page.get_by_label("目标格式：").select_option("pdf")
    page.get_by_role("button", name=" 开始转换").click()
    print('开始转换')

    # 下载1
    # expect(page.get_by_role("button", name="Download")).to_be_visible()
    # page.get_by_role("button", name="Download").click()

    # 下载2
    page.on("download", lambda download: print(download.path()))
    with page.expect_download() as download_info:
        # Perform the action that initiates download
        page.get_by_text("Download").click()
    download = download_info.value
    # Wait for the download process to complete and save the downloaded file somewhere
    download.save_as(r"E:\code\PyQt-Fluent-Widgets\PyQt-Fluent-Widgets\playwright\save" + download.suggested_filename)

    page.wait_for_timeout(30000)
    page.close()
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)