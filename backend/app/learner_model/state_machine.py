"""
Cognitive State Machine for ReLearn Misconceptions
Defines valid state transitions based on empirical diagnostic and reassessment evidence.
"""
from typing import Dict, Any

class MisconceptionStateMachine:
    VALID_STATES = [
        "UNKNOWN",
        "SUSPECTED",
        "ACTIVE",
        "IMPROVING",
        "PARTIALLY_RESOLVED",
        "RESOLVED",
        "RECURRING"
    ]

    def transition_on_diagnosis(
        self,
        current_state: str,
        confidence: float,
        occurrences: int
    ) -> str:
        """Determines state transition when a misconception is diagnosed in a submission."""
        if current_state == "RESOLVED":
            # If a previously resolved misconception resurfaces, it becomes RECURRING
            return "RECURRING"
        
        if confidence >= 0.75 or occurrences >= 2:
            return "ACTIVE"
        elif confidence >= 0.50:
            return "SUSPECTED"
        
        return current_state or "SUSPECTED"

    def transition_on_reassessment(
        self,
        current_state: str,
        resolution_status: str,
        successes_count: int
    ) -> str:
        """Determines state transition following an unseen reassessment check."""
        if resolution_status == "RESOLVED":
            return "RESOLVED"
        elif resolution_status == "IMPROVING":
            return "IMPROVING" if successes_count < 2 else "RESOLVED"
        elif resolution_status == "PARTIALLY_RESOLVED":
            return "PARTIALLY_RESOLVED"
        elif resolution_status == "PERSISTENT":
            return "ACTIVE"
        
        return current_state

state_machine = MisconceptionStateMachine()
