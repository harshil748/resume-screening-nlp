from pathlib import Path

from app.parser import extract_text
from app.preprocessor import extract_skills


def test_extract_text_txt(tmp_path: Path):
    resume_path = tmp_path / "resume.txt"
    resume_path.write_text("Python developer with SQL and machine learning experience.", encoding="utf-8")

    with resume_path.open("rb") as file_obj:
        extracted = extract_text(file_obj, resume_path.name)

    assert "Python developer" in extracted
    assert "machine learning" in extracted


def test_extract_text_empty_filename():
    assert extract_text(None, "") == ""


def test_extract_skills_returns_list():
    skills = extract_skills("Experienced with Python, SQL, Docker, and AWS.")

    assert isinstance(skills, list)
    assert "Python" in skills
