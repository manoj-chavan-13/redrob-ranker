# Redrob AI Intelligent Candidate Ranking System
## Executive Solution Slide Deck — Team Antigravity AI

---

### Slide 1: Executive Summary & Mandate
* **Target Role**: Founding Team Senior AI Engineer (Focus on scalable vector retrieval infrastructure and production LLM evaluation).
* **The Problem**: Conventional vector retrieval filters ("RAG", "LangChain", "Pinecone") are easily manipulated by keyword stuffers while rejecting senior architects who describe custom retrieval systems in plain engineering terms.
* **Our Solution**: Engineered a **Two-Pass Statistical Corpus TF-IDF Ranker** trained across the entire 100,000-candidate pool. Rare terms (`qlora`, `weaviate`, `ndcg`) receive boosted semantic weights while generic buzzwords are mathematically normalized.
* **Core Deliverable**: A high-precision shortlist of 100 verified candidates backed by 1–2 sentence human-readable recruiter narratives justifying exact placements.

---

### Slide 2: 10-Stage Pipeline Architecture Breakdown
1. **Stage 1: Job Intelligence Engine** — Constructs specialized domain lexicons (`RETRIEVAL_TERMS`, `VECTOR_DB_TERMS`, `EVAL_TERMS`) and establishes culture fit weighting (prioritizing product companies over IT services firms).
2. **Stage 2: Ingestion Engine** — High-speed JSONL streaming parser mapping raw records into strongly typed Python dataclasses (`CandidateProfile`) with zero memory bloat (<150 MB RAM).
3. **Stage 3: Behavioral Signal Analyzer** — Evaluates 23 platform signals as a hiring probability modifier ($0.6\text{x}$ to $1.1\text{x}$ envelope), boosting responsive candidates with immediate notice periods.
4. **Stage 4: Honeypot Detection Engine** — Rigorously screens chronological conflicts and synthetic skill claims (e.g., claiming expert skill with <6m tenure), assigning traps a hard score of `0.0`.
5. **Stage 5–8: Hybrid Scoring Engine** — Combines statistical TF-IDF domain scores with experience sweet-spot banding (5–9 years target band) and anti-job-hopping penalties.
6. **Stage 9–10: Explainability Engine** — Synthesizes multi-dimensional scoring into human-readable 1–2 sentence recruiter narratives justifying candidate rank and confidence level.

---

### Slide 3: Mathematical Defensibility & Technical Taxonomies
To quantify engineering seniority, our engine evaluates candidate profiles against three curated domain graphs:
* **Vector Retrieval Infrastructure**: Hands-on experience building custom indexing pipelines using `FAISS`, `Milvus`, `Weaviate`, `Qdrant`, and custom HNSW graphs.
* **Evaluation & Quant Metrics**: Rigorous validation methodologies demonstrated by `NDCG`, `MRR`, `Recall@K`, `Precision@K`, and automated LLM-as-a-judge frameworks.
* **Foundational ML Systems**: Differentiating true practitioners from API wrappers by tracking deep training terms: `QLoRA`, `FlashAttention`, `vLLM`, `DeepSpeed`, and distributed pruning.

---

### Slide 4: Defeating JD Traps & Synthetic Honeypots
* **Title Chasers Penalty (-40% Score Multiplier)**: Habitual job-hoppers inflate titles without building engineering depth. If a candidate averages <18 months tenure across $\ge 3$ roles, our engine applies a sharp 0.60x penalty.
* **Framework Wrapper Filter**: Profiles listing superficial wrapper libraries (`LangChain`, basic OpenAI prompts) without foundational systems keywords receive downgraded semantic multipliers.
* **Product vs. Services Alignment**: For a Founding Team role, product ownership is critical. Candidates from pure product builders receive positive affinity weighting over outsourced IT services firms.
* **Honeypot Disqualification**: Synthetic trap candidates injected into the dataset (e.g., claiming 10+ years of PyTorch experience when graduated 2 years ago) are locked to `0.0000`.

---

### Slide 5: The Behavioral Engagement Envelope
In talent acquisition, technical excellence is meaningless if the candidate is unreachable. We compute a compound behavioral modifier:
* **Recruiter Response Rate**: Linear scaling from `0.60x` (unresponsive) up to `1.10x` boost over 90 days.
* **Platform Activity Recency**: Penalizes profiles dormant for >90 days (`0.85x`) or >180 days (`0.70x`).
* **Notice Period & Availability**: Boosts immediate availability / sub-30 days by `1.05x`; penalties for 90+ days.
* **Assessment Verification**: Adds up to `+0.050` absolute confidence bonus for verified coding badges.

---

### Slide 6: Performance Benchmarks & Compliance Table
Executed offline across 100,000 candidate records on a local workstation (8 CPU Cores, Windows 11):

| Performance Dimension | Measured Benchmark | Hackathon Specification Budget | Validation Status |
| :--- | :--- | :--- | :--- |
| **Pass 1: Corpus TF-IDF Training** | 13.12 seconds | Offline Streaming Processing | ✅ **PASSED** |
| **Pass 2: Hybrid Evaluation** | 13.66 seconds | Offline Streaming Processing | ✅ **PASSED** |
| **Total End-to-End Runtime** | **26.78 seconds** | $\le 300.00$ seconds (5 Minutes) | ✅ **11.2x Faster** |
| **Peak RAM Consumption** | **~145.4 MB** | $\le 16,000.0$ MB (16 GB Limit) | ✅ **99% Margin** |
| **Output Validation Check** | 100 Rows, Monotonic Scores | Exactly 100 Rows, CSV Validated | ✅ **100% Valid** |
