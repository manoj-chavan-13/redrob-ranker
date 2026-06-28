"""
Stage 4: Honeypot Detection Engine.
Detects keyword stuffers, impossible candidates, synthetic anomalies, and timeline inconsistencies.
Never recommend likely honeypots.
"""

from typing import Tuple
from app.models import CandidateProfile


class HoneypotDetector:
    """Evaluates candidate profiles for chronological and logical anomalies."""

    @staticmethod
    def evaluate(c: CandidateProfile) -> Tuple[bool, str]:
        exp = c.years_of_experience
        
        # 1. Impossible total experience
        if exp < 0 or exp > 35:
            return True, f"Impossible total experience years: {exp}"
            
        # 2. Skill realism vs duration check
        for s in c.skills:
            prof = s.proficiency.lower()
            dur = s.duration_months
            if prof == "expert" and dur < 6:
                return True, f"Synthetic anomaly: claiming expert proficiency in '{s.name}' with {dur}m duration"
            if dur > 450:
                return True, f"Impossible skill duration ({dur}m) for '{s.name}'"
                
        # 3. Timeline validation (Education vs Experience)
        for edu in c.education:
            sy = edu.start_year
            ey = edu.end_year
            if sy > ey or ey > 2026:
                return True, f"Timeline invalidity: education span {sy}-{ey}"
            if ey >= 2023 and exp > 10:
                return True, f"Impossible timeline: recent graduate ({ey}) claiming {exp}y experience"
            if ey >= 2020 and exp > 16:
                return True, f"Impossible timeline: graduate ({ey}) claiming {exp}y experience"
                
        # 4. Employment consistency check
        total_hist_dur = sum(h.duration_months for h in c.career_history)
        if total_hist_dur > (exp * 12 + 48) and exp > 2:
            return True, f"Employment inconsistency: career duration ({total_hist_dur}m) exceeds total experience ({exp}y)"
            
        return False, ""
