"""
Stage 1, 5, 6, 7, 9: Job Intelligence & Hybrid Ranking Engine.
Computes corpus TF-IDF weights across the dataset and combines them into the multi-factor Hybrid Ranking formula.
"""

import collections
import math
from pathlib import Path
from typing import Dict, List, Tuple
from app.behavioral import BehavioralAnalyzer
from app.honeypot import HoneypotDetector
from app.ingestion import stream_candidates
from app.models import CandidateProfile

# Lexicons derived from Job Knowledge Graph (Stage 1)
SERVICES_COMPANIES = {
    "tcs", "tata consultancy services", "infosys", "wipro", "accenture", 
    "cognizant", "capgemini", "mindtree", "hcl", "hcl technologies", 
    "tech mahindra", "genpact", "ltimindtree", "mphasis", "deloitte", 
    "kpmg", "pwc", "ey", "ernst & young", "booz allen", "tech-mahindra"
}

IRRELEVANT_TITLES = {
    "marketing", "operations", "accountant", "hr ", "human resources", 
    "customer support", "business analyst", "mechanical", "chemical", 
    "sales", "recruiter", "graphic", "qa ", "quality assurance", 
    "project manager", "product manager", "content writer", "financial"
}

RELEVANT_AI_TITLES = [
    "senior ai engineer", "ai engineer", "lead ai engineer", "staff ai engineer",
    "machine learning engineer", "ml engineer", "senior machine learning engineer",
    "staff machine learning engineer", "search engineer", "recommendation",
    "retrieval engineer", "nlp engineer", "senior nlp engineer", "applied scientist",
    "applied ml engineer", "research engineer", "data scientist", "senior data scientist"
]

RETRIEVAL_TERMS = [
    "sentence transformers", "faiss", "opensearch", "weaviate", "pinecone", 
    "qdrant", "milvus", "elasticsearch", "bm25", "hybrid search", "hybrid retrieval",
    "retrieval", "ranking", "recommendation system", "recommender", "dense retrieval",
    "semantic search", "bge", "e5", "vector search", "matching system", 
    "search pipeline", "search engine", "candidate recommendation", "collaborative filtering",
    "content-based", "re-ranking", "reranking", "personalized search"
]

VECTOR_DB_TERMS = [
    "faiss", "opensearch", "weaviate", "pinecone", "qdrant", "milvus", 
    "elasticsearch", "vector database", "vector db", "pgvector"
]

EVAL_TERMS = [
    "ndcg", "mrr", "map", "a/b test", "online evaluation", "offline benchmark",
    "latency", "p95", "throughput", "scale", "evaluation framework"
]

CORE_ML_TERMS = [
    "python", "pytorch", "tensorflow", "scikit-learn", "fine-tuning", 
    "qlora", "lora", "peft", "llm", "deep learning", "nlp", "distributed systems"
]

CV_SPEECH_TERMS = [
    "opencv", "yolo", "image classification", "speech recognition", "tts", "object detection"
]


