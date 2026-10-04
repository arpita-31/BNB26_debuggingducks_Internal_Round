"""
SQLAlchemy Database Models for ReLearn
Defines schema for users, questions, misconceptions, attempts,
diagnoses, interventions, and persistent learner state.
"""
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class DBUser(Base):
    __tablename__ = "users"

    id = Column(String(50), primary_key=True)
    username = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=True)
    full_name = Column(String(120), nullable=True)
    role = Column(String(20), default="student")  # "student" or "teacher"
    hashed_password = Column(String(256), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    responses = relationship("DBLearnerResponse", back_populates="user")
    concept_states = relationship("DBLearnerConcept", back_populates="user")
    misconception_states = relationship("DBLearnerMisconception", back_populates="user")

class DBMisconception(Base):
    __tablename__ = "misconceptions"

    id = Column(String(20), primary_key=True)  # e.g., M001
    name = Column(String(150), nullable=False)
    concept = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    recommended_intervention = Column(String(100))

class DBQuestion(Base):
    __tablename__ = "questions"

    id = Column(String(50), primary_key=True)
    subject = Column(String(50), default="Programming")  # "Programming", "Mathematics", "Physics"
    topic = Column(String(100), default="Python Loops")
    concept = Column(String(150), nullable=False)
    target_misconception_id = Column(String(20))
    difficulty = Column(String(20), default="beginner")
    title = Column(String(200), nullable=False)
    prompt = Column(Text, nullable=False)
    code = Column(Text, default="")
    expected_output = Column(Text, default="")
    question_type = Column(String(30), default="output_prediction")  # "output_prediction", "code", "mcq", "short_answer"
    assessment_question = Column(Text, default="")
    explanation = Column(Text, default="")
    tags = Column(JSON, default=list)
    is_reassessment = Column(Boolean, default=False)

class DBLearnerResponse(Base):
    __tablename__ = "learner_responses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), ForeignKey("users.id"), nullable=False)
    question_id = Column(String(50), ForeignKey("questions.id"), nullable=False)
    modality = Column(String(20), default="text")
    text_content = Column(Text, default="")
    code_content = Column(Text, default="")
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("DBUser", back_populates="responses")
    diagnosis = relationship("DBDiagnosis", back_populates="response", uselist=False)

class DBDiagnosis(Base):
    __tablename__ = "diagnoses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    response_id = Column(Integer, ForeignKey("learner_responses.id"), nullable=False)
    predicted_misconception_id = Column(String(20), nullable=False)
    confidence = Column(Float, nullable=False)
    margin = Column(Float, default=0.0)
    is_ambiguous = Column(Boolean, default=False)
    evidence = Column(JSON, default=list)
    timestamp = Column(DateTime, default=datetime.utcnow)

    response = relationship("DBLearnerResponse", back_populates="diagnosis")

class DBIntervention(Base):
    __tablename__ = "interventions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), ForeignKey("users.id"), nullable=False)
    misconception_id = Column(String(20), nullable=False)
    intervention_type = Column(String(50), nullable=False)
    completed = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class DBLearnerConcept(Base):
    __tablename__ = "learner_concepts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), ForeignKey("users.id"), nullable=False)
    concept_id = Column(String(100), nullable=False)
    mastery = Column(Float, default=0.0)  # 0.0 to 1.0
    status = Column(String(30), default="UNKNOWN")  # UNKNOWN, LEARNING, IMPROVING, MASTERED
    last_updated = Column(DateTime, default=datetime.utcnow)

    user = relationship("DBUser", back_populates="concept_states")

class DBLearnerMisconception(Base):
    __tablename__ = "learner_misconceptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), ForeignKey("users.id"), nullable=False)
    misconception_id = Column(String(20), nullable=False)
    status = Column(String(30), default="UNKNOWN")  # UNKNOWN, SUSPECTED, ACTIVE, IMPROVING, PARTIALLY_RESOLVED, RESOLVED, RECURRING
    occurrences = Column(Integer, default=0)
    interventions_taken = Column(Integer, default=0)
    reassessments_passed = Column(Integer, default=0)
    confidence = Column(Float, default=0.0)
    last_detected = Column(DateTime, default=datetime.utcnow)

    user = relationship("DBUser", back_populates="misconception_states")

class DBModelMetrics(Base):
    __tablename__ = "model_metrics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow)
