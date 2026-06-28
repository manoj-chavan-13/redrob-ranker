"""
Strongly typed candidate models (Stage 2: Candidate Intelligence Engine).
Never assume missing fields; use safe fallbacks and explicit data structures.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class CareerItem:
    company: str = ""
    title: str = ""
    start_date: str = ""
    end_date: Optional[str] = None
    duration_months: int = 0
    is_current: bool = False
    industry: str = ""
    company_size: str = ""
    description: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CareerItem":
        return cls(
            company=data.get("company", ""),
            title=data.get("title", ""),
            start_date=data.get("start_date", ""),
            end_date=data.get("end_date"),
            duration_months=data.get("duration_months", 0),
            is_current=data.get("is_current", False),
            industry=data.get("industry", ""),
            company_size=data.get("company_size", ""),
            description=data.get("description", "")
        )


@dataclass
class SkillItem:
    name: str = ""
    category: str = ""
    duration_months: int = 0
    proficiency: str = ""
    last_used_year: int = 2025
    endorsements: int = 0

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SkillItem":
        return cls(
            name=data.get("name", ""),
            category=data.get("category", ""),
            duration_months=data.get("duration_months", 0),
            proficiency=data.get("proficiency", ""),
            last_used_year=data.get("last_used_year", 2025),
            endorsements=data.get("endorsements", 0)
        )


@dataclass
class EducationItem:
    institution: str = ""
    degree: str = ""
    field_of_study: str = ""
    start_year: int = 0
    end_year: int = 0
    grade: str = ""
    tier: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EducationItem":
        return cls(
            institution=data.get("institution", ""),
            degree=data.get("degree", ""),
            field_of_study=data.get("field_of_study", ""),
            start_year=data.get("start_year", 0),
            end_year=data.get("end_year", 0),
            grade=data.get("grade", ""),
            tier=data.get("tier", "")
        )


@dataclass
class RedrobSignals:
    recruiter_response_rate: float = 0.5
    last_active_date: str = "2025-01-01"
    open_to_work_flag: bool = True
    notice_period_days: int = 60
    github_activity_score: int = -1
    interview_completion_rate: float = 1.0
    profile_completeness_score: float = 80.0
    saved_by_recruiters_30d: int = 0

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RedrobSignals":
        return cls(
            recruiter_response_rate=data.get("recruiter_response_rate", 0.5),
            last_active_date=data.get("last_active_date", "2025-01-01"),
            open_to_work_flag=data.get("open_to_work_flag", True),
            notice_period_days=data.get("notice_period_days", 60),
            github_activity_score=data.get("github_activity_score", -1),
            interview_completion_rate=data.get("interview_completion_rate", 1.0),
            profile_completeness_score=data.get("profile_completeness_score", 80.0),
            saved_by_recruiters_30d=data.get("saved_by_recruiters_30d", 0)
        )


@dataclass
class CandidateProfile:
    candidate_id: str
    summary: str = ""
    years_of_experience: float = 0.0
    current_title: str = ""
    current_company: str = ""
    current_industry: str = ""
    career_history: List[CareerItem] = field(default_factory=list)
    skills: List[SkillItem] = field(default_factory=list)
    education: List[EducationItem] = field(default_factory=list)
    signals: RedrobSignals = field(default_factory=RedrobSignals)

    @classmethod
    def from_raw_json(cls, data: Dict[str, Any]) -> "CandidateProfile":
        prof = data.get("profile", {})
        return cls(
            candidate_id=data.get("candidate_id", ""),
            summary=prof.get("summary", ""),
            years_of_experience=prof.get("years_of_experience", 0.0),
            current_title=prof.get("current_title", ""),
            current_company=prof.get("current_company", ""),
            current_industry=prof.get("current_industry", ""),
            career_history=[CareerItem.from_dict(h) for h in data.get("career_history", [])],
            skills=[SkillItem.from_dict(s) for s in data.get("skills", [])],
            education=[EducationItem.from_dict(e) for e in data.get("education", [])],
            signals=RedrobSignals.from_dict(data.get("redrob_signals", {}))
        )
