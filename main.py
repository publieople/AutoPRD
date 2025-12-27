import json
import os
from pathlib import Path
from loguru import logger
from schema import InputData, OutputData
from agent import run_agent

def load_input(file_path: str) -> InputData:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return InputData(**data)

def save_json_output(output: OutputData, file_path: str):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(output.model_dump_json(indent=2, ensure_ascii=False))

def save_markdown_output(output: OutputData, file_path: str):
    prd = output.generated_prd
    md_content = f"# {prd.title}\n\n"

    md_content += "## 1. 背景与问题 (Background)\n\n"
    md_content += f"{prd.background}\n\n"

    md_content += "## 2. 痛点分析 (Pain Point Analysis)\n\n"
    # Assuming the first one is the one we generated PRD for, or list all
    for idx, pp in enumerate(output.analysis_summary):
        md_content += f"### 痛点 {idx+1}: {pp.pain_point}\n\n"
        md_content += f"- **根本原因**: {pp.root_cause}\n"
        md_content += f"- **深层动机**: {pp.underlying_motivation}\n"
        md_content += f"- **场景**: {pp.scenario}\n"
        md_content += f"- **创新机会**: {pp.innovation_opportunity}\n"
        md_content += f"- **优先级**: {pp.priority}\n\n"

    md_content += "## 3. 用户故事 (User Stories)\n\n"
    for story in prd.user_stories:
        md_content += f"- {story}\n"
    md_content += "\n"

    md_content += "## 4. 功能需求 (Functional Requirements)\n\n"
    for req in prd.functional_requirements:
        md_content += f"### {req.id} - {req.name}\n\n"
        md_content += f"**描述**: {req.description}\n\n"
        md_content += f"**验收标准**: {req.acceptance_criteria}\n\n"

    md_content += "## 5. 数据指标 (Data Metrics)\n\n"
    for metric in prd.data_metrics:
        md_content += f"- {metric}\n"

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

def main():
    input_path = "input.json"
    output_json_path = "outputs/prd_result.json"
    output_md_path = "outputs/prd_result.md"

    if not os.path.exists(input_path):
        logger.error(f"Input file not found: {input_path}")
        return

    try:
        logger.info("Loading input data...")
        input_data = load_input(input_path)

        logger.info("Running Product Manager Agent...")
        output_data = run_agent(input_data)

        logger.info("Saving outputs...")
        save_json_output(output_data, output_json_path)
        save_markdown_output(output_data, output_md_path)

        logger.success(f"Successfully generated PRD! Check {output_json_path} and {output_md_path}")

    except Exception as e:
        logger.exception(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
