## Plan: NaiveClaw 本地化桌面控制助手 (对接 LM Studio)

这是一个基于 Python 的精简版桌面代理，通过对接 LM Studio 部署的本地多模态模型 (Qwen3.5-4b-vision) 实现对个人电脑的基本自动化控制。

### 架构设计 (基于 src 目录)
- `src/main.py`: 主控制循环，负责协调视觉捕获、大模型推理和动作执行。
- `src/agent/memory.py`: 类 OpenClaw 记忆系统，用于存取历史成功经验、特定控件坐标缓存或长期上下文。
- `src/agent/llm_client.py`: 对接 LM Studio (OpenAI 兼容 API) 的客户端封装，处理 prompt 构建、图片 Base64 转换和结果解析。
- `src/tools/vision.py`: 负责截屏 (`mss` 或 `PIL`) 与图像预处理（可能需要标注屏幕网格以辅助视觉模型定位）。
- `src/tools/controller.py`: 负责系统键鼠控制 (`pyautogui` 或 `pynput`)。
- `src/tools/commander.py`: 负责执行命令行脚本 (`subprocess`) 并捕获输出。
- `src/tools/web_browser.py`: (可选) 后续集成 Playwright 辅助网页特定元素的获取与控制。

### 核心执行流 (Loop)
1. 捕获当前屏幕 (vision) -> 转为 Base64。
2. 从记忆系统 (memory) 中检索与当前任务相关的历史上下文、成功路径或控件坐标。
3. 将 "用户的目标/任务" + "检索到的记忆" + "当前屏幕信息" + "支持的动作列表(Tools)" 发送给 LM Studio。
4. 解析 LM Studio 返回的带有特定动作指令 (如 `CLICK(x,y)`, `TYPE(text)`, `CMD(ls -l)`, `MEM_SAVE(key, value)`) 的文本。
5. 调用对应的本地工具执行动作，并根据指令更新记忆库。
6. 等待短暂延迟后进入下一次循环，直到目标完成。

### 文档记录 (基于 docs 目录)
- `docs/requirements.md`: 需求与依赖详述。
- `docs/architecture.md`: 系统详细架构规范。
- `docs/plan.md`: 项目执行计划。
