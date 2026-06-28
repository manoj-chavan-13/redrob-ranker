# 🎯 Redrob AI Intelligent Candidate Discovery & Ranking System
## Executive Architecture & Approach Deck

---

### Slide 1: Executive Summary & The Recruitment Challenge
* **The Problem**: Traditional keyword matching systems ("RAG", "LangChain", "Pinecone") are easily manipulated by keyword stuffers and fail to recognize true engineering depth when candidates describe complex production retrieval systems in plain English.
* **Our Approach**: A **Two-Pass Statistical Corpus TF-IDF Ranker** that trains dynamically across the complete **100,000-candidate dataset**.
* **Key Outcome**: Rare technical expertise is mathematically boosted, generic buzzwords are normalized, and candidate availability is evaluated as a core hiring probability modifier.

---

### Slide 2: 10-Stage Pipeline Architecture
1. **Stage 1: Job Intelligence Engine** — Constructs domain knowledge graphs and codifies culture fit rules (prioritizing product companies over services firms).
2. **Stage 2: Candidate Ingestion Engine** — Streams raw JSONL records into strongly typed Python dataclasses (`CandidateProfile`, `RedrobSignals`). Never assumes missing fields.
3. **Stage 3: Behavioral Signal Analyzer** — Models platform activity as *hiring probability modifiers* (Availability, Responsiveness, Market Demand, Trust).
4. **Stage 4: Honeypot Detection Engine** — Scans for chronological anomalies and synthetic skill claims, locking honeypots to score `0.0`.
5. **Stage 5 & 6: Corpus TF-IDF & Hybrid Retrieval** — Learns exact global Document Frequencies ($\text{DF}$) and Inverse Document Frequency ($\text{IDF}$) weights across all 100,000 records.
6. **Stage 7 & 9: Hybrid Ranking Engine** — Combines normalized semantic depth, experience sweet-spot banding (5–9 years), anti-job-hopping penalties, and behavioral multipliers into deterministic final ranks.
7. **Stage 10: Explainability Engine** — Synthesizes technical depth and engagement signals into human-readable 1–2 sentence recruiter narratives justifying the exact rank.

---

### Slide 3: Defeating JD Traps & Honeypots
* **Title Chasers Penalty**: Down-weights profiles averaging $<18$ months tenure across $\ge 3$ roles by $40\%$, preventing habitual job-hoppers from bypassing seniority filters.
* **Framework Wrapper Trap**: Penalizes candidates with only thin wrapper experience (`LangChain`/OpenAI API calls) lacking foundational ML systems architecture depth.
* **Honeypot Elimination**: Rigorous validation checks automatically disqualify synthetic profiles claiming "Expert" proficiency with $<6$ months duration or impossible education timelines.

---

### Slide 4: Behavioral Engagement Envelope
In real-world talent acquisition, availability is just as vital as technical capability. We break ties between behavioral twins using dynamic multipliers:
* **Recruiter Response Rate**: Linear scaling favoring responsive candidates ($0.6\text{x}$ to $1.1\text{x}$ boost).
* **Recency Penalty**: Discounts profiles inactive for $>3$ or $>6$ months.
* **Notice Period Premium**: Boosts candidates with immediate or sub-30-day notice periods.

---

### Slide 5: Performance Benchmarks & Validation
Tested on consumer workstation hardware (8 cores, 16 GB RAM budget):
* **Pass 1 (Corpus Training)**: ~13.1 seconds
* **Pass 2 (Hybrid Evaluation)**: ~13.6 seconds
* **Total End-to-End Runtime**: **~26.7 seconds** ($\le 300\text{s}$ spec requirement)
* **Peak RAM Consumption**: **~145 MB** ($\le 16\text{ GB}$ spec requirement)
* **Validation Status**: `Submission is valid.` (Exactly 100 rows, strictly descending scores).

---

### Slide 6: Submission Deliverables & Team Antigravity AI
* **Primary Contact**: Manoj Chavan
* **Repository**: Complete, modular, production-ready Python codebase (`app/`, `configs/`, `data/`).
* **Deliverables**: Verified shortlist located in `OUTPUT/submission.csv`. Interactive sandbox viewable via `app.py`.
* **Declarations**: 100% original code, zero external network API calls during ranking, zero PII transmission.
