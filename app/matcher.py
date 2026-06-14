"""Similarity scoring between job descriptions and resume text."""

from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    from app.preprocessor import preprocess
except ImportError:
    from preprocessor import preprocess


def compute_similarity(job_desc: str, resume_texts: list[str]) -> list[float]:
    """Compute TF-IDF cosine similarity scores for resumes against a job description."""
    if not resume_texts:
        return []

    processed_job = preprocess(job_desc)
    processed_resumes = [preprocess(text) for text in resume_texts]

    if not processed_job or not any(processed_resumes):
        return [0.0 for _ in resume_texts]

    corpus = [processed_job, *processed_resumes]
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)

    try:
        tfidf_matrix = vectorizer.fit_transform(corpus)
    except ValueError:
        return [0.0 for _ in resume_texts]

    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    return [float(max(0.0, min(1.0, score))) for score in similarities]
