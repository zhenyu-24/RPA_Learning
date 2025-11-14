import re
import time
from typing import Optional, Dict, Any
from playwright.sync_api import Page, Browser, BrowserContext, sync_playwright

class BaseBrowser:
    """浏览器基础管理类"""
    def __init__(self, config: Dict[str, Any], logger,
                 browser: Optional[Browser] = None,
                 context: Optional[BrowserContext] = None,
                 page: Optional[Page] = None):
        self.config = config
        self.logger = logger
        self.page_tags: Dict[str, Page] = {}  # 页面标签映射
        self._playwright = None

        # 如果提供了完整的浏览器实例，则直接使用
        if all([browser, context, page]):
            self.browser = browser
            self.context = context
            self.page = page
            self.page_tags['default'] = page

    def __getattr__(self, item):
        """延迟初始化浏览器属性"""
        if item in ["browser", "context", "page"]:
            self.logger.info(f"浏览器未初始化，正在启动浏览器...")
            self.open_browser(self.config.get("browser_type", "chromium"))
            return getattr(self, item)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")

    def open_browser(self, browser_type: str = "chromium", headless: bool = False, channel='msedge'):
        """启动浏览器"""
        try:
            browser_type = browser_type.lower() or self.config.get("browser_type", "chromium").lower()
            self.browser, self.context, self.page = self.create_browser(
                browser_type,
                headless=headless or self.config.get("headless", False),  # 默认非headless便于观察
                channel=channel, # 默认使用msedge浏览器
            )
            self.page_tags['default'] = self.page  # 标记默认页面
            self.logger.info(f"启动浏览器成功，浏览器类型：{browser_type}")
        except Exception as e:
            self.logger.error(f"启动浏览器失败: {e}")
            raise

    def create_browser(self, browser_type: str, headless: bool = False, channel='msedge'):
        """创建浏览器实例"""
        self._playwright = sync_playwright().start()
        browser_launcher = getattr(self._playwright, browser_type)
        browser = browser_launcher.launch(
            headless=headless,
            channel=channel,
            args=self.config.get("browser_args", [])
        )
        context = browser.new_context()
        page = context.new_page()
        return browser, context, page

    def reset_browser(self):
        """重置浏览器上下文"""
        if hasattr(self, 'context'):
            self.context.close()
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.page_tags = {'default': self.page}

    def close(self):
        """关闭浏览器和Playwright"""
        if hasattr(self, 'context'):
            self.context.close()
        if hasattr(self, 'browser'):
            self.browser.close()
        if self._playwright:
            self._playwright.stop()
        self.page_tags.clear()

    def open_new_page(self, tag: str) -> Page:
        """打开新页面"""
        if tag in self.page_tags:
            self.logger.warning(f"页面标签'{tag}'已存在")
            return self.page_tags[tag]
        new_page = self.context.new_page()
        self.page_tags[tag] = new_page
        self.logger.info(f"新页面'{tag}'创建成功")
        return new_page

    def find_page(self, tag: str = None, index: int = None,
                  title: str = None, url: str = None) -> Optional[Page]:
        """查找页面"""
        # 优先通过标签查找
        if tag:
            return self.page_tags.get(tag)
        # 然后通过其他条件查找
        elif index is not None:
            pages = self.context.pages
            return pages[index] if 0 <= index < len(pages) else None
        elif title:
            for page in self.context.pages:
                if title in page.title():
                    return page
        elif url:
            for page in self.context.pages:
                if re.search(url, page.url):
                    return page
        else:
            self.logger.info("未指定查找条件，返回默认页面")
            return self.page
        return None

    def switch_page(self, tag: str = None, index: int = None,
                    title: str = None, url: str = None) -> Optional[Page]:
        """切换当前页面"""
        page = self.find_page(tag, index, title, url)
        if page:
            page.bring_to_front()  # 关键：将页面带到前台
            self.page = page
            self.logger.info(f"已切换到页面: {tag or title or url}")
            return page
        else:
            self.logger.error("未找到指定页面")
            return None

    def get_page_info(self, page: Page = None) -> Dict[str, str]:
        """获取页面信息"""
        if page is None:
            page = self.page
        return {
            "title": page.title(),
            "url": page.url,
            "page_id": str(id(page))
        }

    def list_all_pages(self):
        """列出所有页面信息"""
        pages_info = []
        for i, page in enumerate(self.context.pages):
            info = self.get_page_info(page)
            info['index'] = i
            # 查找对应的tag
            for tag, p in self.page_tags.items():
                if p == page:
                    info['tag'] = tag
                    break
            else:
                info['tag'] = '未命名'
            pages_info.append(info)
        return pages_info

    def __enter__(self):
        """支持上下文管理器"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出时自动关闭"""
        self.close()

