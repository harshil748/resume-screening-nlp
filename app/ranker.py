"""Candidate ranking logic for scored resumes."""

from __future__ import annotations

from pathlib import Path

try:
    from app.preprocessor import extract_skills
except ImportError:
    from preprocessor import extract_skills


def _candidate_name(filename: str) -> str:
    stem = Path(filename).stem or "Candidate"
    readable = stem.replace("_", " ").replace("-", " ").strip()
    return readable.title() if readable else "Candidate"


def rank_candidates(
    filenames: list[str],
    scores: list[float],
    raw_texts: list[str],
    job_desc: str,
) -> list[dict]:
    """Sort candidates by score and return ranked result dictionaries."""
    _ = job_desc
    candidates = []

    for filename, score, raw_text in zip(filenames, scores, raw_texts):
        bounded_score = float(max(0.0, min(1.0, score)))
        candidates.append(
            {
                "name": _candidate_name(filename),
                "score": round(bounded_score, 4),
                "matched_skills": extract_skills(raw_text),
                "raw_score": bounded_score,
            }
        )

    candidates.sort(key=lambda item: item["raw_score"], reverse=True)

    for index, candidate in enumerate(candidates, start=1):
        candidate["rank"] = index

    return candidates
