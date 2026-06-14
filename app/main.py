"""Streamlit entry point for the Resume Screener app."""

from __future__ import annotations

from html import escape

import pandas as pd
import streamlit as st

try:
    from app import matcher, parser, ranker
except ImportError:
    import matcher
    import parser
    import ranker


st.set_page_config(page_title="Resume Screener", page_icon="🧠", layout="wide")

st.markdown(
    """
    <style>
        .main .block-container {
            padding-top: 2rem;
            max-width: 1180px;
        }
        .result-card {
            background: #ffffff;
            border: 1px solid #e6e8ef;
            border-radius: 8px;
            padding: 1rem 1.15rem;
            margin: 0.75rem 0;
            box-shadow: 0 8px 24px rgba(22, 31, 49, 0.06);
        }
        .result-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 0.65rem;
        }
        .candidate-name {
            font-size: 1.05rem;
            font-weight: 700;
            color: #172033;
        }
        .rank-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 3.2rem;
            height: 2rem;
            border-radius: 999px;
            color: #182033;
            font-weight: 800;
            font-size: 0.9rem;
        }
        .rank-gold { background: #ffe08a; }
        .rank-silver { background: #dbe2ea; }
        .rank-bronze { background: #e8b37a; }
        .rank-default { background: #e9f2ff; color: #0f4d7a; }
        .score-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 0.25rem;
            color: #4c586b;
            font-size: 0.92rem;
        }
        .skill-chip {
            display: inline-block;
            margin: 0.2rem 0.25rem 0.2rem 0;
            padding: 0.24rem 0.58rem;
            border-radius: 999px;
            background: #eef6f3;
            color: #16624f;
            border: 1px solid #cfe8df;
            font-size: 0.85rem;
            font-weight: 600;
        }
        div[data-testid="stProgress"] > div > div > div > div {
            background: linear-gradient(90deg, #1f9d78, #2f80ed);
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def _rank_badge(rank: int) -> tuple[str, str]:
    badges = {
        1: ("🥇 #1", "rank-gold"),
        2: ("🥈 #2", "rank-silver"),
        3: ("🥉 #3", "rank-bronze"),
    }
    return badges.get(rank, (f"#{rank}", "rank-default"))


def _results_dataframe(results: list[dict]) -> pd.DataFrame:
    rows = []
    for result in results:
        rows.append(
            {
                "Rank": result["rank"],
                "Candidate": result["name"],
                "Score": f"{result['score'] * 100:.1f}%",
                "Matched Skills": ", ".join(result["matched_skills"]) or "None",
                "Raw Score": result["raw_score"],
            }
        )
    return pd.DataFrame(rows)


if "results" not in st.session_state:
    st.session_state.results = []

with st.sidebar:
    st.title("Resume Screener")
    st.write(
        "Rank candidate resumes against a job description using text extraction, "
        "NLP preprocessing, TF-IDF, and cosine similarity."
    )

    st.subheader("How it works")
    st.markdown(
        """
        1. Upload PDF, DOCX, or TXT resumes.
        2. Paste the target job description.
        3. Review ranked candidates and matched skills.
        """
    )

    st.subheader("Tech stack")
    st.markdown(
        """
        - Streamlit
        - PyPDF2 and pdfplumber
        - python-docx
        - NLTK
        - scikit-learn
        - pandas
        """
    )


st.title("Resume Screening & Candidate Ranking System")

upload_col, jd_col = st.columns([0.4, 0.6], gap="large")

with upload_col:
    uploaded_files = st.file_uploader(
        "Upload Resumes",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
    )

with jd_col:
    job_description = st.text_area("Paste Job Description", height=300)

rank_clicked = st.button("🚀 Rank Candidates", type="primary")

if rank_clicked:
    if not uploaded_files:
        st.error("Upload at least one resume before ranking candidates.")
    elif not job_description.strip():
        st.error("Paste a job description before ranking candidates.")
    else:
        with st.spinner("Analysing resumes..."):
            filenames: list[str] = []
            raw_texts: list[str] = []

            for uploaded_file in uploaded_files:
                text = parser.extract_text(uploaded_file, uploaded_file.name)
                if not text.strip():
                    st.warning(f"Skipped {uploaded_file.name}: no readable text found.")
                    continue
                filenames.append(uploaded_file.name)
                raw_texts.append(text)

            if filenames:
                scores = matcher.compute_similarity(job_description, raw_texts)
                st.session_state.results = ranker.rank_candidates(
                    filenames,
                    scores,
                    raw_texts,
                    job_description,
                )
            else:
                st.session_state.results = []
                st.error("No uploaded resumes contained readable text.")


results = st.session_state.results

if results:
    top_candidate = results[0]
    st.success(
        f"Top candidate: {top_candidate['name']} "
        f"with a {top_candidate['score'] * 100:.1f}% match."
    )

    for candidate in results:
        badge_text, badge_class = _rank_badge(candidate["rank"])
        safe_name = escape(candidate["name"])
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-header">
                    <span class="rank-badge {badge_class}">{badge_text}</span>
                    <span class="candidate-name">{safe_name}</span>
                </div>
                <div class="score-row">
                    <span>Similarity score</span>
                    <strong>{candidate["score"] * 100:.1f}%</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(candidate["score"])

        with st.expander("View Matched Skills"):
            if candidate["matched_skills"]:
                chips = "".join(
                    f'<span class="skill-chip">{escape(skill)}</span>'
                    for skill in candidate["matched_skills"]
                )
                st.markdown(chips, unsafe_allow_html=True)
            else:
                st.write("No listed skills were detected in this resume.")

    results_df = _results_dataframe(results)
    st.subheader("Full Results")
    st.dataframe(results_df, use_container_width=True, hide_index=True)

    csv_data = results_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Results CSV",
        data=csv_data,
        file_name="resume_ranking_results.csv",
        mime="text/csv",
    )
