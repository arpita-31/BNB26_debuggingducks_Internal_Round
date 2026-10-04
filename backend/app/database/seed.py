"""
Seed Data Script for ReLearn
Populates SQLite / Postgres with taxonomy, questions bank, demo student, demo teacher,
class roster, and persistent learner states.
"""
import json
from pathlib import Path
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .db import init_db, SessionLocal
from .models import (
    DBUser, DBMisconception, DBQuestion,
    DBLearnerConcept, DBLearnerMisconception, DBLearnerResponse, DBDiagnosis
)
from app.utils.security import hash_password

def seed_database():
    init_db()
    session: Session = SessionLocal()
    base_dir = Path(__file__).resolve().parent.parent.parent.parent
    data_dir = base_dir / "data"

    try:
        # 1. Seed Misconceptions
        tax_path = data_dir / "misconception_taxonomy.json"
        if tax_path.exists():
            with open(tax_path, "r", encoding="utf-8") as f:
                taxonomies = json.load(f)["taxonomies"]
                for t in taxonomies:
                    existing = session.query(DBMisconception).filter_by(id=t["id"]).first()
                    if not existing:
                        session.add(DBMisconception(
                            id=t["id"],
                            name=t["name"],
                            concept=t["concept"],
                            description=t["description"],
                            recommended_intervention=t.get("recommended_intervention", "")
                        ))

        # 2. Seed Questions
        q_path = data_dir / "questions_bank.json"
        if q_path.exists():
            with open(q_path, "r", encoding="utf-8") as f:
                q_data = json.load(f)
                for q in q_data.get("questions", []):
                    existing = session.query(DBQuestion).filter_by(id=q["id"]).first()
                    if not existing:
                        session.add(DBQuestion(
                            id=q["id"],
                            subject=q.get("subject", "Programming"),
                            topic=q.get("topic", "Python Loops"),
                            concept=q["concept"],
                            target_misconception_id=q.get("target_misconception"),
                            difficulty=q.get("difficulty", "beginner"),
                            title=q["title"],
                            prompt=q["prompt"],
                            code=q.get("code", ""),
                            expected_output=q.get("expected_output", ""),
                            question_type=q.get("question_type", "output_prediction"),
                            explanation=q.get("explanation", ""),
                            tags=q.get("tags", ["python", "loops"]),
                            is_reassessment=False
                        ))
                for q in q_data.get("transfer_reassessment_questions", []):
                    existing = session.query(DBQuestion).filter_by(id=q["id"]).first()
                    if not existing:
                        session.add(DBQuestion(
                            id=q["id"],
                            subject=q.get("subject", "Programming"),
                            topic=q.get("topic", "Python Loops"),
                            concept=q["concept"],
                            target_misconception_id=q.get("target_misconception"),
                            difficulty=q.get("difficulty", "beginner"),
                            title=q["title"],
                            prompt=q["prompt"],
                            code=q.get("code", ""),
                            expected_output=q.get("expected_output", ""),
                            question_type=q.get("question_type", "output_prediction"),
                            explanation=q.get("explanation", ""),
                            tags=q.get("tags", ["reassessment", "transfer"]),
                            is_reassessment=True
                        ))

        # 3. Seed Demo Student ("demo_learner")
        demo_student = session.query(DBUser).filter_by(id="demo_learner").first()
        if not demo_student:
            demo_student = DBUser(
                id="demo_learner",
                username="alex_student",
                email="student@relearn.ai",
                full_name="Alex Rivera",
                role="student",
                hashed_password=hash_password("password123")
            )
            session.add(demo_student)
            session.commit()
        else:
            demo_student.email = "student@relearn.ai"
            demo_student.full_name = "Alex Rivera"
            demo_student.role = "student"
            demo_student.hashed_password = hash_password("password123")
            session.commit()

        # Seed initial concept mastery states for demo_learner if none exist
        if not session.query(DBLearnerConcept).filter_by(user_id="demo_learner").first():
            concepts = [
                ("python_range", 0.38, "LEARNING"),
                ("loop_counting", 0.45, "LEARNING"),
                ("conditionals_assignment", 0.78, "IMPROVING"),
                ("variable_scope", 0.50, "LEARNING"),
                ("recursion", 0.20, "LEARNING"),
                ("mutable_defaults", 0.15, "LEARNING"),
                ("arithmetic_division", 0.85, "MASTERED")
            ]
            for cid, mastery, status in concepts:
                session.add(DBLearnerConcept(
                    user_id="demo_learner",
                    concept_id=cid,
                    mastery=mastery,
                    status=status
                ))

        # Seed initial misconceptions for demo_learner if none exist
        if not session.query(DBLearnerMisconception).filter_by(user_id="demo_learner").first():
            session.add(DBLearnerMisconception(
                user_id="demo_learner",
                misconception_id="M001",
                status="ACTIVE",
                occurrences=2,
                interventions_taken=1,
                reassessments_passed=0,
                confidence=0.91,
                last_detected=datetime.utcnow()
            ))
            session.add(DBLearnerMisconception(
                user_id="demo_learner",
                misconception_id="M002",
                status="IMPROVING",
                occurrences=2,
                interventions_taken=2,
                reassessments_passed=1,
                confidence=0.62,
                last_detected=datetime.utcnow() - timedelta(days=1)
            ))
            session.add(DBLearnerMisconception(
                user_id="demo_learner",
                misconception_id="M003",
                status="RESOLVED",
                occurrences=1,
                interventions_taken=1,
                reassessments_passed=2,
                confidence=0.15,
                last_detected=datetime.utcnow() - timedelta(days=3)
            ))

        # 4. Seed Demo Teacher ("demo_teacher")
        demo_teacher = session.query(DBUser).filter_by(id="demo_teacher").first()
        if not demo_teacher:
            demo_teacher = DBUser(
                id="demo_teacher",
                username="sarah_teacher",
                email="teacher@relearn.ai",
                full_name="Dr. Sarah Chen",
                role="teacher",
                hashed_password=hash_password("password123")
            )
            session.add(demo_teacher)
            session.commit()
        else:
            demo_teacher.email = "teacher@relearn.ai"
            demo_teacher.full_name = "Dr. Sarah Chen"
            demo_teacher.role = "teacher"
            demo_teacher.hashed_password = hash_password("password123")
            session.commit()

        # 5. Seed Additional Class Roster for Teacher Analytics
        additional_students = [
            ("user_002", "jordan@relearn.ai", "jordan_patel", "Jordan Patel", [
                ("python_range", 0.72, "IMPROVING"),
                ("loop_counting", 0.58, "LEARNING"),
                ("conditionals_assignment", 0.90, "MASTERED")
            ], [
                ("M002", "ACTIVE", 3, 1, 0, 0.88),
                ("M001", "RESOLVED", 1, 1, 2, 0.12)
            ]),
            ("user_003", "elena@relearn.ai", "elena_rostova", "Elena Rostova", [
                ("python_range", 0.88, "MASTERED"),
                ("loop_counting", 0.82, "MASTERED"),
                ("variable_scope", 0.85, "MASTERED")
            ], [
                ("M001", "RESOLVED", 2, 2, 2, 0.10),
                ("M004", "RESOLVED", 1, 1, 2, 0.08)
            ]),
            ("user_004", "marcus@relearn.ai", "marcus_vance", "Marcus Vance", [
                ("python_range", 0.42, "LEARNING"),
                ("recursion", 0.30, "LEARNING"),
                ("conditionals_assignment", 0.55, "LEARNING")
            ], [
                ("M003", "ACTIVE", 3, 2, 0, 0.92),
                ("M005", "ACTIVE", 2, 1, 0, 0.85)
            ]),
            ("user_005", "priya@relearn.ai", "priya_sharma", "Priya Sharma", [
                ("python_range", 0.92, "MASTERED"),
                ("recursion", 0.88, "MASTERED"),
                ("variable_scope", 0.91, "MASTERED")
            ], [
                ("M001", "RESOLVED", 1, 1, 2, 0.05),
                ("M005", "RESOLVED", 1, 1, 2, 0.08)
            ])
        ]

        for uid, uemail, uname, ufullname, uconcepts, umisconceptions in additional_students:
            u_obj = session.query(DBUser).filter_by(id=uid).first()
            if not u_obj:
                u_obj = DBUser(
                    id=uid,
                    email=uemail,
                    username=uname,
                    full_name=ufullname,
                    role="student",
                    hashed_password=hash_password("password123")
                )
                session.add(u_obj)
                session.flush()

                for cid, cmastery, cstatus in uconcepts:
                    session.add(DBLearnerConcept(
                        user_id=uid,
                        concept_id=cid,
                        mastery=cmastery,
                        status=cstatus
                    ))

                for mid, mstatus, mocc, mint, mpass, mconf in umisconceptions:
                    session.add(DBLearnerMisconception(
                        user_id=uid,
                        misconception_id=mid,
                        status=mstatus,
                        occurrences=mocc,
                        interventions_taken=mint,
                        reassessments_passed=mpass,
                        confidence=mconf,
                        last_detected=datetime.utcnow() - timedelta(hours=mocc * 3)
                    ))

        session.commit()
        print("Database initialized and successfully seeded.")

    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed_database()
