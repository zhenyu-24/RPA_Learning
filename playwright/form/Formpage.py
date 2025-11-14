import logging
import time
from typing import Dict, Any, Optional, List, Union
from playwright.sync_api import Page, BrowserContext, Browser, sync_playwright, expect


class FormFiller:
    """表单填写自动化类 - 支持数据映射"""

    def __init__(self, browser: Browser = None, page: Page = None, headless: bool = False):
        self.browser = browser
        self.page = page
        self.headless = headless
        self._playwright = None
        self._context = None
        # 设置日志
        self.logger = self._setup_logger()
        # 初始化浏览器（如果未提供）
        if not all([self.browser, self.page]):
            self._init_browser()

    def _setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger('FormFiller')
        logger.setLevel(logging.INFO)
        # 避免重复添加处理器
        if not logger.handlers:
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            # 控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
            # 文件处理器
            file_handler = logging.FileHandler('form_filler.log', encoding='utf-8')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        return logger

    def _init_browser(self):
        """初始化浏览器实例"""
        try:
            self._playwright = sync_playwright().start()
            self.browser = self._playwright.chromium.launch(
                headless=self.headless,
                args=['--disable-blink-features=AutomationControlled']
            )
            self._context = self.browser.new_context(
                viewport={'width': 1920, 'height': 1080}
            )
            self.page = self._context.new_page()
            # 设置弹窗和对话框处理
            self._setup_dialog_handlers()
            self.logger.info("浏览器初始化成功")
        except Exception as e:
            self.logger.error(f"浏览器初始化失败: {e}")
            raise

    def _setup_dialog_handlers(self):
        """设置对话框和弹窗处理器"""
        # 处理 JavaScript 对话框
        self.page.on("dialog", self._handle_dialog)
        # 处理新窗口弹窗
        self.page.on("popup", self._handle_popup)
        self.logger.info("弹窗和对话框处理器已设置")

    def _handle_dialog(self, dialog):
        """处理 JavaScript 对话框"""
        self.logger.info(f"检测到对话框: {dialog.type} - {dialog.message}")
        dialog.accept()  # 接受对话框
        self.logger.info("对话框已接受")

    def _handle_popup(self, popup):
        """处理新窗口弹窗"""
        self.logger.info(f"检测到弹窗: {popup.url}")
        popup.close()
        self.logger.info("弹窗已关闭")

    def navigate_to_form(self, url: str):
        """导航到表单页面"""
        try:
            self.page.goto(url, wait_until='networkidle')
            self.logger.info(f"已导航到: {url}")
        except Exception as e:
            self.logger.error(f"导航失败: {e}")
            raise

    def fill_text_input(self, selector: str, value: str):
        """填写文本输入框"""
        try:
            if value:  # 只在有值时填写
                element = self.page.locator(selector)
                element.fill(str(value))
                self.logger.info(f"文本输入框 '{selector}' 已填写: {value}")
        except Exception as e:
            self.logger.error(f"填写文本输入框失败 {selector}: {e}")
            raise

    def fill_textarea(self, selector: str, value: str):
        """填写文本区域"""
        try:
            if value:  # 只在有值时填写
                element = self.page.locator(selector)
                element.fill(str(value))
                self.logger.info(f"文本区域 '{selector}' 已填写: {value}")
        except Exception as e:
            self.logger.error(f"填写文本区域失败 {selector}: {e}")
            raise

    def set_checkbox(self, selector: str, checked: bool = True):
        """设置复选框状态"""
        try:
            element = self.page.locator(selector)
            current_state = element.is_checked()

            if checked and not current_state:
                element.check()
                self.logger.info(f"复选框 '{selector}' 已选中")
            elif not checked and current_state:
                element.uncheck()
                self.logger.info(f"复选框 '{selector}' 已取消选中")
            else:
                self.logger.info(f"复选框 '{selector}' 状态未改变")

        except Exception as e:
            self.logger.error(f"设置复选框失败 {selector}: {e}")
            raise

    def set_radio_button(self, selector: str):
        """选择单选按钮"""
        try:
            element = self.page.locator(selector)
            element.check()
            self.logger.info(f"单选按钮 '{selector}' 已选择")
        except Exception as e:
            self.logger.error(f"选择单选按钮失败 {selector}: {e}")
            raise

    def select_dropdown(self, selector: str, value: str):
        """选择下拉框选项"""
        try:
            if value:  # 只在有值时选择
                element = self.page.locator(selector)
                element.select_option(label=str(value))
                self.logger.info(f"下拉框 '{selector}' 已选择: {value}")
        except Exception as e:
            self.logger.error(f"选择下拉框选项失败 {selector}: {e}")
            raise

    def click_submit_button(self, selector: str = "button[type='submit']"):
        """点击提交按钮"""
        try:
            submit_button = self.page.locator(selector)
            # 处理可能的弹窗
            with self.page.expect_popup() as popup_info:
                submit_button.click()
            # 如果有弹窗，处理它
            try:
                popup = popup_info.value
                if popup:
                    self.logger.info("检测到提交后的弹窗")
                    popup.wait_for_load_state()
                    popup.close()
            except:
                pass  # 没有弹窗是正常的
            self.logger.info("提交按钮已点击")
        except Exception as e:
            self.logger.error(f"点击提交按钮失败: {e}")
            raise

    def fill_form_from_mapping(self, form_data: Dict[str, Any]):
        """根据映射数据填写表单"""
        self.logger.info("开始根据映射数据填写表单")
        # 处理文本输入框
        for selector, value in form_data.get("text_inputs", {}).items():
            self.fill_text_input(selector, value)
        # 处理文本区域
        for selector, value in form_data.get("textareas", {}).items():
            self.fill_textarea(selector, value)
        # 处理复选框
        for selector, checked in form_data.get("checkboxes", {}).items():
            self.set_checkbox(selector, checked)
        # 处理单选按钮
        for selector in form_data.get("radio_buttons", []):
            self.set_radio_button(selector)
        # 处理下拉框
        for selector, value in form_data.get("dropdowns", {}).items():
            self.select_dropdown(selector, value)
        self.logger.info("表单填写完成")

    def wait_for_submission_result(self, timeout: int = 10000):
        """等待提交结果"""
        try:
            # 等待页面变化或网络空闲
            self.page.wait_for_load_state('networkidle')
            self.logger.info("页面加载完成，表单可能已提交")

        except Exception as e:
            self.logger.warning(f"等待提交结果时出现异常: {e}")

    def take_screenshot(self, filename: str = None):
        """截取屏幕截图"""
        if not filename:
            timestamp = int(time.time())
            filename = f"form_screenshot_{timestamp}.png"

        self.page.screenshot(path=filename)
        self.logger.info(f"屏幕截图已保存: {filename}")

    def close(self):
        """关闭浏览器和资源"""
        try:
            if self._context:
                self._context.close()
            if self.browser:
                self.browser.close()
            if self._playwright:
                self._playwright.stop()

            self.logger.info("浏览器资源已关闭")
        except Exception as e:
            self.logger.error(f"关闭资源时出错: {e}")