class PageMixin(BaseBrowser):
    """页面操作混入类"""
    def goto(self, url: str, wait_until='load', timeout=30000):
        """访问URL"""
        # 先判断url是否为完整地址
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        self.page.goto(url, wait_until=wait_until, timeout=timeout)
        self.logger.info(f"访问URL: {url}")

    def close_page(self, tag: str = None, index: int = None,
                   title: str = None, url: str = None) -> bool:
        """关闭指定页面"""
        page = self.find_page(tag, index, title, url)
        if page and len(self.context.pages) > 1:
            # 先移除page_tags中的映射，再关闭页面
            for t, p in list(self.page_tags.items()):
                if p == page:
                    del self.page_tags[t]
                    break
            page.close()
            self.page = self.context.pages[0]  # 切换到第一个页面
            self.logger.info(f"已关闭页面: {tag or title or url}")
            return True
        elif page:
            self.logger.warning("关闭最后一个页面")
            page.close()
            self.page_tags.clear()
            self.page = None
        return True

    def click(self, selector: str, **kwargs):
        """点击元素"""
        self.page.click(selector, **kwargs)

    def fill(self, selector: str, text: str, **kwargs):
        """填写输入框"""
        self.page.fill(selector, text, **kwargs)

    def get_text(self, selector: str, **kwargs) -> str:
        """获取元素文本"""
        return self.page.inner_text(selector, **kwargs)

# 简单的日志类
class SimpleLogger:
    def info(self, msg):
        print(f"[INFO] {msg}")

    def warning(self, msg):
        print(f"[WARNING] {msg}")

    def error(self, msg):
        print(f"[ERROR] {msg}")

def test_base_browser():
    # 配置浏览器
    config = {
        "browser_type": "chromium",
        "headless": False,  # 非headless模式，可以看到浏览器
        "timeout": 30000,
    }
    logger = SimpleLogger()

    try:
        # 创建浏览器实例
        browser = PageMixin(config, logger)

        logger.info("=== 开始浏览器多页面切换测试 ===")
        # 1. 在默认页面访问百度
        logger.info("\n1. 在默认页面访问百度")
        browser.goto("https://www.baidu.com")
        page_info = browser.get_page_info()
        logger.info(f"当前页面: {page_info}")
        # 2. 打开新页面访问B站
        logger.info("\n2. 打开新页面访问B站")
        bilibili_page = browser.open_new_page("bilibili")
        bilibili_page.goto("https://www.bilibili.com")
        logger.info(f"B站页面: {browser.get_page_info(bilibili_page)}")
        # 3. 打开新页面访问淘宝
        logger.info("\n3. 打开新页面访问淘宝")
        taobao_page = browser.open_new_page("taobao")
        taobao_page.goto("https://www.taobao.com")
        logger.info(f"淘宝页面: {browser.get_page_info(taobao_page)}")
        # 显示所有页面信息
        logger.info("\n5. 所有页面列表:")
        all_pages = browser.list_all_pages()
        for page_info in all_pages:
            logger.info(f"  页面{page_info['index']}: {page_info['tag']} - {page_info['title']}")

        # 4. 测试页面切换
        logger.info("\n6. 开始页面切换测试:")
        # 切换到百度页面
        logger.info("切换到百度页面 (通过tag)")
        browser.switch_page(tag="default")
        logger.info(f"当前页面: {browser.get_page_info()}")
        time.sleep(2)
        # 切换到B站页面
        logger.info("切换到B站页面 (通过tag)")
        browser.switch_page(tag="bilibili")
        logger.info(f"当前页面: {browser.get_page_info()}")
        time.sleep(2)
        # 通过索引切换到淘宝页面
        logger.info("切换到淘宝页面 (通过索引)")
        browser.switch_page(index=2)  # 淘宝页面是第3个(索引2)
        logger.info(f"当前页面: {browser.get_page_info()}")
        time.sleep(2)
        # 显示最终所有页面
        logger.info("\n8. 最终所有页面列表:")
        all_pages = browser.list_all_pages()
        for page_info in all_pages:
            logger.info(f"  页面{page_info['index']}: {page_info['tag']} - {page_info['title']}")
        logger.info("\n=== 测试完成，5秒后自动关闭浏览器 ===")
        time.sleep(5)

    except Exception as e:
        logger.error(f"测试过程中出现错误: {e}")
    finally:
        # 关闭浏览器
        if 'browser' in locals():
            browser.close()
            logger.info("浏览器已关闭")


if __name__ == "__main__":
    test_base_browser()
    print('done')