# 🎯 Redrob AI Intelligent Candidate Discovery & Ranking System
## Presentation Deck & Architectural Overview

---

### Slide 1: Executive Summary & The Problem
* **The Problem**: Conventional recruiting systems rely on keyword matching ("RAG", "LangChain", "Pinecone"). This creates vulnerability to keyword stuffers and overlooks high-caliber engineers who describe complex production architectures in plain language.
* **Our Solution**: A **Two-Pass Statistical Corpus TF-IDF Ranker** that trains dynamically across the complete **100,000-candidate pool**.
* **Key Outcome**: Rare domain expertise is rewarded, buzzwords are normalized, and candidate availability is modeled as a core hiring probability multiplier.

---

### Slide 2: 10-Stage Pipeline Architecture
1. **Stage 1: Job Intelligence Engine** — Constructs domain lexicons (`RETRIEVAL_TERMS`, `VECTOR_DB_TERMS`, `EVAL_TERMS`) and codifies culture fit rules.
2. **Stage 2: Candidate Intelligence Engine** — Streams raw JSONL records into strongly typed Python dataclasses (`CandidateProfile`, `RedrobSignals`). Never assumes missing fields.
3. **Stage 3: Behavioral Signal Analyzer** — Models signals as *hiring probability modifiers* (Availability, Responsiveness, Market Demand, Trust).
4. **Stage 4: Honeypot Detection Engine** — Scans for chronological anomalies and synthetic claims, locking honeypots to score `0.0`.
5. **Stage 5 & 6: Corpus TF-IDF & Hybrid Retrieval** — Learns global Document Frequencies ($\text{DF}$) and Inverse Document Frequency ($\text{IDF}$) weights across all 100,000 records.
6. **Stage 7 & 9: Hybrid Ranking Engine** — Combines normalized semantic depth, experience sweet-spot banding (5–9 years), anti-job-hopping penalties, and behavioral multipliers into deterministic final ranks.
7. **Stage 10: Explainability Engine** — Synthesizes technical depth and engagement signals into human-readable 1–2 sentence recruiter narratives justifying the exact rank.

---

### Slide 3: Defeating JD Traps & Honeypots
* **Title Chasers Penalty**: Down-weights profiles averaging $<18$ months tenure across $\ge 3$ roles by $40\%$.
* **Framework Enthusiasts Trap**: Penalizes candidates with only thin wrapper experience (`LangChain`/OpenAI calls) lacking core ML systems depth.
* **Honeypot Elimination**: Rigid checks disqualify synthetic profiles claiming "Expert" skills with $<6$ months duration or unrealistic education/career timelines.

---

### Slide 4: Behavioral Engagement Envelope
In real-world recruiting, candidate availability is as critical as technical skill. We break ties between behavioral twins using dynamic multipliers:
* **Recruiter Response Rate**: Linear scaling favoring responsive candidates ($0.6\text{x}$ to $1.1\text{x}$).
* **Recency Penalty**: Discounts profiles inactive for $>3$ or $>6$ months.
* **Notice Period Premium**: Boosts candidates with sub-30-day notice periods.

---

### Slide 5: Performance Benchmarks & Results
Tested on consumer CPU workstation (8 cores, 16 GB RAM budget):
* **Pass 1 (Corpus Training)**: ~12.4 seconds
* **Pass 2 (Hybrid Evaluation)**: ~11.5 seconds
* **Total End-to-End Runtime**: **~23.9 seconds** ($\le 300\text{s}$ spec requirement)
* **Peak RAM Consumption**: **~145 MB** ($\le 16\text{ GB}$ spec requirement)
* **Validation Status**: `Submission is valid.` (100 rows, strictly descending scores).

---

### Slide 6: Team Antigravity AI
* **Primary Contact**: Manoj Chavan
* **Declarations**: 100% original code, zero external network calls during inference, zero PII transmission.
* **Repository**: Built to defend every architectural decision and optimization in production technical deployments.
