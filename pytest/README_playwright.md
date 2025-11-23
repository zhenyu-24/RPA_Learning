## ⚙️ CLI 参数说明

### 浏览器控制
```bash
# 以有头模式运行测试（默认：无头模式）
pytest --headed

# 在多浏览器中运行测试
pytest --browser chromium --browser firefox --browser webkit

# 使用特定浏览器渠道
pytest --browser-channel chrome

# 模拟移动设备
pytest --device "iPhone 12"
```

### 调试功能
```bash
# 减慢操作速度（毫秒），便于观察
pytest --slowmo 1000

# 记录 Trace 信息
pytest --tracing on
pytest --tracing retain-on-failure    # 仅在失败时保留

# 录制视频
pytest --video on
pytest --video retain-on-failure      # 仅在失败时保留

# 自动截图
pytest --screenshot on
pytest --screenshot only-on-failure   # 仅在失败时截图

# 整页截图（需要先启用 --screenshot）
pytest --screenshot on --full-page-screenshot on

# 指定工件输出目录
pytest --output artifacts
```