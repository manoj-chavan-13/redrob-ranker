"""
Streaming data ingestion module (Stage 2: Candidate Intelligence Engine).
Optimized for memory efficiency across 100,000 JSONL records.
"""

import json
from pathlib import Path
from typing import Generator
from app.models import CandidateProfile


def stream_candidates(file_path: Path) -> Generator[CandidateProfile, None, None]:
    """Yield strongly typed CandidateProfile objects from JSONL stream."""
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            yield CandidateProfile.from_raw_json(data)
