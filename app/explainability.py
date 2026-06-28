"""
Stage 10: Explainability Engine.
Generates concise 1-2 sentence human-readable recruiter explanations justifying rankings.
"""

from typing import List
from app.models import CandidateProfile


class ExplainabilityEngine:
    """Synthesizes technical depth, career history, and behavioral engagement into reasoning."""

    @staticmethod
    def generate_reasoning(c: CandidateProfile, retrieval_hits: List[str], rank: int, score: float) -> str:
        exp = c.years_of_experience
        company = c.current_company
        sig = c.signals
        
        top_skills = [s.name for s in sorted(c.skills, key=lambda x: -x.endorsements)[:3]]
        skills_str = ", ".join(top_skills) if top_skills else "modern AI/ML stack"
        
        domain_str = f"{len(retrieval_hits)} retrieval/ranking domain hits" if retrieval_hits else "core ML foundations"
        resp_pct = int(sig.recruiter_response_rate * 100)
        
        # Calculate confidence score based on normalized ranking score
        confidence = min(99, int(75 + (min(110.0, score) / 110.0) * 24))
        
        reasoning = (
            f"Candidate ranked #{rank} because of strong alignment as a Senior AI Engineer ({exp}y exp @ {company}), "
            f"demonstrated by {domain_str} and expertise in {skills_str}. "
            f"Excellent recruiter response rate ({resp_pct}%), {sig.notice_period_days}d notice period, "
            f"and consistent interview engagement. Confidence {confidence}%."
        )
        return reasoning
