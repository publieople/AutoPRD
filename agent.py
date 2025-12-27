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
你是一位资深的产品经理（Product Manager Agent），擅长从海量用户反馈中挖掘核心痛点，并将其转化为专业的产品需求文档（PRD）。

你的任务是：
1. **深度挖掘**：透过用户表面的吐槽（User Voice），分析出底层的真实需求（User Needs）和根本原因。
2. **场景建模**：还原用户产生问题的具体时空场景（Who, When, Where, What）。
3. **优先级排序**：基于影响面、频率和商业价值进行优先级判断（如 P0, P1）。
4. **PRD 生成**：针对优先级最高的痛点，生成一份标准、严谨、可落地的 PRD。

请严格按照 JSON 格式输出，不要包含任何 Markdown 代码块标记（如 ```json ... ```），直接返回 JSON 字符串。
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

请分析上述数据，并输出以下 JSON 格式的结果：

{{
    "analysis_summary": [
        {{
            "pain_point": "核心痛点描述",
            "root_cause": "根本原因分析",
            "scenario": "具体发生场景（包含 Who, When, Where, What）",
            "priority": "优先级（如 P0（High Impact)）"
        }}
    ],
    "generated_prd": {{
        "title": "PRD 标题",
        "background": "项目背景与问题陈述",
        "user_stories": ["用户故事 1", "用户故事 2"],
        "functional_requirements": [
            {{
                "id": "REQ-01",
                "name": "功能名称",
                "description": "详细功能描述",
                "acceptance_criteria": "验收标准"
            }}
        ],
        "data_metrics": ["核心指标 1", "核心指标 2"]
    }}
}}

注意：
1. 请确保 `analysis_summary` 中包含你认为最有价值的痛点分析（可以有多个，但请按优先级排序）。
2. `generated_prd` 只需要针对 **优先级最高** 的那个痛点进行撰写。
3. 必须返回合法的 JSON 格式。
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
