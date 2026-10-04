"""
Pydantic Request and Response Schemas for ReLearn API
Provides strict type validation and documentation for all API contracts.
"""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

# Auth Schemas
class UserRegisterRequest(BaseModel):
    email: str = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="Password (at least 6 characters)")
    full_name: str = Field(..., description="Full display name")
    role: str = Field(default="student", description="'student' or 'teacher'")

class UserLoginRequest(BaseModel):
    email: str = Field(..., description="User email address")
    password: str = Field(..., description="Password")

# Ingestion Schemas
class SubmissionPayload(BaseModel):
    modality: str = Field(default="text", description="'text', 'code', 'image', or 'audio'")
    text: str = Field(default="", description="Learner natural language explanation")
    code: str = Field(default="", description="Optional code snippet or prediction")
    metadata: Dict[str, Any] = Field(default_factory=dict)

class DiagnoseRequest(BaseModel):
    domain_id: str = Field(default="python_programming")
    question_id: str
    learner_id: str = Field(default="demo_learner")
    submission: SubmissionPayload

class ProbeAnswerRequest(BaseModel):
    probe_id: str
    selected_option_index: int
    learner_id: str = Field(default="demo_learner")

# Intervention Schemas
class InterventionRequest(BaseModel):
    misconception_id: str
    confidence: float = 1.0
    learner_id: str = Field(default="demo_learner")

class MicroPracticeRequest(BaseModel):
    misconception_id: str
    selected_option_index: int

# Reassessment & Resolution Schemas
class ReassessmentRequest(BaseModel):
    misconception_id: str
    original_question_id: Optional[str] = None
    learner_id: str = Field(default="demo_learner")

class ResolutionRequest(BaseModel):
    reassessment_id: str
    misconception_id: str
    concept_id: str = "python_range"
    learner_response: str
    learner_code: str = ""
    learner_id: str = Field(default="demo_learner")

# Teacher Question Creation Schema
class TeacherQuestionCreate(BaseModel):
    subject: str = Field(default="Programming", description="'Programming', 'Mathematics', 'Physics'")
    topic: str = Field(default="Python Loops")
    concept: str = Field(..., description="e.g. python_range, variable_scope")
    target_misconception_id: Optional[str] = Field(default=None, description="e.g. M001")
    difficulty: str = Field(default="beginner", description="'beginner', 'intermediate', 'advanced'")
    title: str = Field(..., description="Question title")
    prompt: str = Field(..., description="Question prompt text")
    code: Optional[str] = Field(default="", description="Accompanying code snippet")
    expected_output: Optional[str] = Field(default="", description="Expected answer / output")
    question_type: str = Field(default="output_prediction", description="'output_prediction', 'code', 'mcq', 'short_answer'")
    assessment_question: Optional[str] = Field(default="", description="Unseen transfer problem")
    explanation: Optional[str] = Field(default="", description="Detailed pedagogical explanation")
    tags: Optional[List[str]] = Field(default_factory=list)

# N8N Orchestration Schemas
class N8NWebhookPayload(BaseModel):
    learner_id: str = Field(default="user_001")
    question_id: str = Field(default="Q001")
    response: str = Field(..., description="Student response text or code")
    response_type: str = Field(default="text", description="'text' or 'code'")
    domain_id: str = Field(default="python_programming")

# Demo Scenarios
class DemoStepRequest(BaseModel):
    scenario_id: str
    step: int