class HybridScoringEngine:
    """Manages Corpus TF-IDF training and executes Stage 9 Hybrid Ranking."""

    def __init__(self) -> None:
        self.idf_weights: Dict[str, float] = {}
        self.total_candidates: int = 0
        self.all_domain_terms = set(
            RETRIEVAL_TERMS + VECTOR_DB_TERMS + EVAL_TERMS + CORE_ML_TERMS
        )

    def fit_corpus(self, candidates_path: Path) -> None:
        """Pass 1: Stream dataset to compute vocabulary Document Frequencies and IDF weights."""
        df_counts: Dict[str, int] = collections.defaultdict(int)
        count = 0
        for c in stream_candidates(candidates_path):
            count += 1
            history_text = " ".join(h.description for h in c.career_history).lower()
            skills_text = " ".join(s.name for s in c.skills).lower()
            full_text = f"{c.summary.lower()} {history_text} {skills_text}"
            for term in self.all_domain_terms:
                if term in full_text:
                    df_counts[term] += 1
                    
        self.total_candidates = count
        for term in self.all_domain_terms:
            df = df_counts[term]
            self.idf_weights[term] = 1.0 + math.log(max(1, count) / (1.0 + df))

    def evaluate(self, c: CandidateProfile) -> Tuple[float, List[str]]:
        """Pass 2: Score candidate across semantic, career, and behavioral dimensions."""
        is_hp, hp_reason = HoneypotDetector.evaluate(c)
        if is_hp:
            return 0.0, []
            
        title = c.current_title.lower()
        exp = c.years_of_experience
        history = c.career_history
        skills = c.skills
        skills_map = {s.name.lower(): s for s in skills}
        
        # Role Relevance & Title Fit
        if any(it in title for it in IRRELEVANT_TITLES):
            return 0.5, []
            
        title_score = 5.0
        for rt in RELEVANT_AI_TITLES:
            if rt in title:
                title_score = 30.0
                break
        if title_score == 5.0 and any(t in title for t in ["software engineer", "backend", "data engineer"]):
            title_score = 15.0
            
        # Career Progression & Experience Banding (Target 5-9 years)
        if 4.5 <= exp <= 9.5:
            exp_score = 20.0
        elif 3.5 <= exp < 4.5 or 9.5 < exp <= 12.0:
            exp_score = 16.0
        elif 2.5 <= exp < 3.5 or 12.0 < exp <= 14.0:
            exp_score = 10.0
        else:
            exp_score = 4.0
            
        # Disqualifiers & Traps
        if history:
            all_services = all(h.company.lower().strip() in SERVICES_COMPANIES for h in history)
            if all_services:
                title_score *= 0.25
                exp_score *= 0.25
                
        if len(history) >= 3 and exp >= 4.0:
            avg_tenure = sum(h.duration_months for h in history) / len(history)
            if avg_tenure < 18:
                title_score *= 0.6
                
        if history and history[0].is_current:
            curr_desc = history[0].description.lower()
            if any(t in title for t in ["architect", "manager", "director"]):
                if not any(code in curr_desc for code in ["python", "code", "shipped", "built", "model", "pipeline", "implemented"]):
                    title_score *= 0.5
                    
        # Semantic Similarity & Technical Depth weighted by learned IDF
        full_text = (c.summary + " " + " ".join(h.description for h in history)).lower()
        retrieval_hits = [t for t in RETRIEVAL_TERMS if t in full_text or t in skills_map]
        vdb_hits = [t for t in VECTOR_DB_TERMS if t in full_text or t in skills_map]
        eval_hits = [t for t in EVAL_TERMS if t in full_text or t in skills_map]
        ml_hits = [t for t in CORE_ML_TERMS if t in full_text or t in skills_map]
        
        retrieval_score = sum(5.0 * (self.idf_weights.get(t, 3.0) / 3.0) for t in retrieval_hits[:5])
        vdb_score = sum(4.0 * (self.idf_weights.get(t, 3.0) / 3.0) for t in vdb_hits[:4])
        eval_score = sum(3.0 * (self.idf_weights.get(t, 3.0) / 3.0) for t in eval_hits[:4])
        ml_score = sum(2.0 * (self.idf_weights.get(t, 3.0) / 3.0) for t in ml_hits[:5])
        
        tech_score = retrieval_score + vdb_score + eval_score + ml_score
        
        cv_hits = sum(1 for t in CV_SPEECH_TERMS if t in skills_map)
        if cv_hits >= 3 and len(retrieval_hits) == 0 and "nlp" not in skills_map:
            tech_score *= 0.25
            
        if ("langchain" in skills_map or "prompt engineering" in skills_map) and len(retrieval_hits) <= 1 and len(ml_hits) <= 2:
            tech_score *= 0.4
            
        tech_score = min(50.0, tech_score)
        raw_score = title_score + exp_score + tech_score
        
        # Apply Stage 3 Behavioral Modifier
        behavioral_multiplier = BehavioralAnalyzer.compute_modifier(c)
        final_score = round(raw_score * behavioral_multiplier, 4)
        
        return final_score, retrieval_hits
