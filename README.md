# AutoPRD - 智能产品经理 Agent (DeepSeek-V3.2)

## 1. 项目简介

本项目是“胜算云国产多模型实战 PK 大赛” **Level 3 赛题：产品经理 Agent** 的参赛作品。
项目基于 **DeepSeek-V3.2** 模型构建，旨在模拟资深产品经理的工作流，自动化完成从“用户反馈”到“标准 PRD 文档”的转化过程。

### 核心能力

- **深度洞察**: 透过用户碎片化反馈挖掘底层动机（User Needs）。
- **场景建模**: 还原用户痛点发生的具体时空场景（Context & Scenario）。
- **科学决策**: 基于 ICE/RISE 模型对需求进行优先级排序。
- **标准输出**: 生成符合行业规范的结构化 PRD 文档。

## 2. 技术栈

- **核心模型**: DeepSeek-V3.2 (通过胜算云 API 调用)
- **开发语言**: Python 3.10+
- **框架/工具**:
  - **包管理**: uv
  - **LLM SDK**: openai (兼容 DeepSeek API)
  - **数据处理**: pandas, pydantic
  - _注：本项目严格遵守单模型约束，核心逻辑仅调用 DeepSeek-V3.2。_

## 3. 项目结构

```
AutoPRD/
├── agent/                  # 核心代码目录
│   ├── __init__.py
│   ├── core.py             # Agent 主逻辑类
│   ├── prompts.py          # Prompt 模板管理
│   ├── utils.py            # 工具函数
│   └── models.py           # 数据模型定义
├── data/                   # 数据存储
│   ├── input/              # 输入数据 (feedback.json)
│   └── output/             # 输出结果 (prd_result.json/md)
├── docs/                   # 项目文档
│   ├── requirements_analysis.md # 需求分析
│   ├── system_design.md         # 系统设计
│   └── data_schema.md           # 数据规范
├── main.py                 # 程序启动入口
├── pyproject.toml          # 项目配置与依赖
├── uv.lock                 # 依赖锁定文件
├── .env.example            # 环境变量示例
└── README.md               # 项目说明
```

## 4. 快速开始

### 环境准备

本项目使用 `uv` 进行依赖管理。

1. **安装 uv** (如果尚未安装):

    ```bash
    # Windows (PowerShell)
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

    # macOS/Linux
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2. **初始化环境**:

    ```bash
    uv sync
    ```

3. **配置环境变量**:
    复制 `.env.example` 为 `.env` 并填入 API Key。

    ```bash
    cp .env.example .env
    ```

### 运行项目

```bash
uv run main.py
```
