"""
Persistent Learner Model Engine for ReLearn
Manages learner profiles, concept mastery vectors, state transitions,
and persistence to SQLite.
"""
from typing import Dict, Any, List
from datetime import datetime
from sqlalchemy.orm import Session

from app.database.db import SessionLocal
from app.database.models import (
    DBUser, DBLearnerConcept, DBLearnerMisconception,
    DBLearnerResponse, DBDiagnosis
)
from .state_machine import state_machine

class LearnerModelEngine:
    def get_or_create_learner(self, learner_id: str, session: Session) -> DBUser:
        learner = session.query(DBUser).filter_by(id=learner_id).first()
        if not learner:
            learner = DBUser(id=learner_id, username=f"Learner {learner_id}")
            session.add(learner)
            session.commit()
        return learner

    def record_diagnosis(
        self,
        learner_id: str,
        question_id: str,
        misconception_id: str,
        confidence: float,
        evidence: List[str]
    ) -> Dict[str, Any]:
        """Updates persistent state when a misconception is diagnosed."""
        session: Session = SessionLocal()
        try:
            self.get_or_create_learner(learner_id, session)

            if misconception_id != "NONE":
                misc_record = session.query(DBLearnerMisconception).filter_by(
                    user_id=learner_id, misconception_id=misconception_id
                ).first()

                if not misc_record:
                    misc_record = DBLearnerMisconception(
                        user_id=learner_id,
                        misconception_id=misconception_id,
                        occurrences=1,
                        status="SUSPECTED",
                        confidence=confidence,
                        last_detected=datetime.utcnow()
                    )
                    session.add(misc_record)
                else:
                    misc_record.occurrences += 1
                    misc_record.confidence = confidence
                    misc_record.last_detected = datetime.utcnow()
                    misc_record.status = state_machine.transition_on_diagnosis(
                        current_state=misc_record.status,
                        confidence=confidence,
                        occurrences=misc_record.occurrences
                    )

            session.commit()
            return {"status": "SUCCESS", "learner_id": learner_id}
        except Exception as e:
            session.rollback()
            return {"status": "ERROR", "message": str(e)}
        finally:
            session.close()

    def record_resolution(
        self,
        learner_id: str,
        misconception_id: str,
        concept_id: str,
        resolution_status: str,
        mastery_delta: float
    ) -> Dict[str, Any]:
        """Updates persistent state and concept mastery following an unseen reassessment."""
        session: Session = SessionLocal()
        try:
            self.get_or_create_learner(learner_id, session)

            # 1. Update misconception state
            misc_record = session.query(DBLearnerMisconception).filter_by(
                user_id=learner_id, misconception_id=misconception_id
            ).first()

            old_status = "UNKNOWN"
            new_status = resolution_status
            if misc_record:
                old_status = misc_record.status
                if resolution_status in ["RESOLVED", "IMPROVING"]:
                    misc_record.reassessments_passed += 1

                new_status = state_machine.transition_on_reassessment(
                    current_state=misc_record.status,
                    resolution_status=resolution_status,
                    successes_count=misc_record.reassessments_passed
                )
                misc_record.status = new_status

            # 2. Update concept mastery
            concept_record = session.query(DBLearnerConcept).filter_by(
                user_id=learner_id, concept_id=concept_id
            ).first()

            old_mastery = 0.32
            new_mastery = 0.32
            if not concept_record:
                new_mastery = min(1.0, max(0.0, 0.32 + mastery_delta))
                concept_record = DBLearnerConcept(
                    user_id=learner_id,
                    concept_id=concept_id,
                    mastery=new_mastery,
                    status="IMPROVING" if new_mastery < 0.8 else "MASTERED"
                )
                session.add(concept_record)
            else:
                old_mastery = concept_record.mastery
                new_mastery = min(1.0, max(0.0, old_mastery + mastery_delta))
                concept_record.mastery = new_mastery
                concept_record.status = "MASTERED" if new_mastery >= 0.8 else ("IMPROVING" if new_mastery > 0.4 else "LEARNING")
                concept_record.last_updated = datetime.utcnow()

            session.commit()

            return {
                "learner_id": learner_id,
                "misconception_id": misconception_id,
                "old_status": old_status,
                "new_status": new_status,
                "mastery_before": round(old_mastery, 2),
                "mastery_after": round(new_mastery, 2)
            }
        except Exception as e:
            session.rollback()
            return {"status": "ERROR", "message": str(e)}
        finally:
            session.close()

    def get_learner_profile(self, learner_id: str) -> Dict[str, Any]:
        """Compiles full persistent learner dashboard profile."""
        session: Session = SessionLocal()
        try:
            self.get_or_create_learner(learner_id, session)

            concepts = session.query(DBLearnerConcept).filter_by(user_id=learner_id).all()
            concept_list = [
                {
                    "concept_id": c.concept_id,
                    "name": c.concept_id.replace("_", " ").title(),
                    "mastery": round(c.mastery, 2),
                    "status": c.status
                }
                for c in concepts
            ]

            misconceptions = session.query(DBLearnerMisconception).filter_by(user_id=learner_id).all()
            active_list = []
            resolved_list = []
            for m in misconceptions:
                item = {
                    "misconception_id": m.misconception_id,
                    "status": m.status,
                    "occurrences": m.occurrences,
                    "interventions": m.interventions_taken,
                    "reassessments_passed": m.reassessments_passed,
                    "confidence": round(m.confidence, 2),
                    "last_detected": m.last_detected.isoformat() if m.last_detected else None
                }
                if m.status in ["RESOLVED"]:
                    resolved_list.append(item)
                else:
                    active_list.append(item)

            overall_mastery = (
                sum(c.mastery for c in concepts) / len(concepts) if concepts else 0.5
            )

            return {
                "learner_id": learner_id,
                "overall_mastery": round(overall_mastery, 2),
                "concepts": concept_list,
                "active_misconceptions": active_list,
                "resolved_misconceptions": resolved_list,
                "summary": {
                    "total_concepts_tracked": len(concept_list),
                    "active_misconceptions_count": len(active_list),
                    "resolved_misconceptions_count": len(resolved_list)
                }
            }
        finally:
            session.close()

learner_engine = LearnerModelEngine()
