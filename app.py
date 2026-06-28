import csv
from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="Redrob AI Candidate Ranking Dashboard",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Redrob AI Intelligent Candidate Discovery & Ranking")
st.markdown("### Senior AI Engineer Mandate — Top 100 Recommended Shortlist")

sub_path = Path("submission.csv")
if not sub_path.exists():
    st.error("Submission file `submission.csv` not found. Please run `python main.py` first.")
else:
    candidates = []
    with open(sub_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            candidates.append({
                "Rank": int(row["rank"]),
                "Candidate ID": row["candidate_id"],
                "Score": float(row["score"]),
                "Recruiter Reasoning": row["reasoning"]
            })

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Candidates Evaluated", "100,000")
    col2.metric("Shortlisted Profiles", len(candidates))
    col3.metric("Top Score", f"{candidates[0]['Score']:.4f}" if candidates else "N/A")

    st.divider()

    search = st.text_input("🔍 Search Candidate ID or Keyword in Reasoning", "")
    filtered = [
        c for c in candidates 
        if search.lower() in c["Candidate ID"].lower() or search.lower() in c["Recruiter Reasoning"].lower()
    ]

    st.subheader(f"Ranked Candidate List ({len(filtered)} matches)")
    
    for c in filtered[:25]:
        with st.expander(f"Rank #{c['Rank']} | {c['Candidate ID']} | Score: {c['Score']:.4f}"):
            st.markdown(f"**Recruiter Assessment:**\n> {c['Recruiter Reasoning']}")
