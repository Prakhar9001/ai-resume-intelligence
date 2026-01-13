import re

COMMON_SKILLS = [
    "python", "java", "c++", "sql", "mysql", "postgresql",
    "flask", "django", "react", "node", "rest", "api",
    "machine learning", "deep learning", "nlp",
    "faiss", "docker", "aws", "git"
]


def extract_skills_from_text(text: str):
    text = text.lower()
    found = set()

    for skill in COMMON_SKILLS:
        if skill in text:
            found.add(skill.title())

    return list(found)


def rule_based_analysis(resume_text: str, jd_text: str):
    resume_skills = extract_skills_from_text(resume_text)
    jd_skills = extract_skills_from_text(jd_text)

    matched = sorted(set(resume_skills) & set(jd_skills))
    missing = sorted(set(jd_skills) - set(resume_skills))

    exp_keywords = ["intern", "project", "experience", "developed", "built"]
    matched_points = []
    gaps = []

    for kw in exp_keywords:
        if kw in resume_text.lower():
            matched_points.append(f"Mentions {kw}")
        else:
            gaps.append(f"No evidence of {kw}")

    return {
        "skill_match": {
            "matched": matched,
            "missing": missing
        },
        "experience_alignment": {
            "matched_points": matched_points,
            "gaps": gaps
        }
    }


def score_skill_match(matched: list, missing: list) -> float:
    total = len(matched) + len(missing)
    if total == 0:
        return 0.0
    return (len(matched) / total) * 40.0


def score_experience(matched_points: list, gaps: list) -> float:
    score = min(len(matched_points) * 6.0, 30.0)
    penalty = min(len(gaps) * 2.0, 10.0)
    return max(0.0, score - penalty)


def score_keywords(jd_keywords: list, resume_text: str) -> float:
    if not jd_keywords:
        return 0.0
    hits = sum(1 for k in jd_keywords if k.lower() in resume_text.lower())
    return (hits / len(jd_keywords)) * 30.0


def final_score(llm_json: dict, jd_keywords: list, resume_text: str):
    s1 = score_skill_match(
        llm_json["skill_match"]["matched"],
        llm_json["skill_match"]["missing"]
    )
    s2 = score_experience(
        llm_json["experience_alignment"]["matched_points"],
        llm_json["experience_alignment"]["gaps"]
    )
    s3 = score_keywords(jd_keywords, resume_text)

    total = round(s1 + s2 + s3, 2)

    return {
        "skill_score": round(s1, 2),
        "experience_score": round(s2, 2),
        "keyword_score": round(s3, 2),
        "final_score": total
    }
