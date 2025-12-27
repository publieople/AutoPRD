from typing import List, Optional
from pydantic import BaseModel, Field

class ProductInfo(BaseModel):
    name: str
    description: str

class FeedbackItem(BaseModel):
    id: str
    source: str
    user_level: str
    content: str
    timestamp: Optional[str] = None

class InputData(BaseModel):
    product_info: ProductInfo
    feedback_data: List[FeedbackItem]

class PainPoint(BaseModel):
    pain_point: str = Field(..., description="核心痛点")
    root_cause: str = Field(..., description="根本原因 (Technical & Product)")
    underlying_motivation: str = Field(..., description="深层动机 (Psychological & Social)")
    scenario: str = Field(..., description="发生场景 (Who, When, Where, What)")
    innovation_opportunity: str = Field(..., description="创新机会 (Beyond just fixing bugs)")
    priority: str = Field(..., description="优先级 (e.g., P0, P1)")

class FunctionalRequirement(BaseModel):
    id: str
    name: str
    description: str
    acceptance_criteria: str

class GeneratedPRD(BaseModel):
    title: str
    background: str
    user_stories: List[str]
    functional_requirements: List[FunctionalRequirement]
    data_metrics: List[str]

class OutputData(BaseModel):
    analysis_summary: List[PainPoint]
    generated_prd: GeneratedPRD
