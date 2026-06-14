"""NLP preprocessing and skill extraction helpers."""

from __future__ import annotations

import re

import nltk


for _resource in ("punkt", "stopwords", "wordnet"):
    try:
        nltk.download(_resource, quiet=True)
    except Exception:
        pass

try:
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import word_tokenize
except Exception:
    stopwords = None
    WordNetLemmatizer = None
    word_tokenize = None


_FALLBACK_STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "with",
}


try:
    _STOPWORDS = set(stopwords.words("english")) if stopwords else _FALLBACK_STOPWORDS
except Exception:
    _STOPWORDS = _FALLBACK_STOPWORDS

try:
    _LEMMATIZER = WordNetLemmatizer() if WordNetLemmatizer else None
except Exception:
    _LEMMATIZER = None


TECH_SKILLS = [
    "Python",
    "Java",
    "JavaScript",
    "C++",
    "SQL",
    "NoSQL",
    "MongoDB",
    "MySQL",
    "PostgreSQL",
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "Computer Vision",
    "TensorFlow",
    "PyTorch",
    "Keras",
    "scikit-learn",
    "pandas",
    "NumPy",
    "Matplotlib",
    "Seaborn",
    "Streamlit",
    "Flask",
    "Django",
    "FastAPI",
    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "GCP",
    "Git",
    "GitHub",
    "Linux",
    "React",
    "Node.js",
    "HTML",
    "CSS",
    "REST API",
    "Agile",
    "Scrum",
    "Data Analysis",
    "Power BI",
    "Tableau",
    "Excel",
    "R",
    "MATLAB",
    "Spark",
    "Hadoop",
]


def _tokenize(text: str) -> list[str]:
    if word_tokenize is not None:
        try:
            return word_tokenize(text)
        except Exception:
            pass
    return text.split()


def _lemmatize(token: str) -> str:
    if _LEMMATIZER is not None:
        try:
            return _LEMMATIZER.lemmatize(token)
        except Exception:
            return token
    return token


def preprocess(text: str) -> str:
    """Clean resume or job-description text for vector-based matching."""
    if not text:
        return ""

    normalized = text.lower()
    normalized = re.sub(r"[^a-z0-9\s]", " ", normalized)
    tokens = _tokenize(normalized)
    cleaned_tokens = [
        _lemmatize(token)
        for token in tokens
        if token and token not in _STOPWORDS and len(token) > 1
    ]
    return " ".join(cleaned_tokens)


def _skill_regex(skill: str) -> re.Pattern[str]:
    escaped = re.escape(skill)
    escaped = escaped.replace(r"\ ", r"\s+")
    return re.compile(rf"(?<![A-Za-z0-9+#.]){escaped}(?![A-Za-z0-9+#.])", re.IGNORECASE)


def extract_skills(text: str) -> list[str]:
    """Return deduplicated technology skills found in text."""
    if not text:
        return []

    matched: list[str] = []
    seen: set[str] = set()
    for skill in TECH_SKILLS:
        if skill.lower() in seen:
            continue
        if _skill_regex(skill).search(text):
            matched.append(skill)
            seen.add(skill.lower())
    return matched
