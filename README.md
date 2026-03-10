# NaiveClaw

NaiveClaw 是一个基于 Python 的精简版桌面代理（Desktop Agent）。它通过对接部署在 **LM Studio** 上的本地多模态大语言模型（如 `qwen3.5-4b-vision` 等），实现对个人电脑的自动化基础交互控制，模拟出一个本地运行、轻量级的类 OpenClaw 控制器。

## 🎯 核心特性

- **纯本地化**：通过兼容 OpenAI API 标准的本地推断端（LM Studio）运行视觉决策，彻底告别云端隐私泄漏风险。
- **视觉反馈的自主控制**：Agent 依靠截屏 (`vision`) 判断视觉元素，并生成下一步的动作意图。
- **轻便的执行引擎**：包含鼠标/键盘点击输入 (`controller`)、命令行系统控制 (`commander`) 等工具集。
- **面向后续扩展的设计**：可无缝集成 Playwright 等高级模块进行更精微的组件控制，或随时挂载用户自定义的 Python 工具脚本（Skill 热插拔）。

## 🏗 应用架构

项目划分为以下逻辑层结构：
```text
NaiveClaw/
├── docs/                     # 架构设计、项目计划与需求文档
├── src/
│   ├── main.py               # 主核心执行循环 (Event Loop)
│   ├── agent/
│   │   └── llm_client.py     # 封装与 LM Studio/OpenAI 兼容后端的网通请求逻辑
│   └── tools/
│       ├── commander.py      # 系统终端命令行沙盒工具
│       ├── controller.py     # 键鼠动作执行器工具
│       └── vision.py         # 屏幕快照与图像预处理工具
├── tests/                    # 单元测试模块
├── requirements.txt          # Python 依赖项管理
└── README.md
```

## 🛠 依赖与安装

项目依赖于 Python 3.9+，核心第三方库为：
- `openai`: 管理和构建标准化 Prompt，传输 Base64 给大模型。
- `mss` & `Pillow` : 对本地电脑进行低延迟截屏和高效图片压缩。
- `pyautogui`: 模拟物理键鼠交互。

### 安装步骤

1. 克隆代码到本地：
   ```bash
   git clone https://github.com/your-username/NaiveClaw.git
   cd NaiveClaw
   ```

2. 安装要求依赖：
   ```bash
   pip install -r docs/requirements.md
   ```
   *(或者直接使用: `pip install openai mss pillow pyautogui python-dotenv`)*

## 🚀 使用指南

首先，请确保您已经在后台运行了 [LM Studio](https://lmstudio.ai/)，同时加载了支持视觉 (`vision`) 能力的模型（例如 `Qwen3.5-4b-vision`）。
启动 Local Inference Server（服务默认监听 `http://localhost:1234/v1`）。

随后在终端执行项目入口开启 Agent：

```bash
python src/main.py --goal "打开记事本，输入Hello NaiveClaw并最小化窗口"
```

你可以通过传入 `--steps` 参数来限制 Agent 的最大自主行动步数（默认为 `15`）：

```bash
python src/main.py --goal "请帮我清空回收站" --steps 10
```

## ⚠️ 安全警告

**本项目包含 `CMD` 终端命令行自动化执行能力。**  
为了保护您的系统不被大模型的幻觉误操作，目前在执行涉及到操作系统文件修改等核心指令时，均可能伴随重大风险。如果是关键环境，使用前建议于 `src/tools/commander.py` 或者 `main.py` 中为 `CMD` 的执行增加一道人为的控制台确认 (Human-in-the-loop)。 

## 📜 许可证

MIT License
