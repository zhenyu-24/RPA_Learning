from playwright.sync_api import sync_playwright

# 1.启动 playwright driver 进程
p = sync_playwright().start()

# 2.启动浏览器，返回 Browser 类型对象
browser = p.chromium.launch(headless=False,
                            executable_path=r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')

# 3.创建新页面，返回 Page 类型对象
page = browser.new_page()
page.goto("https://www.byhy.net/cdn2/files/selenium/stock1.html")
print(page.title()) # 打印网页标题栏

# 4.输入通讯，点击查询。这是定位与操作，是自动化重点，后文详细讲解
page.locator('#kw').fill('通讯')  # 输入通讯
page.locator('#go').click()      # 点击查询

# 等待1秒，等待页面加载完成
page.wait_for_timeout(1000)
# 5.打印所有搜索内容
lcs = page.locator(".result-item").all()
for lc in lcs:
    print(lc.inner_text())

# 6.关闭浏览器
browser.close()
input('4....')
# 7.关闭 playwright driver 进程
p.stop()