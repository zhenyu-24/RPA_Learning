## pytest 特点

pytest 可以用来做 系统测试 的自动化， 它的特点有

- 用 Python 编写测试用例，简便易用
- 可以用 文件系统目录层次 对应 手工测试用例 层次结构
- 灵活的 初始化清除 机制
- 可以灵活挑选测试用例执行
- 利用第三方插件，可以生成不错的报表

## 快速上手

pytest 如何知道你哪些代码是自动化的测试用例？

官方文档 给出了 pytest 寻找 测试项 的 具体规则

- 如果未指定命令行参数，则从 testpath（如果已配置）或当前目录开始收集。

  如果命令行参数， 指定了 目录、文件名 或 node id 的任何组合，则按参数来找

- 寻找过程会递归到目录中，除非它们匹配上 norecursedirs。

- 在这些目录中，搜索由其测试包名称导入的 `test_*.py` 或 `*_test.py` 文件。

- 从这些文件中，收集如下测试项：

  - test为前缀 的 `函数`
  - Test为前缀的 `类` 里面的 test为前缀的方法

### 运行测试

执行测试非常简单，打开命令行窗口，进入自动化项目根目录，执行命令程序 `pytest` 即可

上面的示例执行结果如下

![img](https://www.byhy.net/cdn2/imgs/api/tut_20200626162633_92.png)

显示找到3个测试项，2个执行通过，1个不通过。通过的用例 是用一个绿色小点表示， 不通过的用例用一个红色的F表示。并且会在后面显示具体不通过的用例 和不通过的检查点 代码细节。

**注意**

直接执行 `pytest` 命令不会将当前目录设置为模块搜索路径。所以更推荐 执行命令 `python -m pytest`

如果我们希望 显示测试代码中print的内容，因为这些打印语句在调试代码时很有用，可以加上命令行参数 -s

如下

```undefined
python -m pytest -s
```

如果我们希望得到更详细的执行信息，包括每个测试类、测试函数的名字，可以加上参数 -v，这个参数可以和 -s 合并为 -sv。如下

```undefined
python -m pytest -sv
```

执行 pytest 时， 如果命令行没有指定目标目录 或者 文件， 它会自动搜索当前目录下所有符合条件的文件、类、函数。所以上面，就找到了3个测试方法，对应3个用例。项目根目录 中只有一个cases 目录用例存放测试用例， 将来还会有其他目录，比如：lib目录存放库代码、cfg目录存放配置数据 等等。为了防止 pytest 到其他目录中找测试用例项，执行测试时，我们可以在命令行加上目标目录 cases ，就是这样

```py
python -m pytest cases
```

### 产生报告

前面在安装pytest，我们也安装了 pytest-html 插件，这个插件就是用来产生测试报告的。

要产生报告，在命令行加上 参数 `--html=report.html --self-contained-html` ，如下

```py
python -m pytest cases --html=report.html --self-contained-html
```

这样就会产生名为 report.html 的测试报告文件，可以在浏览器中打开

## 初始化清除

对自动化测试框架来说，初始化清除功能 至关重要。

### 模块级别

`模块级别` 的初始化、清除 分别 在整个模块的测试用例 执行前后执行，并且 `只会执行1次` 。

如下定义 setup_module 和 teardown_module 全局函数

```py
def setup_module():
    print('\n *** 初始化-模块 ***')


def teardown_module():
    print('\n ***   清除-模块 ***')

class Test_错误密码:

    def test_C001001(self):
        print('\n用例C001001')
        assert 1 == 1
        
    def test_C001002(self):
        print('\n用例C001002')
        assert 2 == 2
        
    def test_C001003(self):
        print('\n用例C001003')
        assert 3 == 2


class Test_错误密码2:

    def test_C001021(self):
        print('\n用例C001021')
        assert 1 == 1
        
    def test_C001022(self):
        print('\n用例C001022')
        assert 2 == 2
```

执行命令 `python -m pytest cases -s` ，运行结果如下

```markdown
collected 5 items

cases\登录\test_错误登录.py
 *** 初始化-模块 ***

用例C001001
.
用例C001002
.
用例C001003
F
用例C001021
.
用例C001022
.
 ***   清除-模块 ***
```

可以发现，模块级别的初始化、清除 在 整个模块所有用例 执行前后 分别 `执行1次`

它主要是用来为该 `模块` 中 所有的测试用例做 `公共的` 初始化 和 清除

### 类级别

```
类级别` 的初始化、清除 分别 在整个类的测试用例 执行前后执行，并且 `只会执行1次
```

如下定义 setup_class 和 teardown_class 类方法

```py
def setup_module():
    print('\n *** 初始化-模块 ***')

def teardown_module():
    print('\n ***   清除-模块 ***')

class Test_错误密码:

    @classmethod
    def setup_class(cls):
        print('\n === 初始化-类 ===')

    @classmethod
    def teardown_class(cls):
        print('\n === 清除 - 类 ===')
        
    def test_C001001(self):
        print('\n用例C001001')
        assert 1 == 1
        
    def test_C001002(self):
        print('\n用例C001002')
        assert 2 == 2
        
    def test_C001003(self):
        print('\n用例C001003')
        assert 3 == 2

class Test_错误密码2:

    def test_C001021(self):
        print('\n用例C001021')
        assert 1 == 1
        
    def test_C001022(self):
        print('\n用例C001022')
        assert 2 == 2
```

执行命令 `python -m pytest cases -s` ，运行结果如下

```diff
collected 5 items

cases\登录\test_错误登录.py
 *** 初始化-模块 ***

 === 初始化-类 ===

用例C001001
.
用例C001002
.
用例C001003
F
 === 清除 - 类 ===

用例C001021
.
用例C001022
.
 ***   清除-模块 ***
```

可以发现，类级别的初始化、清除 在 整个类 所有用例 执行前后 分别 `执行1次` 。

它主要是用来为该 `类` 中的所有测试用例做 `公共的` 初始化 和 清除

### 方法级别

方法级别 的初始化、清除 分别 在类的 每个测试方法 执行前后执行，并且 `每个用例分别执行1次`

如下定义 setup_method 和 teardown_method 实例方法

```py
def setup_module():
    print('\n *** 初始化-模块 ***')

def teardown_module():
    print('\n ***   清除-模块 ***')

class Test_错误密码:

    @classmethod
    def setup_class(cls):
        print('\n === 初始化-类 ===')

    @classmethod
    def teardown_class(cls):
        print('\n === 清除 - 类 ===')
        
    def setup_method(self):
        print('\n --- 初始化-方法  ---')

    def teardown_method(self):
        print('\n --- 清除  -方法 ---')
        
    def test_C001001(self):
        print('\n用例C001001')
        assert 1 == 1
        
    def test_C001002(self):
        print('\n用例C001002')
        assert 2 == 2
        
    def test_C001003(self):
        print('\n用例C001003')
        assert 3 == 2

class Test_错误密码2:

    def test_C001021(self):
        print('\n用例C001021')
        assert 1 == 1
        
    def test_C001022(self):
        print('\n用例C001022')
        assert 2 == 2
```

执行命令 `python -m pytest cases -s` ，运行结果如下

```lua
collected 5 items

cases\登录\test_错误登录.py
 *** 初始化-模块 ***

 === 初始化-类 ===

 --- 初始化-方法  ---

用例C001001
.
 --- 清除  -方法 ---

 --- 初始化-方法  ---

用例C001002
.
 --- 清除  -方法 ---

 --- 初始化-方法  ---

用例C001003
F
 --- 清除  -方法 ---

 === 清除 - 类 ===

用例C001021
.
用例C001022
.
 ***   清除-模块 ***
```

可以发现，方法级别的初始化、清除 在 整个模块所有用例 执行前后 分别 `执行一次`

### 目录级别

目标级别的 初始化清除，就是针对整个目录执行的初始化、清除。

我们在需要初始化的目录下面创建 一个名为 `conftest.py` 的文件，里面内容如下所示

```py
import pytest 

@pytest.fixture(scope='package',autouse=True)
def st_emptyEnv():
    print(f'\n#### 初始化-目录甲')
    yield
    
    print(f'\n#### 清除-目录甲')
```

注意：这里清除环境的代码就是 yield 之后的代码。 这是一个生成器。