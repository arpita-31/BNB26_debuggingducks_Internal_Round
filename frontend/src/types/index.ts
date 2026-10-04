/**
 * TypeScript Type Definitions for ReLearn
 * Matches FastAPI backend Pydantic schemas.
 */

export type Modality = 'text' | 'code' | 'image' | 'audio';

export interface SubmissionPayload {
  modality: Modality;
  text: string;
  code?: string;
  metadata?: Record<string, any>;
}

export interface CandidateProbability {
  id: string;
  name: string;
  probability: number;
}

export interface AlternativeHypothesis {
  misconception_id: string;
  name: string;
  concept: string;
  confidence: number;
}

export interface PipelineStage {
  stage: number;
  name: string;
  status: 'COMPLETED' | 'AMBIGUOUS' | 'CONFIDENT';
  detail: string;
}

export interface DiagnosisResponse {
  learner_id: string;
  question_id: string;
  domain_id: string;
  modality: string;
  syntax_valid: boolean;
  syntax_error?: string;
  prediction: {
    misconception_id: string;
    name: string;
    concept: string;
    confidence: number;
    is_correct: boolean;
  };
  differentiation: {
    margin: number;
    secondary_id?: string;
    is_ambiguous: boolean;
    rationale: string;
  };
  ranked_candidates: CandidateProbability[];
  alternatives: AlternativeHypothesis[];
  evidence: string[];
  diagnostic_probe?: DiagnosticProbe | null;
  pipeline_stages: PipelineStage[];
}

export interface DiagnosticProbeOption {
  text: string;
  indicates: string;
  explanation: string;
}

export interface DiagnosticProbe {
  id: string;
  pair: string[];
  title: string;
  prompt: string;
  options: DiagnosticProbeOption[];
}

export interface InterventionStage {
  type: string;
  title: string;
  content?: string;
  visual_type?: string;
  data?: any;
  code?: string;
  explanation?: string;
  question?: string;
  options?: string[];
  correct_index?: number;
}

export interface InterventionResponse {
  learner_id: string;
  misconception_id: string;
  name: string;
  concept: string;
  confidence_detected: number;
  pedagogical_goal: string;
  stages: InterventionStage[];
  total_stages: number;
}

export interface ReassessmentQuestion {
  id: string;
  concept: string;
  difficulty: string;
  title: string;
  prompt: string;
  code?: string;
  expected_output?: string;
}

export interface ResolutionResponse {
  reassessment_id: string;
  misconception_id: string;
  resolution_status: 'RESOLVED' | 'IMPROVING' | 'PARTIALLY_RESOLVED' | 'PERSISTENT';
  is_resolved: boolean;
  evidence: string;
  mastery_before: number;
  mastery_after: number;
  new_state: string;
}

export interface LearnerProfile {
  learner_id: string;
  overall_mastery: number;
  concepts: Array<{
    concept_id: string;
    name: string;
    mastery: number;
    status: string;
  }>;
  active_misconceptions: Array<{
    misconception_id: string;
    status: string;
    occurrences: number;
    confidence: number;
  }>;
  resolved_misconceptions: Array<{
    misconception_id: string;
    status: string;
  }>;
  summary: {
    total_concepts_tracked: number;
    active_misconceptions_count: number;
    resolved_misconceptions_count: number;
  };
}
