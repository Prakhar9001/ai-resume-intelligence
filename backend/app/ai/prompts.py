SYSTEM_PROMPT = """
You are an AI assistant that analyzes resumes against job descriptions.

RULES:
- Use ONLY the provided resume chunks.
- DO NOT invent skills, tools, or experience.
- If something is missing, explicitly say it is missing.
- Be concise and factual.
- Output MUST be valid JSON and match the schema exactly.
"""

def build_user_prompt(job_desc_structured: dict, retrieved_chunks: list) -> str:
    chunks_text = []

    for i, c in enumerate(retrieved_chunks, 1):
        chunks_text.append(
            f"[Chunk {i} | Section: {c['section']} | Subsection: {c['subsection']}]\n{c['text']}"
        )

    return f"""
JOB DESCRIPTION (STRUCTURED):
Required Skills: {job_desc_structured.get('required_skills', [])}
Responsibilities: {job_desc_structured.get('responsibilities', [])}
Experience Requirements: {job_desc_structured.get('experience', [])}

RETRIEVED RESUME CHUNKS:
{chr(10).join(chunks_text)}

TASK:
Analyze the resume against the job description.

RETURN JSON IN THIS EXACT FORMAT:
{{
  "skill_match": {{
    "matched": [],
    "missing": []
  }},
  "experience_alignment": {{
    "matched_points": [],
    "gaps": []
  }},
  "section_feedback": {{
    "summary": "",
    "experience": "",
    "skills": ""
  }}
}}
"""
