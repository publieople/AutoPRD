# 产品经理 Agent：用户痛点和应用场景挖掘，输出需求文档

背景与价值

## 场景故事

PM 小美负责一款 ToC 的移动应用。每天，她都会收到来自 App Store 评论、客服聊天记录、社群反馈等成百上千条碎片化信息。

有的用户在吐槽“登录太慢”，有的用户建议“增加深色模式”，还有的用户只是单纯的情绪宣泄。

小美不仅要从这些海量噪音中提取出有效的**“用户痛点”，还要分析痛点背后的“典型场景”，判断优先级，并最终将其转化为开发可执行的“产品需求文档(PRD)”**。

她迫切需要一个 “PM Agent 助手”， 能像资深产品经理一样思考， 自动完成 “数据清洗 -> 痛点挖掘 -> 场景建模 -> PRD 生成” 的全流程。

## 为什么选这个场景

- 核心能力考察：区别于简单的文本摘要，本题要求 Agent 具备 “逻辑推理” 与 “商业洞察” 能力，需区分 “表面需求” 与 “深层动机”。

真实工作流：模拟真实互联网产品迭代流程，考察 AI 在复杂职场任务中的落地价值。

- 结构化输出：考察 Agent 将非结构化自然语言转化为高度结构化、工程化文档（PRD）的能力。
  考察点

<table><tr><td>维度</td><td>考察内容</td></tr><tr><td>洞察深度</td><td>能否透过用户表述（User Voice）挖掘出底层动机（User Needs）。</td></tr><tr><td>场景建模</td><td>能否还原用户产生问题的具体时空场景（Context &amp; Scenario）。</td></tr><tr><td>决策逻辑</td><td>能够基于频率、影响面和商业价值对需求进行优先级排序 (ICE/RISE 模型)。</td></tr><tr><td>文档规范</td><td>生成的 PRD 是否符合行业标准，逻辑闭环，无歧义。</td></tr></table>

## 任务定义

输入：

1. 多源用户反馈数据（包含来源、内容、用户画像标签等）。

2. 产品基础背景（产品定位、当前核心功能列表）。

输出：

1. 痛点分析报告：识别出的核心痛点、发生场景、优先级。

2. 标准 PRD 文档：针对优先级最高的痛点生成的完整需求文档。

## 输入格式

```javascript
{
  "product_info": {
    "name": "HealthTrack Pro",
    "description": "一款专注于跑步和饮食记录的健康管理 App。"
  },
  "feedback_data": [
    {
      "id": "F001",
      "source": "AppStore Review",
      "user_level": "VIP",
      "content": "每次跑完步想分享到朋友圈，生成的长图都要加载半天，太扫兴了，不想发了。"
    },
    {
      "timestamp": "2024-05-20 08:30"
    }
  ],
  {
    "id": "F002",
    "source": "Customer Service",
    "user_level": "New User",
    "content": "找不到哪里记录早餐的热量，功能藏得太深。",
    "timestamp": "2024-05-20 09:15"
  },
  {
    "id": "F003",
    "source": "User Interview",
    "user_level": "Active",
    "content": "希望能有个功能自动识别我的食物热量，手动输入太累了，坚持不下来。",
    "timestamp": "2024-05-20 10:00"
  }
}
```

## 输出格式

选手需提交 outputs/prd \_ result.md 或 json。

## prd \_ result.json 示例:

```python
代码块

1     {
2       "analysis_summary": [
```

```javascript
{
    "pain_point": "分享流程体验差，导致用户传播意愿中断",
    "root_cause": "图片生成性能瓶颈，缺乏即时反馈",
    "scenario": "用户刚完成高强度运动，多巴胺分泌高，渴望即时获得社交认同。",
    "priority": "P0（High Impact)"
},
"generated_prd": {
    "title": "跑步记录分享流程优化",
    "background": "当前分享长图生成耗时过长（>5s），造成 30% 用户在分享页流失，影响自然新增。",
    "user_stories": [
        "作为一名跑者，我希望跑完立即看到精美战报，以便快速发朋友圈炫耀。"
    ],
    "functional_requirements": [
        {
            "id": "REQ-01",
            "name": "异步预加载机制",
            "description": "在用户跑步结束点击停止时，后台静默预生成默认模板图片。",
            "acceptance_criteria": "用户进入分享页时，图片需在 1s 内展示。"
        }
    ],
    "data_metrics": ["分享成功率", "分享页面停留时长"]
}
```

## 内容规范

## • 深层挖掘：

Bad Case: 用户说 “加载慢”， Agent 建议 “优化服务器”。

Good Case: Agent 分析出 “加载慢” 导致了 “社交炫耀心理受挫”，建议优先优化 “首屏渲染” 或提供 “简易版快速分享”。

- 场景描述：必须包含 Who (谁)、When (什么时机)、Where (在什么界面/环境下)、What (遇到了什么阻碍)。

PRD 完整性：输出的 PRD 必须包含：背景 (Background)、用户故事 (User Stories)、功能需求 (Functional ReqS)、验收标准 (Acceptance Criteria)。

## 评分标准（100 分）

<table><tr><td>维度</td><td>分值</td><td>说明</td></tr><tr><td>痛点归因准确度</td><td>30</td><td>能准确认别 feedback 中的核心矛盾，不被情绪化语言误导。</td></tr><tr><td>场景建模能力</td><td>20</td><td>能夠構建出真實、具體的用戶使用場景，而非泛泛而談。</td></tr><tr><td>解决方案可行性</td><td>20</td><td>提出的功能需求在技术和商业上是合理的，非天马行空。</td></tr><tr><td>PRD 结构规范</td><td>30</td><td>文档结构严谨，字段齐全，可直接交付给开发人员阅读。</td></tr></table>

## 难度梯度

<table><tr><td>等级</td><td>目标分</td><td>达成条件</td></tr><tr><td>入门</td><td>60分</td><td>能对用户反馈进行分类（如：Bug、建议、咨询），并生成简单的功能列表。</td></tr><tr><td>进阶</td><td>80分</td><td>能识别高价值痛点，按照标准格式输出 PRD，包含基本的用户故事。</td></tr><tr><td>挑战</td><td>95分+</td><td>能结合用户画像进行差异化分析，挖掘出潜在的创新机会（而不仅仅是修 Bug），并定义出完善的数据埋点指标。</td></tr></table>
