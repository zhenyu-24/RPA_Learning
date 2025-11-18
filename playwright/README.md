# 一、安装
安装库:

```bash
pip install playwright
```

安装 [pytest 插件](https://pypi.org/project/pytest-playwright/)(Playwright 建议使用官方 [Playwright Pytest 插件](https://playwright.nodejs.cn/python/docs/test-runners) 来编写端到端测试。它提供上下文隔离，可在多种浏览器配置下开箱即用地运行)：

```bash
pip install pytest-playwright
```

安装所需的浏览器：

```bash
playwright install
```

## 案例

```
from playwright.sync_api import sync_playwright
import time

# 创建一个playwright上下文管理器
with sync_playwright() as p:
    # 创建一个浏览器（设置为非headless模式）
    browser = p.chromium.launch(headless=False)
    # 打开一个页面
    page = browser.new_page()
    # 访问淘宝
    page.goto("http://www.taobao.com")

    # 等待10秒
    time.sleep(10)
    # 关闭浏览器
    browser.close()
```

# 二、page基础操作
## page.goto(): 打开页面

1. timeout
设置页面加载的超时时间，单位为毫秒。如果页面在指定的时间内未加载完成，将抛出超时异常。
```
page.goto(url, timeout=30000)  # 设置超时时间为30秒
```

2. referer
设置页面导航的引用页面URL，模拟用户从某个特定页面跳转而来。
```
page.goto(url, referer='https://example.com')
```

3. wait_until
设置控制着页面加载完成的条件
- 'load'：等待页面完全加载
- domcontentloaded:等待DOM内容加载完成，即HTML文档已解析完毕，但页面内的资源（如图片、样式表、脚本等）可能还在加载中
- network: 等待所有的网络请求完毕
```
page.goto(url,wait_until='load')
```

## 其它基础操作

- page.title():获取标题名称
- page.content(): 获取页面html
- page.close():  关闭页面
- page.reload():刷新页面
- page.go_back():  上一页
- page.go_forward(): 下一页
- page.screenshot(): 页面截图

## 定位方式

- [page.get_by_role()](https://playwright.net.cn/python/docs/locators#locate-by-role) 根据显式和隐式辅助功能属性进行定位(**优先**)。
- [page.get_by_text()](https://playwright.net.cn/python/docs/locators#locate-by-text) 根据文本内容进行定位。
- [page.get_by_label()](https://playwright.net.cn/python/docs/locators#locate-by-label) 根据关联标签的文本定位表单控件。
- [page.get_by_placeholder()](https://playwright.net.cn/python/docs/locators#locate-by-placeholder) 根据占位符定位输入框。
- [page.get_by_alt_text()](https://playwright.net.cn/python/docs/locators#locate-by-alt-text) 根据替代文本定位元素，通常是图像。
- [page.get_by_title()](https://playwright.net.cn/python/docs/locators#locate-by-title) 根据 title 属性定位元素。
- [page.get_by_test_id()](https://playwright.net.cn/python/docs/locators#locate-by-test-id) 根据其 `data-testid` 属性定位元素（可配置其他属性）。

# 三、操作

## 文本输入

使用 [locator.fill()](https://playwright.net.cn/python/docs/api/class-locator#locator-fill) 是填写表单字段最简单的方法。它会聚焦元素并触发一个带有所输入文本的 `input` 事件。它适用于 `<input>`、`<textarea>` 和 `[contenteditable]` 元素。

```
# Text input
page.get_by_role("textbox").fill("Peter")

# Date input
page.get_by_label("Birth date").fill("2020-02-02")

# Time input
page.get_by_label("Appointment time").fill("13:15")

# Local datetime input
page.get_by_label("Local time").fill("2020-03-02T05:15")
```

## 复选框和单选按钮

使用 [locator.set_checked()](https://playwright.net.cn/python/docs/api/class-locator#locator-set-checked) 是勾选和取消勾选复选框或单选按钮最简单的方法。此方法可用于 `input[type=checkbox]`、`input[type=radio]` 和 `[role=checkbox]` 元素。使用 `is_checked()`判断是否被选中

```
# Check the checkbox
page.get_by_label('I agree to the terms above').check()

# Assert the checked state
expect(page.get_by_label('Subscribe to newsletter')).to_be_checked()

# Select the radio button
page.get_by_label('XL').check()
```

## 选择选项

使用 [locator.select_option()](https://playwright.net.cn/python/docs/api/class-locator#locator-select-option) 在 `<select>` 元素中选择一个或多个选项。您可以指定选项的 `value` 或 `label` 进行选择。可以同时选择多个选项。

```
# Single selection matching the value or label
page.get_by_label('Choose a color').select_option('blue')

# Single selection matching the label
page.get_by_label('Choose a color').select_option(label='Blue')

# Multiple selected items
page.get_by_label('Choose multiple colors').select_option(['red', 'green', 'blue'])
```

## 鼠标点击

执行简单的模拟用户点击。

```py
# Generic click
page.get_by_role("button").click()

# Double click
page.get_by_text("Item").dblclick()

# Right click
page.get_by_text("Item").click(button="right")

# Shift + click
page.get_by_text("Item").click(modifiers=["Shift"])

# Hover over element
page.get_by_text("Item").hover()

# Click the top left corner
page.get_by_text("Item").click(position={ "x": 0, "y": 0})
```

## 文件上传与下载

### 上传

您可以使用 [locator.set_input_files()](https://playwright.net.cn/python/docs/api/class-locator#locator-set-input-files) 方法选择用于上传的输入文件。它要求第一个参数指向类型为 `"file"` 的 [input 元素](https://mdn.org.cn/en-US/docs/Web/HTML/Element/input)。可以在数组中传递多个文件。如果某些文件路径是相对路径，它们将相对于当前工作目录进行解析。空数组会清除选定的文件。

```py
# Select one file
page.get_by_label("Upload file").set_input_files('myfile.pdf')

# Select multiple files
page.get_by_label("Upload files").set_input_files(['file1.txt', 'file2.txt'])

# Select a directory
page.get_by_label("Upload directory").set_input_files('mydir')

# Remove all the selected files
page.get_by_label("Upload file").set_input_files([])

# Upload buffer from memory
page.get_by_label("Upload file").set_input_files(
    files=[
        {"name": "test.txt", "mimeType": "text/plain", "buffer": b"this is a test"}
    ],
)
```

如果您没有可用的输入元素（它是动态创建的），您可以处理 [page.on("filechooser")](https://playwright.net.cn/python/docs/api/class-page#page-event-file-chooser) 事件或在您的操作后使用相应的等待方法

```py
with page.expect_file_chooser() as fc_info:
    page.get_by_label("Upload file").click()
file_chooser = fc_info.value
file_chooser.set_files("myfile.pdf")
```

### 下载

页面下载的每个附件都会触发 [page.on("download")](https://playwright.net.cn/python/docs/api/class-page#page-event-download) 事件。所有这些附件都会下载到一个临时文件夹中。你可以使用事件中的 [Download](https://playwright.net.cn/python/docs/api/class-download) 对象获取下载的 URL、文件名和有效载荷流。

你可以在 [browser_type.launch()](https://playwright.net.cn/python/docs/api/class-browsertype#browser-type-launch) 中使用 [downloads_path](https://playwright.net.cn/python/docs/api/class-browsertype#browser-type-launch-option-downloads-path) 选项指定下载文件的存储路径。

**注意**:下载的文件会在产生它们的浏览器上下文关闭时被删除。

这是处理文件下载的最简单方法

```py
# Start waiting for the download
with page.expect_download() as download_info:
    # Perform the action that initiates download
    page.get_by_text("Download file").click()
download = download_info.value

# Wait for the download process to complete and save the downloaded file somewhere
download.save_as("/path/to/save/at/" + download.suggested_filename)
```

如果你不知道是什么启动了下载，你仍然可以处理这个事件

```py
page.on("download", lambda download: print(download.path()))
```

请注意，处理事件会分叉控制流，使脚本更难理解。你的主控制流可能没有等待此操作解析，因此你的场景可能在下载文件时结束。

### **文件选择对话框**

```
# 监听文件选择器弹出
with page.expect_file_chooser() as fc_info:
    page.get_by_role("button", name=" 选择文件").click()
# 获取文件选择器并设置文件
file_chooser = fc_info.value
file_chooser.set_files([r'E:\code\PyQt-Fluent-Widgets\PyQt-Fluent-Widgets\README.md'])
```

```
page.on("filechooser", lambda file_chooser: file_chooser.set_files("/tmp/myfile.pdf"))
```

## 处理弹窗/打开的新页面

`page.expect_popup()`: 同步等待，使用 `with` 语句，直到弹窗出现。使用场景: 知道**何时**会触发弹窗, 一次等待一个弹窗

```
# 首先，使用 with 语句开始等待一个弹出窗口
with page.expect_popup() as popup_info:
    # 然后，在这个代码块内执行会触发弹窗的操作，例如点击一个链接
    page.get_by_text("打开新窗口的链接").click()
# 当 with 块结束时，弹出窗口应该已经被捕获了
# 通过 .value 获取新页面的对象
new_page = popup_info.value
# 现在，你可以像操作普通页面一样操作这个新窗口了
new_page.wait_for_load_state() # 等待新页面加载
```

`page.on("popup", handler)`: 事件监听，设置回调函数; 使用场景: 不知道**何时**会触发弹窗, 处理所有后续弹窗



# 四、元素筛选与过滤

## 元素筛选

 1.	count()

统计匹配到的元素个数

```
res = page.locator(li).count()
```

 2.	get_attribute()

获取匹配元素的属性值。

```
page.locator('img').get_attribute('src')
```

 3.	inner_text()

获取元素的文本

```
page.locator('#box').inner_text()
```

 4. input_value()

获取input元素的value值

```
value = page.locator('#user').input_value()
```

 5. all_inner_texts()

返回所有匹配元素的文本内容

```
texts = page.locator("link").all_inner_texts()
```

 6. first、last、nth()

```
page.locator(li).first
banana = page.locator("listitem").last
# 获取匹配到的第2个元素
banana = page.locator("listitem").nth(2)
```

## 过滤定位器

### 按文本过滤

可以使用 [locator.filter()](https://playwright.nodejs.cn/python/docs/api/class-locator#locator-filter) 方法按文本过滤定位器。它将在元素内部的某个位置（可能在后代元素中）搜索特定字符串，不区分大小写。你还可以传递正则表达式。

```py
page.get_by_role("listitem").filter(has_text=re.compile("Product 2")).get_by_role(
    "button", name="Add to cart"
).click()
```

### 通过不包含文本进行过滤

或者，通过不包含文本进行过滤：

```py
# 5 in-stock items
expect(page.get_by_role("listitem").filter(has_not_text="Out of stock")).to_have_count(5)
```

### 按子级/后代过滤

定位器支持仅选择具有或不具有与另一个定位器匹配的后代的元素的选项。因此，你可以按任何其他定位器（例如 [locator.get_by_role()](https://playwright.nodejs.cn/python/docs/api/class-locator#locator-get-by-role)、[locator.get_by_test_id()](https://playwright.nodejs.cn/python/docs/api/class-locator#locator-get-by-test-id)、[locator.get_by_text()](https://playwright.nodejs.cn/python/docs/api/class-locator#locator-get-by-text) 等）进行过滤。

```py
expect(
    page.get_by_role("listitem").filter(
        has=page.get_by_role("heading", name="Product 2")
    )
).to_have_count(1)
```

### 按没有子级/后代进行过滤

我们还可以通过内部没有匹配元素来进行过滤。

```py
expect(
    page.get_by_role("listitem").filter(
        has_not=page.get_by_role("heading", name="Product 2")
    )
).to_have_count(1)
```

# 五、元素选择

## CSS选择器

Playwright 中，根据 CSS Selector 选择元素，就是使用 [Locator](https://playwright.dev/python/docs/api/class-locator) 类型的对象

比如，前文中， Page 对象的 locator方法就会创建一个 `Locator` 类型对象，参数就可以是 CSS Selector 表达式

```py
page.locator('#kw').fill('通讯')
page.locator('#go').click() 
```

Page对象的 locator 定位到的如果是唯一的 html元素，就可以调用 Locator 对象的 方法，比如 `fill` , `click` , `inner_text` 等等对元素进行操作了。

### 根据 tag名、id、class 选择元素

CSS Selector 可以根据 `tag名` 、 `id 属性` 和 `class属性` 来 选择元素，

1. 根据 tag名 选择元素的 CSS Selector 语法非常简单，直接写上tag名即可，

比如 要选择 所有的tag名为div的元素，打印所有的tag名为div的元素的内部可见文本

```py
locators = page.locator('div').all()
for one in locators:
    print(one.inner_text())
```

要获取 所有的tag名为div的元素的内部可见文本，也可以直接调用 `all_inner_texts`

```py
texts = page.locator('div').all_inner_texts()
```

注意，如果 locator调用 `匹配的结果是多个元素` ， 调用 `针对单个元素的方法` ，比如 `inner_text` ，会有错误抛出：

```py
page.locator('div').inner_text()
```

2. 根据id属性 选择元素的语法是在id号前面加上一个井号： `#id值`

比如 ，有下面这样的元素：

```html
<input  type="text" id='searchtext' />
```

就可以使用 `#searchtext` 这样的 CSS Selector 来选择它。

比如，我们想在 `id 为 searchtext` 的输入框中输入文本 `你好` ，完整的Python代码如下

```py
lct = page.locator('#searchtext')
lct.fill('你好')
```

3.根据class属性 选择元素的语法是在 class 值 前面加上一个点： `.class值`

要选择 class 属性值为 animal的元素 动物，可以这样写

```py
page.locator('.animal')
```

一个 学生张三 可以定义有 `多个` 类型： `中国人` 和 `学生` 。`中国人` 和 `学生` 都是 张三 的 类型。元素也可以有 `多个class类型` ，多个class类型的值之间用 `空格` 隔开，比如

```html
<span class="chinese student">张三</span>
```

注意，这里 span元素 有两个class属性，分别 是 chinese 和 student， 而不是一个 名为 `chinese student` 的属性。我们要用代码选择这个元素，可以指定任意一个class 属性值，都可以匹配到这个元素，如下

```py
page.locator('.chinese')
```

或者

```py
page.locator('.student')
```

而不能这样写

```py
page.locator('.chinese student')
```

如果要表示同时具有两个class 属性，可以这样写

```py
page.locator('.chinese.student')
```

### 匹配多个元素

前面已经说， 如果一个 locator表达式匹配多个元素，要获取所有的元素对应的 locator 对象，使用 `all方法`

```py
locators = page.locator('.plant').all()
```

有时，我们只需要得到某种表达式对应的元素数量 ，可以使用 `count方法`，如下

```py
count = page.locator('.plant').count()
```

返回结果就是匹配的元素数量。 可以根据返回结果是否为0 判断元素是否存在

有时，我们只需要得到某种表达式对应的第一个，或者最后一个元素。

可以使用 `first` 和 `last` 属性 ， 如下

```py
lct = page.locator('.plant')
print(lct.first.inner_text(), lct.last.inner_text())
```

也可以，通过 `nth` 方法，获取指定次序的元素，参数0表达第一个， 1 表示第2个，比如

```py
lct = page.locator('.plant')
print(lct.nth(1).inner_text())
```

### 元素内部定位

前面都是通过 `Page` 对象调用的 locator 方法， 定位的范围是整个网页。如果我们想在某个元素内部定位，可以通过 `Locator` 对象 调用 locator 方法。比如

```py
lct = page.locator('#bottom')

# 在 #bottom 对应元素的范围内 寻找标签名为 span 的元素。
eles = lct.locator('span').all()
for e in eles:
    print(e.inner_text())
```

### 选择 子元素 和 后代元素

HTML中， 元素 内部可以 **包含其他元素**， 比如 下面的 HTML片段

```html
<div id='container'>
    
    <div id='layer1'>
        <div id='inner11'>
            <span>内层11</span>
        </div>
        <div id='inner12'>
            <span>内层12</span>
        </div>
    </div>

    <div id='layer2'>
        <div id='inner21'>
            <span>内层21</span>
        </div>
    </div>
    
</div>
```

下面的一段话有些绕口， 请 大家细心 阅读：

id 为 `container` 的div元素 包含了 id 为 `layer1` 和 `layer2` 的两个div元素。这种包含是直接包含， 中间没有其他的层次的元素了。 所以 id 为 `layer1` 和 `layer2` 的两个div元素 是 id 为 `container` 的div元素 的 **直接子元素**。而 id 为 `layer1` 的div元素 又包含了 id 为 `inner11` 和 `inner12` 的两个div元素。 中间没有其他层次的元素，所以这种包含关系也是 **直接子元素** 关系。id 为 `layer2` 的div元素 又包含了 id 为 `inner21` 这个div元素。 这种包含关系也是 **直接子元素** 关系

而对于 id 为 `container` 的div元素来说， id 为 `inner11` 、`inner12` 、`inner22` 的元素 和 两个 `span类型的元素` 都不是 它的直接子元素， 因为中间隔了 几层。虽然不是直接子元素， 但是 它们还是在 `container` 的内部， 可以称之为它 的 **后代元素**。后代元素也包括了直接子元素， 比如 id 为 `layer1` 和 `layer2` 的两个div元素 也可以说 是 id 为 `container` 的div元素 的 **直接子元素，同时也是后代子元素**。如果 `元素2` 是 `元素1` 的 直接子元素， CSS Selector 选择子元素的语法是这样的

```undefined
元素1 > 元素2
```

中间用一个大于号 （我们可以理解为箭头号）。注意，最终选择的元素是 **元素2**， 并且要求这个 **元素2** 是 **元素1** 的直接子元素。也支持更多层级的选择， 比如

```undefined
元素1 > 元素2 > 元素3 > 元素4
```

就是选择 `元素1` 里面的子元素 `元素2` 里面的子元素 `元素3` 里面的子元素 `元素4` ， 最终选择的元素是 **元素4**。

如果 `元素2` 是 `元素1` 的 后代元素， CSS Selector 选择后代元素的语法是这样的

```undefined
元素1   元素2
```

中间是一个或者多个空格隔开。最终选择的元素是 **元素2** ， 并且要求这个 **元素2** 是 **元素1** 的后代元素。也支持更多层级的选择， 比如

```undefined
元素1   元素2   元素3  元素4
```

最终选择的元素是 **元素4**

### 根据属性选择

id、class 都是web元素的 `属性` ，因为它们是很常用的属性，所以css选择器专门提供了根据 id、class 选择的语法。

那么其他的属性呢？比如

```html
<a href="http://www.miitbeian.gov.cn">苏ICP备88885574号</a>！
```

css 选择器支持通过任何属性来选择元素，语法是用一个方括号 `[]` 。比如要选择上面的a元素，就可以使用`[href="http://www.miitbeian.gov.cn"]` 。这个表达式的意思是，选择 属性href值为 `http://www.miitbeian.gov.cn` 的元素。

完整代码如下

```py
from playwright.sync_api import sync_playwright

p = sync_playwright().start()
browser = p.chromium.launch(headless=False, slow_mo=50)
page = browser.new_page()
page.goto("https://www.byhy.net/cdn2/files/selenium/sample1.html")

# 根据属性选择元素
element = page.locator('[href="http://www.miitbeian.gov.cn"]')
# 打印出元素文本
print(element.inner_text())
```

当然，前面可以加上标签名的限制，比如 `a[href="http://www.miitbeian.gov.cn"]` 表示 选择所有 标签名为 `a` ，且 属性 href值为 `http://www.miitbeian.gov.cn` 的元素。属性值用单引号，双引号都可以。根据属性选择，还可以不指定属性值，比如 `[href]` ， 表示选择 所有 具有 属性名 为href 的元素，不管它们的值是什么。

CSS 还可以选择 属性值 `包含` 某个字符串 的元素比如， 要选择a节点，里面的href属性包含了 miitbeian 字符串，就可以这样写

```css
a[href*="miitbeian"]
```

还可以 选择 属性值 以某个字符串 `开头` 的元素。比如， 要选择a节点，里面的href属性以 http 开头 ，就可以这样写

```css
a[href^="http"]
```

还可以 选择 属性值 以某个字符串 `结尾` 的元素。比如， 要选择a节点，里面的href属性以 gov.cn 结尾 ，就可以这样写

```css
a[href$="gov.cn"]
```

如果一个元素具有多个属性

```html
<div class="misc" ctype="gun">沙漠之鹰</div>
```

CSS 选择器 可以指定 选择的元素要 同时具有多个属性的限制，像这样 `div[class=misc][ctype=gun]`

### 选择语法联合使用

CSS selector的另一个强大之处在于： 选择语法 可以 `联合使用`。比如， 我们要选择 如下网页中 html 中的元素 `版权1` 对应的 `span`

```html
<div id='bottom'>
    <div class='footer1'>
        <span class='copyright' name='cp1'>版权1</span>
        <span class='copyright' name='cp2'>版权2</span>
        <span class='copyright1' name='cp1'>版权3</span>
    </div>
    <div class='footer2'>
        <span class='copyright' name='cp1'>版权4</span>
    </div>        
</div>         
```

CSS selector 表达式 可以这样写：

```css
.footer1 > .copyright[name=cp1]
```

### 组选择

如果我们要 同时选择所有class 为 plant `和` class 为 animal 的元素。怎么办？这种情况，css选择器可以 使用 `逗号` ，称之为 组选择 ，像这样

```html
.plant , .animal
```

再比如，我们要同时选择所有tag名为div的元素 `和` id为BYHY的元素，就可以像这样写

```html
div,#BYHY
```

对应的Playwright代码如下

```py
elements = wd.find_elements(By.CSS_SELECTOR, 'div,#BYHY')
for element in elements:
    print(element.text)
```

###  按次序选择子节点

对应的html如下，关键信息如下

```html
    <body>  
       <div id='t1'>
           <h3> 唐诗 </h3>
           <span>李白</span>
           <p>静夜思</p>
           <span>杜甫</span>
           <p>春夜喜雨</p>              
       </div>      
        
       <div id='t2'>
           <h3> 宋词 </h3>
           <span>苏轼</span>
           <p>赤壁怀古</p>
           <p>明月几时有</p>
           <p>江城子·乙卯正月二十日夜记梦</p>
           <p>蝶恋花·春景</p>
           <span>辛弃疾</span>
           <p>京口北固亭怀古</p>
           <p>青玉案·元夕</p>
           <p>西江月·夜行黄沙道中</p>
       </div>             

    </body>
```

#### 父元素的第n个子节点

我们可以指定选择的元素 `是父元素的第几个子节点`使用 `nth-child`比如，我们要选择 唐诗 和宋词 的第一个 作者，也就是说 选择的是 第2个子元素，并且是span类型。所以这样可以这样写 `span:nth-child(2)` ，如果你不加节点类型限制，直接这样写 `:nth-child(2)`就是选择所有位置为第2个的所有元素，不管是什么类型。

#### 父元素的倒数第n个子节点

也可以反过来， 选择的是父元素的 `倒数第几个子节点` ，使用 `nth-last-child`比如：

```html
p:nth-last-child(1)
```

就是选择第倒数第1个子元素，并且是p元素

#### 父元素的第几个某类型的子节点

我们可以指定选择的元素 是父元素的第几个 `某类型的` 子节点使用 `nth-of-type`。比如，我们要选择 唐诗 和宋词 的第一个 作者，

可以像上面那样思考：选择的是 第2个子元素，并且是span类型。所以这样可以这样写 `span:nth-child(2)` ，还可以这样思考，选择的是 `第1个span类型` 的子元素。所以也可以这样写 `span:nth-of-type(1)`

#### 父元素的倒数第几个某类型的子节点

当然也可以反过来， 选择父元素的 `倒数第几个某类型` 的子节点，使用 `nth-last-of-type`像这样

```html
p:nth-last-of-type(2)
```

## role选择器

### get_by_alt_text

允许通过替代文本定位元素。

**用法**

例如，此方法将通过替代文本 "Playwright 标志" 查找图片

```html
<img alt='Playwright logo'>
```

```py
page.get_by_alt_text("Playwright logo").click()
```

- `exact` [bool](https://docs.python.org/3/library/stdtypes.html) *(optional)*

是否查找精确匹配：区分大小写和整个字符串。默认为 false。通过正则表达式定位时被忽略。请注意，完全匹配仍然会修剪空格。

### get_by_label

允许通过关联的 `<label>` 或 `aria-labelledby` 元素的文本或通过 `aria-label` 属性来定位输入元素。

**用法**

例如，此方法将在以下 DOM 中查找标签 "用户名" 和 "密码" 的输入：

```html
<input aria-label="Username">
<label for="password-input">Password:</label>
<input id="password-input">
```

```py
page.get_by_label("Username").fill("john")
page.get_by_label("Password").fill("secret")
```

### get_by_placeholder

允许通过占位符文本定位输入元素。

**用法**

例如，考虑以下 DOM 结构。

```html
<input type="email" placeholder="name@example.com" />
```

你可以在通过占位符文本找到输入后填充输入：

```py
page.get_by_placeholder("name@example.com").fill("playwright@microsoft.com")
```

### get_by_role

允许通过 [ARIA 角色](https://www.w3.org/TR/wai-aria-1.2/#roles)、[ARIA 属性](https://www.w3.org/TR/wai-aria-1.2/#aria-attributes) 和 [可访问的名称](https://w3c.github.io/accname/#dfn-accessible-name) 定位元素。

**用法**

考虑以下 DOM 结构。

```html
<h3>Sign up</h3>
<label>
  <input type="checkbox" /> Subscribe
</label>
<br/>
<button>Submit</button>
```

你可以通过每个元素的隐式角色来定位它：

```py
expect(page.get_by_role("heading", name="Sign up")).to_be_visible()

page.get_by_role("checkbox", name="Subscribe").check()

page.get_by_role("button", name=re.compile("submit", re.IGNORECASE)).click()
```

### get_by_text

允许定位包含给定文本的元素。另请参阅 [locator.filter()](https://playwright.nodejs.cn/python/docs/api/class-locator#locator-filter)，它允许按其他条件（例如可访问的角色）进行匹配，然后按文本内容进行过滤。

**用法**

考虑以下 DOM 结构：

```html
<div>Hello <span>world</span></div>
<div>Hello</div>
```

你可以通过文本子字符串、精确字符串或正则表达式进行定位：

```py
# Matches <span>
page.get_by_text("world")

# Matches first <div>
page.get_by_text("Hello world")

# Matches second <div>
page.get_by_text("Hello", exact=True)

# Matches both <div>s
page.get_by_text(re.compile("Hello"))

# Matches second <div>
page.get_by_text(re.compile("^hello$", re.IGNORECASE))
```

### get_by_title

允许通过标题属性定位元素。

**用法**

考虑以下 DOM 结构。

```html
<span title='Issues count'>25 issues</span>
```

你可以通过标题文本找到问题后查看问题数：

```py
expect(page.get_by_title("Issues count")).to_have_text("25 issues")
```

# 页面

每个 [BrowserContext](https://playwright.net.cn/python/docs/api/class-browsercontext) 可以有多个页面。一个 [Page](https://playwright.net.cn/python/docs/api/class-page) 指的是浏览器上下文中的一个选项卡或一个弹出窗口。它应该用于导航到 URL 并与页面内容进行交互。

```py
page = context.new_page()

# Navigate explicitly, similar to entering a URL in the browser.
page.goto('http://example.com')
# Fill an input.
page.locator('#search').fill('query')

# Navigate implicitly by clicking a link.
page.locator('#submit').click()
# Expect a new url.
print(page.url)
```

## 多个页面

每个浏览器上下文可以承载多个页面（标签页）。

- 每个页面都表现得像一个聚焦的、活动的页面。不需要将页面带到最前面。
- 上下文中的页面遵循上下文级别的模拟，例如视口大小、自定义网络路由或浏览器语言环境。

```py
# create two pages
page_one = context.new_page()
page_two = context.new_page()

# get pages of a browser context
all_pages = context.pages
```

## 处理弹窗

如果页面打开了一个弹窗（例如，由 `target="_blank"` 链接打开的页面），您可以通过监听页面上的 `popup` 事件来获取它的引用。

除了 `browserContext.on('page')` 事件之外，还会发出此事件，但仅适用于与此页面相关的弹窗。

## 处理弹窗

如果页面打开了一个弹窗（例如，由 `target="_blank"` 链接打开的页面），您可以通过监听页面上的 `popup` 事件来获取它的引用。

除了 `browserContext.on('page')` 事件之外，还会发出此事件，但仅适用于与此页面相关的弹窗。

```py
# Get popup after a specific action (e.g., click)
with page.expect_popup() as popup_info:
    page.get_by_text("open the popup").click()
popup = popup_info.value

# Interact with the popup normally
popup.get_by_role("button").click()
print(popup.title())
```

如果触发弹窗的操作未知，可以使用以下模式。

```py
# Get all popups when they open
def handle_popup(popup):
    popup.wait_for_load_state()
    print(popup.title())

page.on("popup", handle_popup)
```

# 对话框

Playwright 可以与网页对话框交互，例如 [`alert`](https://mdn.org.cn/en-US/docs/Web/API/Window/alert)、[`confirm`](https://mdn.org.cn/en-US/docs/Web/API/Window/confirm)、[`prompt`](https://mdn.org.cn/en-US/docs/Web/API/Window/prompt) 以及 [`beforeunload`](https://mdn.org.cn/en-US/docs/Web/API/Window/beforeunload_event) 确认。

## alert()、confirm()、prompt() 对话框

默认情况下，对话框由 Playwright 自动关闭，因此您无需处理它们。但是，您可以在触发对话框的操作之前注册一个对话框处理程序，以 [dialog.accept()](https://playwright.net.cn/python/docs/api/class-dialog#dialog-accept) 或 [dialog.dismiss()](https://playwright.net.cn/python/docs/api/class-dialog#dialog-dismiss) 它。

```py
page.on("dialog", lambda dialog: dialog.accept())
page.get_by_role("button").click()
```

[page.on("dialog")](https://playwright.net.cn/python/docs/api/class-page#page-event-dialog) 监听器**必须处理**对话框。否则您的操作将停滞，无论是 [locator.click()](https://playwright.net.cn/python/docs/api/class-locator#locator-click) 还是其他操作。这是因为 Web 中的对话框是模态的，因此会阻塞后续页面执行，直到它们被处理。

## beforeunload 对话框

`beforeunload` 是浏览器的一种安全机制，当用户尝试离开或关闭页面时，如果页面有未保存的数据，浏览器会显示一个确认对话框。当 [page.close()](https://playwright.net.cn/python/docs/api/class-page#page-close) 被调用时，如果 [run_before_unload](https://playwright.net.cn/python/docs/api/class-page#page-close-option-run-before-unload) 的值为真，页面将运行其卸载处理程序。这是 [page.close()](https://playwright.net.cn/python/docs/api/class-page#page-close) 不等待页面实际关闭的唯一情况，因为页面最终可能会保持打开状态。

您可以注册一个对话框处理程序来自己处理 `beforeunload` 对话框

```py
def handle_dialog(dialog):
    assert dialog.type == 'beforeunload'
    dialog.dismiss()

page.on('dialog', lambda: handle_dialog)
page.close(run_before_unload=True)
```

## 打印对话框

为了断言通过 [`window.print`](https://mdn.org.cn/en-US/docs/Web/API/Window/print) 触发了打印对话框，您可以使用以下代码片段

```py
page.goto("<url>")

page.evaluate("(() => {window.waitForPrintDialog = new Promise(f => window.print = f);})()")
page.get_by_text("Print it!").click()

page.wait_for_function("window.waitForPrintDialog")
```

这将等待在点击按钮后打开打印对话框。请确保在点击按钮之前/页面加载后评估脚本。

# 断言

Playwright 包括自动重试断言，通过等待直到满足条件来消除不稳定，类似于操作之前的自动等待。你可以为全局或每个断言指定自定义超时。默认超时时间为 5 秒。

```
from playwright.sync_api import expect

expect.set_options(timeout=10_000)	# 全局超时
def test_foobar(page: Page) -> None:
    expect(page.get_by_text("Name")).to_be_visible(timeout=10_000)	# 每个断言超时
```

| 断言                                                         | 描述                                                         |
| :----------------------------------------------------------- | :----------------------------------------------------------- |
| [expect(locator).to_be_attached()](https://playwright.net.cn/python/docs/api/class-locatorassertions#locator-assertions-to-be-attached) | 元素已附加                                                   |
| [expect(locator).to_be_checked()](https://playwright.net.cn/python/docs/api/class-locatorassertions#locator-assertions-to-be-checked) | 复选框已选中                                                 |
| [expect(locator).to_be_disabled()](https://playwright.net.cn/python/docs/api/class-locatorassertions#locator-assertions-to-be-disabled) | 元素已禁用                                                   |
| [expect(locator).to_be_editable()](https://playwright.net.cn/python/docs/api/class-locatorassertions#locator-assertions-to-be-editable) | 元素可编辑                                                   |
| [expect(locator).to_be_empty()](https://playwright.net.cn/python/docs/api/class-locatorassertions#locator-assertions-to-be-empty) | 容器为空                                                     |
| [expect(locator).to_be_enabled()](https://playwright.net.cn/python/docs/api/class-locatorassertions#locator-assertions-to-be-enabled) | 元素已启用                                                   |
| [expect(locator).to_be_focused()](https://playwright.net.cn/python/docs/api/class-locatorassertions#locator-assertions-to-be-focused) | 元素已聚焦                                                   |
| [expect(locator).to_be_hidden()](https://playwright.net.cn/python/docs/api/class-locatorassertions#locator-assertions-to-be-hidden) | 元素不可见                                                   |
| [expect(locator).to_be_in_viewport()](https://playwright.net.cn/python/docs/api/class-locatorassertions#locator-assertions-to-be-in-viewport) | 元素与视口相交                                               |
| [expect(locator).to_be_visible()](https://playwright.net.cn/python/docs/api/class-locatorassertions#locator-assertions-to-be-visible) | 元素可见                                                     |
| [expect(locator).to_contain_class()](https://playwright.net.cn/python/docs/api/class-locatorassertions#locator-assertions-to-contain-class) | 元素具有指定的 CSS 类                                        |
| [expect(locator).to_contain_text()](https://playwright.net.cn/python/docs/api/class-locatorassertions#locator-assertions-to-contain-text) | 元素包含文本                                                 |
| [expect(locator).to_have_accessible_description()](https://playwright.net.cn/python/docs/api/class-locatorassertions#locator-assertions-to-have-accessible-description) | 元素具有匹配的[无障碍描述](https://w3c.github.io/accname/#dfn-accessible-description) |
| [expect(locator).to_have_accessible_name()](https://playwright.net.cn/python/docs/api/class-locatorassertions#locator-assertions-to-have-accessible-name) | 元素具有匹配的[无障碍名称](https://w3c.github.io/accname/#dfn-accessible-name) |
| [expect(locator).to_have_attribute()](https://playwright.net.cn/python/docs/api/class-locatorassertions#locator-assertions-to-have-attribute) | 元素具有 DOM 属性                                            |
| [expect(locator).to_have_class()](https://playwright.net.cn/python/docs/api/class-locatorassertions#locator-assertions-to-have-class) | 元素具有 class 属性                                          |
| [expect(locator).to_have_count()](https://playwright.net.cn/python/docs/api/class-locatorassertions#locator-assertions-to-have-count) | 列表具有精确数量的子元素                                     |
| [expect(locator).to_have_css()](https://playwright.net.cn/python/docs/api/class-locatorassertions#locator-assertions-to-have-css) | 元素具有 CSS 属性                                            |
| [expect(locator).to_have_id()](https://playwright.net.cn/python/docs/api/class-locatorassertions#locator-assertions-to-have-id) | 元素具有 ID                                                  |
| [expect(locator).to_have_js_property()](https://playwright.net.cn/python/docs/api/class-locatorassertions#locator-assertions-to-have-js-property) | 元素具有 JavaScript 属性                                     |
| [expect(locator).to_have_role()](https://playwright.net.cn/python/docs/api/class-locatorassertions#locator-assertions-to-have-role) | 元素具有特定的[ARIA 角色](https://www.w3.org/TR/wai-aria-1.2/#roles) |
| [expect(locator).to_have_text()](https://playwright.net.cn/python/docs/api/class-locatorassertions#locator-assertions-to-have-text) | 元素匹配文本                                                 |
| [expect(locator).to_have_value()](https://playwright.net.cn/python/docs/api/class-locatorassertions#locator-assertions-to-have-value) | 输入框有值                                                   |
| [expect(locator).to_have_values()](https://playwright.net.cn/python/docs/api/class-locatorassertions#locator-assertions-to-have-values) | 选择框已选择选项                                             |
| [expect(locator).to_match_aria_snapshot()](https://playwright.net.cn/python/docs/api/class-locatorassertions#locator-assertions-to-match-aria-snapshot) | 元素与提供的 Aria 快照匹配                                   |
| [expect(page).to_have_title()](https://playwright.net.cn/python/docs/api/class-pageassertions#page-assertions-to-have-title) | 页面有标题                                                   |
| [expect(page).to_have_url()](https://playwright.net.cn/python/docs/api/class-pageassertions#page-assertions-to-have-url) | 页面有 URL                                                   |
| [expect(response).to_be_ok()](https://playwright.net.cn/python/docs/api/class-apiresponseassertions#api-response-assertions-to-be-ok) | 响应状态为 OK                                                |

# 等待

playwright默认就有智能等待机制，默认等待的时间为30秒(30000毫秒)

可以使用 Page 对象的 `wait_for_timeout` 方法达到等待效果，单位是 `毫秒`

```py
page.wait_for_timeout(1000)
```

### 1、set_default_timeout：修改默认的等待时间

### 2、wait_for_load_state：等待元素处于某种状态

wait_for_load_state函数是用于等待页面加载状态达到指定状态的。这个函数通常在处理页面加载时使用，确保在执行后续操作前，页面已经完成特定的加载阶段。

- `'load'`**：** 等待`load`事件被触发，这个事件在所有资源（包括图像、脚本等）都加载完成后触发，标志着整个页面加载完成。
- **`'domcontentloaded'`：**等待`DOMContentLoaded`事件被触发。这个事件在HTML文档解析完成，DOM树构建完毕（不等待外部资源加载）时触发
- `'networkidle'` **：** **不推荐使用**,  等到至少毫秒没有网络连接。
- **`'commit'`：**在收到网络响应并开始加载文档时完成操作。

### 3、wait_for_url：等待页面跳转到指定的url地址

### 4、wait_for_event：等待事件出现

### 5、wait_for_function: 等待js函数执行的结果为true

### 6、wait_for_timeout:等待指定的时间

### 7、wait_for_selector：等待元素处于某个状态

# 评估 JavaScript

Playwright 脚本在你的 Playwright 环境中运行。你的页面脚本在浏览器页面环境中运行。这些环境并不交叉，它们运行在不同进程的不同虚拟机中，甚至可能运行在不同的计算机上。[page.evaluate()](https://playwright.nodejs.cn/python/docs/api/class-page#page-evaluate) API 可以在网页上下文中运行 JavaScript 函数，并将结果带回 Playwright 环境。像 `window` 和 `document` 这样的浏览器全局变量可以在 `evaluate` 中使用。

```py
href = page.evaluate('() => document.location.href')
```

如果结果是 Promise 或者函数是异步的，则评估将自动等待直到解决：

```py
status = page.evaluate("""async () => {
  response = await fetch(location.href)
  return response.status
}""")
```

## 不同的环境

评估脚本在浏览器环境中运行，而测试在测试环境中运行。这意味着你不能在页面中使用测试中的变量，反之亦然。相反，你应该将它们明确作为参数传递。以下代码片段是错误的，因为它直接使用变量：

```py
data = "some data"
result = page.evaluate("""() => {
  // WRONG: there is no "data" in the web page.
  window.myApp.use(data)
}""")
```

以下代码片段是正确的，因为它将值明确作为参数传递：

```py
data = "some data"
# Pass |data| as a parameter.
result = page.evaluate("""data => {
  window.myApp.use(data)
}""", data)
```

## 评价参数

像 [page.evaluate()](https://playwright.nodejs.cn/python/docs/api/class-page#page-evaluate) 这样的 Playwright 评估方法采用单个可选参数。此参数可以是 [可串行化](https://web.nodejs.cn/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify#Description) 值和 [JSHandle](https://playwright.nodejs.cn/python/docs/api/class-jshandle) 实例的混合。句柄会自动转换为其代表的值。

```py
# A primitive value.
page.evaluate('num => num', 42)

# An array.
page.evaluate('array => array.length', [1, 2, 3])

# An object.
page.evaluate('object => object.foo', { 'foo': 'bar' })

# A single handle.
button = page.evaluate_handle('window.button')
page.evaluate('button => button.textContent', button)

# Alternative notation using JSHandle.evaluate.
button.evaluate('(button, from) => button.textContent.substring(from)', 5)

# Object with multiple handles.
button1 = page.evaluate_handle('window.button1')
button2 = page.evaluate_handle('.button2')
page.evaluate("""o => o.button1.textContent + o.button2.textContent""",
    { 'button1': button1, 'button2': button2 })

# Object destructuring works. Note that property names must match
# between the destructured object and the argument.
# Also note the required parenthesis.
page.evaluate("""
    ({ button1, button2 }) => button1.textContent + button2.textContent""",
    { 'button1': button1, 'button2': button2 })

# Array works as well. Arbitrary names can be used for destructuring.
# Note the required parenthesis.
page.evaluate("""
    ([b1, b2]) => b1.textContent + b2.textContent""",
    [button1, button2])

# Any mix of serializables and handles works.
page.evaluate("""
    x => x.button1.textContent + x.list[0].textContent + String(x.foo)""",
    { 'button1': button1, 'list': [button2], 'foo': None })
```

## 初始化脚本

有时在页面开始加载之前评估页面中的某些内容很方便。例如，你可能需要设置一些模拟或测试数据。

在这种情况下，使用 [page.add_init_script()](https://playwright.nodejs.cn/python/docs/api/class-page#page-add-init-script) 或 [browser_context.add_init_script()](https://playwright.nodejs.cn/python/docs/api/class-browsercontext#browser-context-add-init-script)。在下面的示例中，我们将用常量值替换 `Math.random()`。

首先，创建一个包含模拟的 `preload.js` 文件。

```js
// preload.js
Math.random = () => 42;
```

接下来，将初始化脚本添加到页面。

```py
# In your test, assuming the "preload.js" file is in the "mocks" directory.
page.add_init_script(path="mocks/preload.js")
```

# 事件

Playwright 允许监听网页上发生的各种类型的事件，例如网络请求、子页面创建、专用 worker 等。有几种方法可以订阅此类事件，例如等待事件或添加或删除事件监听器。

大多数时候，脚本需要等待特定事件发生。以下是一些典型的事件等待模式。

使用 [page.expect_request()](https://playwright.net.cn/python/docs/api/class-page#page-wait-for-request) 等待指定 URL 的请求。

```py
with page.expect_request("**/*logo*.png") as first:
  page.goto("https://wikipedia.org")
print(first.value.url)
```

等待弹出窗口

```py
with page.expect_popup() as popup:
  page.get_by_text("open the popup").click()
popup.value.goto("https://wikipedia.org")
```

## 添加/删除事件监听器

有时，事件会在随机时间发生，此时需要处理它们，而不是等待它们。Playwright 支持传统的语言机制来订阅和取消订阅事件。

```py
def print_request_sent(request):
  print("Request sent: " + request.url)

def print_request_finished(request):
  print("Request finished: " + request.url)

page.on("request", print_request_sent)
page.on("requestfinished", print_request_finished)
page.goto("https://wikipedia.org")

page.remove_listener("requestfinished", print_request_finished)
page.goto("https://www.openstreetmap.org/")
```

## 添加一次性监听器

如果某个事件需要处理一次，则为此提供了一个便捷的 API。

```py
page.once("dialog", lambda dialog: dialog.accept("2021"))
page.evaluate("prompt('Enter a number:')")
```

# 事件监听

playwright提供了完善的事件监听机制，通过事件监听机制可以实现一些常用的操作

### 1、`on('close')`: 页面关闭时出发

### 2、`on("console")`:  控制台输入时触发

### 3、`page.on("crash")`:  页面崩溃时触发

### 4、`page.on("dialog")`:  对话框弹出时触发

### 5、`page.on("download")`:   下载事件触发

### 6、`page.on("request")`:   请求事件触发

### 7、`page.on("response")`:   响应事件触发

### 8、`page.on("websocket"):`  监听到websocket请求发送时触发

# 时钟

准确模拟时间相关行为对于验证应用的正确性至关重要。利用 [时钟](https://playwright.nodejs.cn/python/docs/clock#) 功能允许开发者在测试中操纵和控制时间，从而能够精确验证渲染时间、超时、计划任务等功能，而不会出现实时执行的延迟和变化。

[时钟](https://playwright.nodejs.cn/python/docs/clock#) API 提供以下方法来控制时间：

- `setFixedTime`：设置 `Date.now()` 和 `new Date()` 的固定时间。
- `install`：初始化时钟并允许你：
  - `pauseAt`：在特定时间暂停时间。
  - `fastForward`：快进时间。
  - `runFor`：运行特定持续时间的时间。
  - `resume`：恢复时间。
- `setSystemTime`：设置当前系统时间。

推荐的方法是使用 `setFixedTime` 将时间设置为特定值。如果这对你的用例不起作用，你可以使用 `install`，它允许你稍后暂停时间、快进、勾选等。`setSystemTime` 仅推荐用于高级用例。[page.clock](https://playwright.nodejs.cn/python/docs/api/class-page#page-clock) 覆盖与时间相关的原生全局类和函数，允许手动控制它们：

- `Date`
- `setTimeout`
- `clearTimeout`
- `setInterval`
- `clearInterval`
- `requestAnimationFrame`
- `cancelAnimationFrame`
- `requestIdleCallback`
- `cancelIdleCallback`
- `performance`
- `Event.timeStamp`

## 使用预定义时间进行测试

通常，你只需要在保持计时器运行的同时伪造 `Date.now`。这样，时间自然流动，但 `Date.now` 始终返回一个固定值。

```py
page.clock.set_fixed_time(datetime.datetime(2024, 2, 2, 10, 0, 0))
page.goto("http://localhost:3333")
expect(page.get_by_test_id("current-time")).to_have_text("2/2/2024, 10:00:00 AM")
page.clock.set_fixed_time(datetime.datetime(2024, 2, 2, 10, 30, 0))
# We know that the page has a timer that updates the time every second.
expect(page.get_by_test_id("current-time")).to_have_text("2/2/2024, 10:30:00 AM")
```

## 一致的时间和计时器

有时你的计时器依赖于 `Date.now`，当 `Date.now` 值不随时间变化时会感到困惑。在这种情况下，你可以安装时钟并在测试时快进到感兴趣的时间。

```py
# Initialize clock with some time before the test time and let the page load
# naturally. `Date.now` will progress as the timers fire.
page.clock.install(time=datetime.datetime(2024, 2, 2, 8, 0, 0))
page.goto("http://localhost:3333")

# Pretend that the user closed the laptop lid and opened it again at 10am.
# Pause the time once reached that point.
page.clock.pause_at(datetime.datetime(2024, 2, 2, 10, 0, 0))

# Assert the page state.
expect(page.get_by_test_id("current-time")).to_have_text("2/2/2024, 10:00:00 AM")

# Close the laptop lid again and open it at 10:30am.
page.clock.fast_forward("30:00")
expect(page.get_by_test_id("current-time")).to_have_text("2/2/2024, 10:30:00 AM")
```

# 隔离

Playwright 可以在单个场景中创建多个浏览器上下文。当你想要测试多用户功能（例如聊天）时，这非常有用。

```py
from playwright.sync_api import sync_playwright, Playwright

def run(playwright: Playwright):
    # create a chromium browser instance
    chromium = playwright.chromium
    browser = chromium.launch()

    # create two isolated browser contexts
    user_context = browser.new_context()
    admin_context = browser.new_context()

    # create pages and interact with contexts independently

with sync_playwright() as playwright:
    run(playwright)
```

# 页面对象模型

## 介绍

可以构建大型测试套件以优化创作和维护的便利性。页面对象模型是构建测试套件的一种方法。

页面对象代表 Web 应用的一部分。电商 Web 应用可能有主页、列表页面和结账页面。它们中的每一个都可以由页面对象模型来表示。

页面对象通过创建适合你的应用的更高级别 API 来简化创作，通过在一处捕获元素选择器并创建可重用代码以避免重复来简化维护。

## 执行

页面对象模型封装在 Playwright [Page](https://playwright.nodejs.cn/python/docs/api/class-page) 上。

models/search.py

```py
class SearchPage:
    def __init__(self, page):
        self.page = page
        self.search_term_input = page.locator('[aria-label="Enter your search term"]')

    def navigate(self):
        self.page.goto("https://bing.com")

    def search(self, text):
        self.search_term_input.fill(text)
        self.search_term_input.press("Enter")
```

然后可以在测试中使用页面对象。

test_search.py

```py
from models.search import SearchPage

# in the test
page = browser.new_page()
search_page = SearchPage(page)
search_page.navigate()
search_page.search("search query")
```

# 截图和视频

以下是捕获屏幕截图并将其保存到文件中的快速方法：

```py
page.screenshot(path="screenshot.png")
```

[Screenshots API](https://playwright.nodejs.cn/python/docs/api/class-page#page-screenshot) 接受许多图片格式、剪辑区域、质量等参数。请务必检查它们。

## 整页截图

全页屏幕截图是完整可滚动页面的屏幕截图，就好像你有一个非常高的屏幕并且页面可以完全容纳它一样。

```py
page.screenshot(path="screenshot.png", full_page=True)
```

## 录视频

测试结束时 [浏览器上下文](https://playwright.nodejs.cn/python/docs/browser-contexts) 关闭时保存视频。如果你手动创建浏览器上下文，请确保等待 [browser_context.close()](https://playwright.nodejs.cn/python/docs/api/class-browsercontext#browser-context-close)。

```py
context = browser.new_context(record_video_dir="videos/")
# Make sure to close, so that videos are saved.
context.close()
```

你还可以指定视频大小。视频大小默认为缩小到适合 800x800 的视口大小。视口的视频放置在输出视频的左上角，必要时缩小以适合。你可能需要设置视口大小以匹配你所需的视频大小。

```py
context = browser.new_context(
    record_video_dir="videos/",
    record_video_size={"width": 640, "height": 480}
)
```

保存的视频文件将出现在指定的文件夹中。它们都生成了唯一的名称。对于多页面场景，你可以通过 [page.video](https://playwright.nodejs.cn/python/docs/api/class-page#page-video) 访问与页面关联的视频文件。

```py
path = page.video.path()
```

# 代码生成

```
Usage: playwright codegen [options] [url]

open page and generate code for user actions

Options:
  -o, --output <file name>             saves the generated script to a file
  --target <language>                  language to generate, one of javascript, playwright-test, python, python-async, python-pytest, csharp, csharp-mstest, csharp-nunit, java, java-junit (default:
                                       "python")
  --test-id-attribute <attributeName>  use the specified attribute to generate data test ID selectors
  -b, --browser <browserType>          browser to use, one of cr, chromium, ff, firefox, wk, webkit (default: "chromium")
  --block-service-workers              block service workers
  --channel <channel>                  Chromium distribution channel, "chrome", "chrome-beta", "msedge-dev", etc
  --color-scheme <scheme>              emulate preferred color scheme, "light" or "dark"
  --device <deviceName>                emulate device, for example  "iPhone 11"
  --geolocation <coordinates>          specify geolocation coordinates, for example "37.819722,-122.478611"
  --ignore-https-errors                ignore https errors
  --load-storage <filename>            load context storage state from the file, previously saved with --save-storage
  --lang <language>                    specify language / locale, for example "en-GB"
  --proxy-server <proxy>               specify proxy server, for example "http://myproxy:3128" or "socks5://myproxy:8080"
  --proxy-bypass <bypass>              comma-separated domains to bypass proxy, for example ".com,chromium.org,.domain.com"
  --save-har <filename>                save HAR file with all network activity at the end
  --save-har-glob <glob pattern>       filter entries in the HAR by matching url against this glob pattern
  --save-storage <filename>            save context storage state at the end, for later use with --load-storage
  --timezone <time zone>               time zone to emulate, for example "Europe/Rome"
  --timeout <timeout>                  timeout for Playwright actions in milliseconds, no timeout by default
  --user-agent <ua string>             specify user agent string
  --user-data-dir <directory>          use the specified user data directory instead of a new context
  --viewport-size <size>               specify browser viewport size in pixels, for example "1280, 720"
  -h, --help                           display help for command
```

# 验证

Playwright 提供了一种在测试中重用登录状态的方法。这样你只需登录一次，然后跳过所有测试的登录步骤。

```
# Save storage state into the file.
storage = context.storage_state(path="state.json")

# Create a new context with the saved storage state.
context = browser.new_context(storage_state="state.json")
```

# Pytest 插件参考

要运行测试，请使用 [Pytest](https://docs.pytest.org/en/stable/) CLI。

```
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
- `-s` 允许输出print内容

# 打包

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
