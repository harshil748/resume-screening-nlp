# Resume Screening & Candidate Ranking System

> An AI-powered recruitment assistant that parses resumes and ranks candidates against a job description using Natural Language Processing.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B?logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3%2B-F7931E?logo=scikit-learn&logoColor=white)
![NLTK](https://img.shields.io/badge/NLTK-3.8%2B-lightgreen)

---

## Project Overview
This is an AI recruitment assistant that automates resume screening using NLP techniques.

The system allows a recruiter to upload multiple resumes in PDF, DOCX, or TXT format alongside a job description. It then extracts and preprocesses the text, computes TF-IDF cosine similarity scores, and produces a ranked list of candidates with their match percentage and matched skills — all through a clean Streamlit dashboard.

---

## Features

### Core Features
- **Multi-format Resume Parsing** — Supports PDF (via PyPDF2 + pdfplumber), DOCX (via python-docx), and TXT files
- **Text Preprocessing** — Lowercasing, stopword removal, tokenization, and lemmatization using NLTK and spaCy
- **Similarity Matching** — TF-IDF vectorization with cosine similarity to compare each resume against the job description
- **Candidate Ranking** — Generates a ranked list with match percentage and top matched skills per candidate
- **Interactive Dashboard** — Built with Streamlit; upload resumes, paste JD, and see results instantly

### Bonus Features
- Sentence Transformers / BERT embeddings for semantic matching (beyond keyword overlap)
- Visual score breakdown per candidate

---

## Tech Stack

| Area | Technology |
|------|------------|
| Language | Python 3.10+ |
| NLP | NLTK, spaCy |
| ML / Similarity | scikit-learn (TF-IDF + Cosine Similarity) |
| UI | Streamlit |
| File Parsing | PyPDF2, pdfplumber, python-docx |
| Data Handling | pandas |
| Deployment (optional) | Hugging Face Spaces / Render |

---

## Prerequisites

- Python 3.10 or higher
- pip
- Git

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/resume-screening-nlp.git
cd resume-screening-nlp
```

### 2. Create a Virtual Environment (recommended)

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download Required NLP Data

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
python -m spacy download en_core_web_sm
```

---

## Usage

### Running the App

```bash
streamlit run app/main.py
```

The app will open in your browser at `http://localhost:8501`.

### Steps Inside the App

1. **Upload Resumes** — Click "Browse files" and select one or more PDF / DOCX / TXT resumes
2. **Enter Job Description** — Paste the job description into the text area
3. **Click "Rank Candidates"** — The system processes all resumes and displays a ranked table
4. **Review Results** — See each candidate's match score, skills matched, and their rank

---

## Project Structure

```
resume-screening-nlp/
├── app/
│   ├── main.py             # Streamlit UI — entry point
│   ├── parser.py           # Extract text from PDF / DOCX / TXT
│   ├── preprocessor.py     # NLP preprocessing pipeline
│   ├── matcher.py          # TF-IDF + cosine similarity
│   └── ranker.py           # Candidate ranking logic
├── data/
│   └── sample_resumes/     # Sample resumes for testing
├── notebooks/
│   └── exploration.ipynb   # Exploratory analysis notebook
├── tests/
│   └── test_parser.py      # Unit tests for the parser
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Running Tests

```bash
python -m pytest tests/
```

---

## Sample Output

| Rank | Candidate | Match Score | Matched Skills |
|------|-----------|-------------|----------------|
| 1 | Rahul Sharma | 89% | Python, NLP, scikit-learn, pandas |
| 2 | Priya Patel | 82% | Python, NLTK, Machine Learning |
| 3 | Arjun Mehta | 74% | Python, TF-IDF, Data Analysis |

---

## requirements.txt

```
streamlit>=1.28.0
PyPDF2>=3.0.0
pdfplumber>=0.10.0
python-docx>=1.0.0
nltk>=3.8.0
spacy>=3.7.0
scikit-learn>=1.3.0
pandas>=2.0.0
sentence-transformers>=2.2.0
```

---

## Acknowledgements

- [Kaggle Resume Dataset](https://www.kaggle.com/) — reference dataset
- [Streamlit Docs](https://docs.streamlit.io/) — UI framework
- [scikit-learn TF-IDF](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html) — similarity engine
