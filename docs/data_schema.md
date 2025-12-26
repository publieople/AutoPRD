# 数据规范文档 (Data Schema)

## 1. 输入数据规范 (Input Schema)

文件: `data/input/feedback.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "product_info": {
      "type": "object",
      "properties": {
        "name": { "type": "string", "description": "产品名称" },
        "description": {
          "type": "string",
          "description": "产品一句话介绍/定位"
        }
      },
      "required": ["name", "description"]
    },
    "feedback_data": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string", "description": "反馈唯一标识" },
          "source": { "type": "string", "description": "反馈来源渠道" },
          "user_level": { "type": "string", "description": "用户等级/类型" },
          "content": { "type": "string", "description": "反馈具体内容" },
          "timestamp": { "type": "string", "description": "反馈时间" }
        },
        "required": ["id", "content"]
      }
    }
  },
  "required": ["product_info", "feedback_data"]
}
```

## 2. 输出数据规范 (Output Schema)

文件: `data/output/prd_result.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "analysis_summary": {
      "type": "object",
      "description": "痛点分析摘要 (针对 Top 1)",
      "properties": {
        "pain_point": { "type": "string", "description": "核心痛点描述" },
        "root_cause": { "type": "string", "description": "根本原因分析" },
        "scenario": { "type": "string", "description": "用户场景还原" },
        "priority": {
          "type": "string",
          "description": "优先级评级 (e.g., P0, P1)"
        },
        "rationale": { "type": "string", "description": "优先级评定理由" }
      },
      "required": ["pain_point", "root_cause", "scenario", "priority"]
    },
    "generated_prd": {
      "type": "object",
      "description": "生成的 PRD 文档结构",
      "properties": {
        "title": { "type": "string", "description": "需求文档标题" },
        "background": { "type": "string", "description": "项目背景与现状" },
        "user_stories": {
          "type": "array",
          "items": { "type": "string" },
          "description": "用户故事列表"
        },
        "functional_requirements": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": { "type": "string", "description": "需求ID (REQ-XX)" },
              "name": { "type": "string", "description": "功能名称" },
              "description": {
                "type": "string",
                "description": "详细功能描述"
              },
              "acceptance_criteria": {
                "type": "string",
                "description": "验收标准"
              }
            },
            "required": ["id", "name", "description", "acceptance_criteria"]
          }
        },
        "data_metrics": {
          "type": "array",
          "items": { "type": "string" },
          "description": "关键数据指标"
        }
      },
      "required": [
        "title",
        "background",
        "user_stories",
        "functional_requirements"
      ]
    }
  },
  "required": ["analysis_summary", "generated_prd"]
}
```
