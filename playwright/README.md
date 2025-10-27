# Playwright教程
## 教程
- [官方文档](https://playwright.dev/python/docs/intro)
- [中文文档](https://playwright.nodejs.cn/python/docs/intro)
- [视频教程](https://www.bilibili.com/video/BV1Gw411N73T?spm_id_from=333.788.videopod.episodes&vd_source=c52a6491548814d54a99f3b97b0df55c&p=2)

## 安装
```
pip install playwright
playwright install chromium
```

## 基本操作
### 打开浏览器并访问页面
```python
from playwright.sync_api import sync_playwright
# 1.启动 playwright driver 进程
p = sync_playwright().start()
# 2.启动浏览器，返回 Browser 类型对象
browser = p.chromium.launch(headless=False)
page = browser.new_page()
page.goto("https://playwright.nodejs.cn/")
```

### 交互
执行操作从定位元素开始。Playwright 为此使用 定位器 API。定位器代表了一种随时在页面上查找元素的方法，了解有关可用定位器 不同种类 的更多信息。Playwright 将在执行操作之前等待元素变为 actionable，因此无需等待它变得可用。
```python
page.get_by_role("link", name="Get started").click()
```

| 行动                                                         | 描述                   |
| :----------------------------------------------------------- | :--------------------- |
| [locator.check()](https://playwright.nodejs.cn/python/docs/api/class-locator#locator-check) | 检查输入复选框         |
| [locator.click()](https://playwright.nodejs.cn/python/docs/api/class-locator#locator-click) | 单击该元素             |
| [locator.uncheck()](https://playwright.nodejs.cn/python/docs/api/class-locator#locator-uncheck) | 取消选中输入复选框     |
| [locator.hover()](https://playwright.nodejs.cn/python/docs/api/class-locator#locator-hover) | 将鼠标悬停在元素上     |
| [locator.fill()](https://playwright.nodejs.cn/python/docs/api/class-locator#locator-fill) | 填写表单字段，输入文本 |
| [locator.focus()](https://playwright.nodejs.cn/python/docs/api/class-locator#locator-focus) | 聚焦元素               |
| [locator.press()](https://playwright.nodejs.cn/python/docs/api/class-locator#locator-press) | 按单个键               |
| [locator.set_input_files()](https://playwright.nodejs.cn/python/docs/api/class-locator#locator-set-input-files) | 选择要上传的文件       |
| [locator.select_option()](https://playwright.nodejs.cn/python/docs/api/class-locator#locator-select-option) | 在下拉菜单中选择选项   |

## 录屏

### 运行代码生成器

```
playwright codegen --channel=msedge https://www.baidu.com/
```

运行 `codegen` 并在浏览器中执行操作。Playwright 会自动生成你的交互代码。Codegen 会分析渲染的页面并推荐最佳定位器，优先考虑角色、文本和测试 ID 定位器。当多个元素与一个定位器匹配时，生成器会对其进行改进，以唯一地标识目标元素，从而减少测试失败和不稳定性。

使用测试生成器，你可以记录：

- 通过与页面交互执行单击或填充等操作
- 通过点击工具栏图标，然后点击要断言的页面元素来执行断言。你可以选择：
  - `'assert visibility'` 断言元素可见
  - `'assert text'` 断言元素包含特定文本
  - `'assert value'` 断言某个元素具有特定值

完成与页面的交互后，按 `'record'` 按钮停止录制，然后使用 `'copy'` 按钮将生成的代码复制到编辑器。

使用 `'clear'` 按钮清除代码并重新开始录制。完成后，关闭 Playwright 检查器窗口或停止终端命令。

要了解有关生成测试的更多信息，请查看关于 [代码生成器](https://playwright.nodejs.cn/python/docs/codegen) 的详细指南。

### 生成定位器

可以使用测试生成器生成 [locators](https://playwright.nodejs.cn/python/docs/locators)。

- 按下 `'Record'` 按钮停止录制，此时会显示 `'Pick Locator'` 按钮。
- 点击 `'Pick Locator'` 按钮，并将鼠标悬停在浏览器窗口中的元素上，即可看到每个元素下方高亮的定位器。
- 点击你要定位的元素，该定位器的代码将显示在“选择定位器”按钮旁边的定位器演示区中。
- 在定位器测试区中编辑定位器进行微调，并在浏览器窗口中查看高亮显示的匹配元素
- 使用“复制”按钮复制定位器并将其粘贴到你的代码中。

### 模拟

你可以使用模拟为特定的视口、设备、配色方案、地理位置、语言或时区生成测试。测试生成器还可以保留已验证的状态。查看 [测试生成器](https://playwright.nodejs.cn/python/docs/codegen#emulation) 指南以了解更多信息。

## 运行测试

### 命令行

要运行测试，请使用 `pytest` 命令。这将默认在 Chromium 浏览器上运行你的测试。默认情况下，测试在无头模式下运行，这意味着运行测试时不会打开浏览器窗口，并且结果将在终端中看到。

```bash
pytest
```

### 在 Head 模式下运行测试

要在 head 模式下运行测试，请使用 `--headed` 标志。这将在运行测试时打开一个浏览器窗口，完成后浏览器窗口将关闭。

```bash
pytest --headed
```

### 在不同浏览器上运行测试

要指定要在哪个浏览器上运行测试，请使用 `--browser` 标志，后跟浏览器名称。

```bash
pytest --browser webkit
```

要指定多个浏览器来运行测试，请多次使用 `--browser` 标志，后跟每个浏览器的名称。

```bash
pytest --browser webkit --browser firefox
```

### 运行特定测试

要运行单个测试文件，请传入要运行的测试文件的名称。

```bash
pytest test_login.py
```

要运行一组测试文件，请传入要运行的测试文件的名称。

```bash
pytest tests/test_todo_page.py tests/test_landing_page.py
```

要运行特定测试，请传入要运行的测试的函数名称。

```bash
pytest -k test_add_a_todo_item
```

### 并行运行测试

要并行运行测试，请使用 `--numprocesses` 标志，后跟要运行测试的进程数。我们建议使用一半的逻辑 CPU 核心。

```bash
pytest --numprocesses 2
```

## 跟踪查看器

### 记录跟踪

```
# 启动跟踪功能
context.tracing.start(snapshots=True, sources=True, screenshots=True)
# 结束跟踪
context.tracing.stop(path="trace.zip")
```

可以通过使用 `--tracing` 标志运行测试来记录跟踪。

```bash
pytest --tracing on
```

用于跟踪的选项包括：

- `on`：记录每个测试的跟踪信息
- `off`：不记录痕迹。（默认）
- `retain-on-failure`：记录每个测试的跟踪信息，但删除所有成功测试运行的跟踪信息。

这将记录跟踪并将其放入 `test-results` 目录中名为 `trace.zip` 的文件中。

### 打开跟踪

你可以使用 Playwright CLI 或在 [`trace.playwright.dev`](https://trace.playwright.dev/) 上的浏览器中打开已保存的跟踪。确保添加跟踪 zip 文件所在位置的完整路径。打开后，你可以点击每个操作，或使用时间轴查看每个操作前后的页面状态。你还可以在测试的每个步骤中检查日志、源和网络。跟踪查看器会创建一个 DOM 快照，以便你可以与其进行全面交互，例如打开开发者工具等。

```bash
playwright show-trace trace.zip
```

## Pytest 插件参考

### 用法

要运行测试，请使用 [Pytest](https://docs.pytest.org/en/stable/) CLI。

```bash
pytest --browser webkit --headed
```

请注意，CLI 参数仅适用于默认的 `browser`、`context` 和 `page` 装置。如果你使用类似 [browser.new_context()](https://playwright.nodejs.cn/python/docs/api/class-browser#browser-new-context) 的 API 调用创建浏览器、上下文或页面，则 CLI 参数将不适用。

- `--headed`：以有头模式运行测试（默认值：无头模式）。
- `--browser`：在不同的浏览器 `chromium`、`firefox` 或 `webkit` 中运行测试。可以多次指定（默认值：`chromium`）。

- `--browser-channel` [Browser channel](https://playwright.nodejs.cn/python/docs/browsers) to be used.

- `--slowmo` 将 Playwright 操作减慢指定的毫秒数。此方法有助于你了解正在发生的事情（默认值：0）。

- `--device` [Device](https://playwright.nodejs.cn/python/docs/emulation) to be emulated.

- `--output` 测试生成的工件目录（默认值：`test-results`）。
- `--tracing` 是否为每个测试记录一个 [trace](https://playwright.nodejs.cn/python/docs/trace-viewer)。`on`、`off` 或 `retain-on-failure`（默认值：`off`）。
- `--video` 是否为每次测试录制视频。`on`、`off` 或 `retain-on-failure`（默认值：`off`）。
- `--screenshot` 每次测试后是否自动截图。`on`、`off` 或 `only-on-failure`（默认值：`off`）。
- `--full-page-screenshot` 是否在失败时截取整页屏幕截图。默认情况下，仅捕获视口。需要启用 `--screenshot`（默认值：`off`）。

## 打包

可以将 Playwright 与 [Pyinstaller](https://www.pyinstaller.org/) 结合使用来创建独立的可执行文件。

```
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://playwright.nodejs.cn/")
    page.screenshot(path="example.png")
    browser.close()
```

