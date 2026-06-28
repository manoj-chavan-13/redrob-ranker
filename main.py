#!/usr/bin/env python3
"""
Redrob AI Candidate Ranking System — Main Pipeline Entrypoint
=============================================================
Orchestrates the 10-Stage Candidate Discovery & Ranking architecture:
  - Stage 1: Job Intelligence & Lexicon Setup
  - Stage 2: Candidate Ingestion & Profile Modeling
  - Stage 3: Behavioral Signal Analyzer
  - Stage 4: Honeypot Detection Engine
  - Stage 5 & 6: Corpus TF-IDF Semantic Weights & Hybrid Retrieval
  - Stage 9: Hybrid Ranking Formula
  - Stage 10: Explainability Engine
"""

import argparse
import csv
import logging
import sys
import time
from pathlib import Path
from typing import Any, List, Tuple

from app.explainability import ExplainabilityEngine
from app.ingestion import stream_candidates
from app.scoring import HybridScoringEngine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("RedrobMasterPipeline")


def run_pipeline(candidates_path: Path, output_path: Path, top_k: int = 100) -> None:
    """Execute end-to-end 10-stage ranking pipeline."""
    t0 = time.time()
    
    logger.info("===================================================================")
    logger.info("Initializing Redrob AI Intelligent Candidate Ranking Pipeline")
    logger.info("===================================================================")
    
    scoring_engine = HybridScoringEngine()
    
    # Pass 1: Corpus Training & Statistical Weights
    logger.info(f"[Stage 5/6] Pass 1: Training Corpus TF-IDF model on {candidates_path.name}...")
    scoring_engine.fit_corpus(candidates_path)
    logger.info(
        f"-> Vocabulary frequencies learned across {scoring_engine.total_candidates:,} candidates. "
        f"Rare domain terms assigned dynamic IDF semantic boost."
    )
    
    # Pass 2: Hybrid Evaluation & Scoring
    logger.info(f"[Stage 2/3/4/9] Pass 2: Evaluating candidates across hybrid dimensions...")
    scored_results: List[Tuple[float, str, List[str], Any]] = []
    
    for candidate in stream_candidates(candidates_path):
        score, hits = scoring_engine.evaluate(candidate)
        scored_results.append((score, candidate.candidate_id, hits, candidate))
        
    # Sort strictly descending by score, ascending by candidate_id for deterministic tie-break
    scored_results.sort(key=lambda x: (-x[0], x[1]))
    top_candidates = scored_results[:top_k]
    
    # Stage 10: Generate Recruiter Explanations & Export CSV
    logger.info(f"[Stage 10] Generating recruiter explainability narratives and writing top {top_k}...")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["candidate_id", "rank", "score", "reasoning"])
        for idx, (score, cid, hits, cand_obj) in enumerate(top_candidates, start=1):
            reasoning = ExplainabilityEngine.generate_reasoning(cand_obj, hits, idx, score)
            writer.writerow([cid, idx, f"{score:.4f}", reasoning])
            
    elapsed = time.time() - t0
    logger.info("===================================================================")
    logger.info(f"Pipeline Execution Complete! Processed {scoring_engine.total_candidates:,} candidates in {elapsed:.2f}s.")
    logger.info(f"Submission file generated at: {output_path.resolve()}")
    logger.info("===================================================================")


def main():
    parser = argparse.ArgumentParser(description="Redrob Master Candidate Ranking Pipeline")
    parser.add_argument("--candidates", default="./candidates.jsonl", help="Path to input candidates.jsonl")
    parser.add_argument("--out", default="./submission.csv", help="Path to output submission CSV")
    args = parser.parse_args()
    
    candidates_file = Path(args.candidates)
    if not candidates_file.exists():
        fallback = Path("./data/candidates.jsonl")
        if fallback.exists():
            candidates_file = fallback
        else:
            logger.error(f"Input file '{candidates_file}' not found.")
            sys.exit(1)
            
    run_pipeline(candidates_file, Path(args.out))


if __name__ == "__main__":
    main()
