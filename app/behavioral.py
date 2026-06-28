"""
Stage 3: Behavioral Signal Analyzer.
Redrob signals are modeled as hiring probability modifiers rather than raw features.
Computes Availability, Responsiveness, Trust, and Engagement scores to break ties between behavioral twins.
"""

from datetime import datetime
from typing import Dict
from app.models import CandidateProfile


class BehavioralAnalyzer:
    """Evaluates behavioral signals to compute dynamic hiring probability modifiers."""

    @staticmethod
    def compute_modifier(c: CandidateProfile) -> float:
        sig = c.signals
        
        # 1. Responsiveness Score (0.6 to 1.1)
        resp_rate = sig.recruiter_response_rate
        responsiveness_score = 0.6 + (0.5 * resp_rate)
        
        # 2. Availability & Recency Score
        availability_score = 1.0
        try:
            act_date = datetime.strptime(sig.last_active_date, "%Y-%m-%d")
            ref_date = datetime(2026, 6, 1)
            months_inactive = (ref_date - act_date).days / 30.0
            if months_inactive > 6:
                availability_score *= 0.6
            elif months_inactive > 3:
                availability_score *= 0.85
        except Exception:
            pass
            
        if not sig.open_to_work_flag:
            availability_score *= 0.85
            
        if sig.notice_period_days <= 30:
            availability_score *= 1.05
        elif sig.notice_period_days > 60:
            availability_score *= 0.9
            
        # 3. Trust & Reliability Score
        trust_score = 1.0
        if sig.interview_completion_rate < 0.5:
            trust_score *= 0.85
            
        # 4. Market Demand & Technical Engagement Score
        engagement_score = 1.0
        if sig.github_activity_score > 50:
            engagement_score *= 1.05
        elif sig.github_activity_score == -1 and c.years_of_experience >= 5.0:
            engagement_score *= 0.95
            
        # Composite Hiring Probability Modifier
        hiring_probability = round(
            responsiveness_score * availability_score * trust_score * engagement_score, 4
        )
        return hiring_probability
