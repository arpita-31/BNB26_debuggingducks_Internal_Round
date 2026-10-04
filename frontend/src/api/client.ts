/**
 * Strongly Typed API Client for ReLearn FastAPI Backend
 */
import {
  SubmissionPayload,
  DiagnosisResponse,
  InterventionResponse,
  ResolutionResponse,
  LearnerProfile
} from '../types';

const API_BASE = '';

export async function diagnoseSubmission(
  domainId: string,
  questionId: string,
  submission: SubmissionPayload,
  learnerId = 'demo_learner'
): Promise<DiagnosisResponse> {
  const res = await fetch(`${API_BASE}/api/diagnose`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      domain_id: domainId,
      question_id: questionId,
      learner_id: learnerId,
      submission
    })
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function fetchIntervention(
  misconceptionId: string,
  confidence = 1.0,
  learnerId = 'demo_learner'
): Promise<InterventionResponse> {
  const res = await fetch(`${API_BASE}/api/intervention`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      misconception_id: misconceptionId,
      confidence,
      learner_id: learnerId
    })
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function verifyResolution(
  reassessmentId: string,
  misconceptionId: string,
  learnerResponse: string,
  conceptId = 'python_range',
  learnerId = 'demo_learner'
): Promise<ResolutionResponse> {
  const res = await fetch(`${API_BASE}/api/resolve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      reassessment_id: reassessmentId,
      misconception_id: misconceptionId,
      concept_id: conceptId,
      learner_response: learnerResponse,
      learner_id: learnerId
    })
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function fetchLearnerProfile(learnerId = 'demo_learner'): Promise<LearnerProfile> {
  const res = await fetch(`${API_BASE}/api/learner/${learnerId}`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function fetchModelMetrics() {
  const res = await fetch(`${API_BASE}/api/model/metrics`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