def map_csv_to_form_fields(csv_data: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    将CSV数据映射到表单字段

    Args:
        csv_data: 从CSV读取的数据列表，每行是一个字典

    Returns:
        映射后的表单数据列表
    """
    mapped_data = []

    for row in csv_data:
        form_fields = {
            "text_inputs": {
                "#username": row.get("username", ""),
                "#email": row.get("email", ""),
                "#phone": row.get("phone", ""),
                "#birthdate": row.get("birthdate", ""),
                "#password": row.get("password", ""),
                "#confirm_password": row.get("confirm_password", ""),
            },
            "textareas": {
                "#comments": row.get("comments", "")
            },
            "checkboxes": {
                "#newsletter": row.get("newsletter", "").lower() in ["true", "1", "yes", "是"],
                "#promotions": row.get("promotions", "").lower() in ["true", "1", "yes", "是"],
                "#notifications": row.get("notifications", "").lower() in ["true", "1", "yes", "是"],
                "#agree_terms": True  # 必须同意条款
            },
            "radio_buttons": [
                f"#gender_{row.get('gender', 'male')}"  # gender_male, gender_female, gender_other
            ],
            "dropdowns": {
                "#country": row.get("country", ""),
                "#city": row.get("city", ""),
            }
        }
        mapped_data.append(form_fields)

    return mapped_data


def create_sample_csv_data() -> List[Dict[str, str]]:
    """
    创建示例CSV数据
    在实际使用中，这里应该从CSV文件读取
    """
    return [
        {
            "username": "zhangsan",
            "email": "zhangsan@example.com",
            "phone": "13800138000",
            "birthdate": "1990-01-15",
            "password": "password123",
            "confirm_password": "password123",
            "gender": "male",
            "country": "中国",
            "city": "北京",
            "newsletter": "true",
            "promotions": "false",
            "notifications": "true",
            "comments": "这是一个测试用户的个人简介"
        },
        {
            "username": "lisi",
            "email": "lisi@example.com",
            "phone": "13900139000",
            "birthdate": "1992-05-20",
            "password": "password456",
            "confirm_password": "password456",
            "gender": "female",
            "country": "中国",
            "city": "上海",
            "newsletter": "true",
            "promotions": "true",
            "notifications": "false",
            "comments": "另一个测试用户的简介信息"
        },
        {
            "username": "wangwu",
            "email": "wangwu@example.com",
            "phone": "13700137000",
            "birthdate": "1988-11-30",
            "password": "password789",
            "confirm_password": "password789",
            "gender": "other",
            "country": "中国",
            "city": "广州",
            "newsletter": "false",
            "promotions": "true",
            "notifications": "true",
            "comments": ""
        }
    ]


def example_usage():
    """使用示例 - 从CSV数据自动填写表单"""

    # 创建表单填写器
    form_filler = FormFiller(headless=False)

    try:
        # 导航到表单页面
        url = "http://127.0.0.1:5500/form.html"
        form_filler.navigate_to_form(url)

        # 从CSV获取数据（这里使用示例数据，实际应该从文件读取）
        csv_data = create_sample_csv_data()
        form_filler.logger.info(f"读取到 {len(csv_data)} 条数据")

        # 映射数据到表单字段
        mapped_data = map_csv_to_form_fields(csv_data)

        # 为每条数据填写表单
        for i, form_data in enumerate(mapped_data, 1):
            form_filler.logger.info(f"开始处理第 {i} 条数据")

            try:
                # 填写表单
                form_filler.fill_form_from_mapping(form_data)

                # 提交前的截图
                form_filler.take_screenshot(f"before_submission_{i}.png")

                # 点击提交按钮
                form_filler.click_submit_button()

                # 等待提交结果
                form_filler.wait_for_submission_result()

                # 提交后的截图
                form_filler.take_screenshot(f"after_submission_{i}.png")

                form_filler.logger.info(f"第 {i} 条数据处理完成")

                # 如果是最后一条数据，不需要重新导航
                if i < len(mapped_data):
                    # 等待一下然后重新导航到表单页面继续下一条
                    form_filler.page.wait_for_timeout(2000)
                    form_filler.navigate_to_form(url)

            except Exception as e:
                form_filler.logger.error(f"处理第 {i} 条数据时出错: {e}")
                form_filler.take_screenshot(f"error_{i}.png")
                continue  # 继续处理下一条数据

        form_filler.logger.info("所有数据处理完成")

    except Exception as e:
        form_filler.logger.error(f"表单填写过程出错: {e}")
        form_filler.take_screenshot("final_error.png")

    finally:
        form_filler.close()


def example_usage_single():
    """单条数据测试示例"""

    form_filler = FormFiller(headless=False)

    try:
        # 导航到表单页面
        url = "http://127.0.0.1:5500/form.html"
        form_filler.navigate_to_form(url)

        # 单条测试数据
        test_data = {
            "username": "testuser",
            "email": "test@example.com",
            "phone": "13812345678",
            "birthdate": "1995-03-20",
            "password": "testpass123",
            "confirm_password": "testpass123",
            "gender": "male",
            "country": "中国",
            "city": "北京",
            "department": "technology",
            "newsletter": "true",
            "promotions": "true",
            "notifications": "false",
            "comments": "这是单条测试数据的简介"
        }

        # 映射数据
        mapped_data = map_csv_to_form_fields([test_data])[0]

        # 填写表单
        form_filler.fill_form_from_mapping(mapped_data)

        # 截图
        form_filler.take_screenshot("single_test_before.png")

        # 提交
        form_filler.click_submit_button()

        # 等待结果
        form_filler.wait_for_submission_result()

        form_filler.take_screenshot("single_test_after.png")

        form_filler.logger.info("单条数据测试完成")

    except Exception as e:
        form_filler.logger.error(f"单条数据测试出错: {e}")
        form_filler.take_screenshot("single_test_error.png")

    finally:
        form_filler.close()


if __name__ == "__main__":
    # 运行示例
    print("选择运行模式:")
    print("1. 多条数据测试")
    print("2. 单条数据测试")

    choice = input("请输入选择 (1 或 2): ").strip()

    if choice == "1":
        example_usage()
    else:
        example_usage_single()