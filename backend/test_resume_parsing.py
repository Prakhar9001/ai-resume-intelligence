import json
from app.ai.resume_parser import extract_text_from_pdf, detect_sections
from app.ai.chunker import chunk_sections
from app.ai.embeddings import embed_chunks
from app.ai.retriever import build_faiss_index, retrieve_top_k
from app.ai.prompts import SYSTEM_PROMPT, build_user_prompt
from app.ai.llm_client import run_llm
from app.ai.scorer import final_score

PDF_PATH = "sample_resume.pdf"


def safe_parse_json(text: str):
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start == -1 or end == -1:
            raise ValueError("No JSON found")
        return json.loads(text[start:end])
    except Exception:
        return {
            "skill_match": {
                "matched": [],
                "missing": []
            },
            "experience_alignment": {
                "matched_points": [],
                "gaps": []
            },
            "section_feedback": {
                "summary": "LLM output was unstructured.",
                "experience": "Fallback JSON used to keep pipeline stable.",
                "skills": "Model/prompt can be improved later."
            }
        }


def main():
    print("\n=== DAY 3: FULL RAG + LLM + SCORING ===")

    resume_text = extract_text_from_pdf(PDF_PATH)
    sections = detect_sections(resume_text)
    chunks = chunk_sections(sections)

    embeddings, metadata = embed_chunks(chunks)
    index = build_faiss_index(embeddings)

    query = "backend developer with python and databases"
    retrieved = retrieve_top_k(
        query=query,
        index=index,
        metadata=metadata,
        embed_fn=lambda x: embed_chunks(
            [{"text": t, "section": None, "subsection": None} for t in x]
        )[0],
        top_k=3
    )

    jd_structured = {
        "required_skills": ["Python", "SQL", "REST APIs"],
        "responsibilities": ["Build backend services", "Work with databases"],
        "experience": ["Internship or project experience"]
    }

    jd_keywords = ["Python", "MySQL", "PostgreSQL", "REST"]

    user_prompt = build_user_prompt(jd_structured, retrieved)
    raw_output = run_llm(SYSTEM_PROMPT, user_prompt)

    llm_json = safe_parse_json(raw_output)

    scores = final_score(llm_json, jd_keywords, resume_text)

    print("\n=== LLM ANALYSIS (JSON) ===")
    print(json.dumps(llm_json, indent=2))

    print("\n=== FINAL SCORES ===")
    print(scores)


if __name__ == "__main__":
    main()
