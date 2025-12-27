import os
import json
from typing import Any, Dict
from openai import OpenAI
from loguru import logger
from dotenv import load_dotenv
from schema import InputData, OutputData

load_dotenv()

# Configuration
API_KEY = os.getenv("API_KEY") or os.getenv("DEEPSEEK_API_KEY")
BASE_URL = os.getenv("BASE_URL") or os.getenv("DEEPSEEK_BASE_URL") or "https://api.deepseek.com"
MODEL_NAME = os.getenv("MODEL_NAME") or "deepseek-chat"

if not API_KEY:
    logger.warning("API_KEY not found in environment variables. Please set it in .env file.")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

SYSTEM_PROMPT = """
你是一位世界级的产品经理（Product Manager Agent），拥有敏锐的商业洞察力和逻辑推理能力。你的目标不仅仅是修复 Bug，而是通过深度挖掘用户反馈，发现产品创新的机会。

你的核心能力：
1.  **深度洞察 (Deep Insight)**：
    -   透过用户表面的吐槽（User Voice），挖掘底层的真实需求（User Needs）和心理动机（Psychological Motivation）。
    -   例如：用户抱怨“加载慢”，深层动机可能是“社交炫耀心理受挫”（急于分享成就）。
2.  **差异化分析 (Differentiated Analysis)**：
    -   结合用户画像（User Persona/Level）进行分析。VIP 用户的痛点可能关乎尊贵感/效率，新用户的痛点可能关乎易用性/引导。
3.  **场景建模 (Scenario Modeling)**：
    -   还原用户产生问题的具体时空场景，必须包含：Who（谁）、When（什么时机）、Where（在什么界面/环境下）、What（遇到了什么阻碍）。
4.  **创新思维 (Innovation)**：
    -   不要只做“头痛医头”的修补，要思考是否有更好的交互方式或创新功能来彻底解决问题。
5.  **结构化输出 (Structured Output)**：
    -   生成符合行业标准的 PRD，逻辑闭环，无歧义。

请严格按照 JSON 格式输出，不要包含任何 Markdown 代码块标记。
"""

def construct_user_prompt(data: InputData) -> str:
    feedback_text = "\n".join([
        f"- ID: {item.id}, 用户等级: {item.user_level}, 来源: {item.source}, 内容: {item.content}"
        for item in data.feedback_data
    ])

    prompt = f"""
产品信息：
- 名称：{data.product_info.name}
- 描述：{data.product_info.description}

用户反馈数据：
{feedback_text}

请执行以下分析步骤（思维链）：
1.  **用户画像分析**：分析不同等级用户（VIP vs New vs Active）的关注点差异。
2.  **痛点挖掘**：识别核心矛盾。区分“情绪宣泄”与“真实痛点”。
3.  **深层归因**：分析痛点背后的技术瓶颈和用户心理（如：社交认同、掌控感缺失）。
4.  **场景还原**：构建具体的 User Story 场景。
5.  **解决方案构思**：提出 MVP 方案和长期创新方案。
6.  **优先级评估**：基于 ICE 模型（Impact, Confidence, Ease）或 RISE 模型排序。

请输出以下 JSON 格式的结果：

{{
    "analysis_summary": [
        {{
            "pain_point": "核心痛点描述（简洁有力）",
            "root_cause": "根本原因（技术/产品逻辑）",
            "underlying_motivation": "深层动机（心理/社交需求，如：渴望即时反馈、社交炫耀）",
            "scenario": "具体场景：Who(用户角色) + When(时间/触发点) + Where(界面/环境) + What(操作与阻碍)",
            "innovation_opportunity": "创新机会（如何超越预期解决问题，而非仅修复Bug）",
            "priority": "优先级（如 P0 - High Impact, P1 - Medium Impact）"
        }}
    ],
    "generated_prd": {{
        "title": "PRD 标题（针对最高优先级痛点）",
        "background": "背景与问题陈述（引用具体数据或场景，说明为什么要做这个）",
        "user_stories": [
            "As a <Role>, I want to <Action>, so that <Benefit>."
        ],
        "functional_requirements": [
            {{
                "id": "REQ-01",
                "name": "功能名称",
                "description": "详细功能描述（逻辑清晰）",
                "acceptance_criteria": "验收标准（可测试，包含性能指标）"
            }}
        ],
        "data_metrics": [
            "核心指标 1（如：分享成功率、首屏加载耗时）",
            "过程指标 2（如：分享页停留时长、功能点击率）"
        ]
    }}
}}

注意：
1.  `analysis_summary` 需包含所有识别出的有效痛点。
2.  `generated_prd` 仅针对 **优先级最高 (P0)** 的痛点。
3.  **数据指标** 必须具体且具有指导意义。
"""
    return prompt

def run_agent(input_data: InputData) -> OutputData:
    logger.info(f"Starting analysis for product: {input_data.product_info.name}")

    user_prompt = construct_user_prompt(input_data)

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.2
        )

        content = response.choices[0].message.content
        logger.info("Received response from LLM")
        logger.debug(f"Raw response: {content}")

        # Clean content if it contains markdown code blocks
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]

        content = content.strip()

        # Parse JSON
        try:
            json_data = json.loads(content)
            output = OutputData(**json_data)
            return output
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}")
            raise
        except Exception as e:
            logger.error(f"Validation error: {e}")
            raise

    except Exception as e:
        logger.error(f"Error during LLM call: {e}")
        raise
