"""
Diagnostic Question Engine for ReLearn
Serves targeted probe questions when the model diagnosis is ambiguous or when
different misconceptions yield overlapping surface answers.
"""
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

class DiagnosticQuestionEngine:
    def __init__(self):
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        self.probes_file = base_dir / "data" / "diagnostic_probes.json"
        self._probes: List[Dict[str, Any]] = []
        self._load_probes()

    def _load_probes(self):
        if self.probes_file.exists():
            with open(self.probes_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._probes = data.get("probes", [])

    def find_disambiguation_probe(self, class_a: str, class_b: str) -> Optional[Dict[str, Any]]:
        """Finds a tailored diagnostic probe to distinguish between two candidate misconceptions."""
        target_set = {class_a, class_b}
        for probe in self._probes:
            pair_set = set(probe.get("pair", []))
            if target_set == pair_set:
                return probe

        # Fallback probe if no specific pair probe is defined
        for probe in self._probes:
            if class_a in probe.get("pair", []) or class_b in probe.get("pair", []):
                return probe

        return None

    def evaluate_probe_response(self, probe_id: str, selected_option_index: int) -> Dict[str, Any]:
        """Evaluates learner's response to the diagnostic probe to finalize the diagnosis."""
        probe = next((p for p in self._probes if p["id"] == probe_id), None)
        if not probe:
            return {"error": "Probe not found"}

        options = probe.get("options", [])
        if selected_option_index < 0 or selected_option_index >= len(options):
            return {"error": "Invalid option index"}

        chosen = options[selected_option_index]
        return {
            "probe_id": probe_id,
            "selected_option": chosen["text"],
            "disambiguated_misconception_id": chosen["indicates"],
            "explanation": chosen["explanation"],
            "status": "DISAMBIGUATED"
        }

diagnostic_engine = DiagnosticQuestionEngine()
