from flask import Flask, request, jsonify
from flask_cors import CORS
import tempfile
import os
import json

from app.ai.resume_parser import extract_text_from_pdf, detect_sections
from app.ai.chunker import chunk_sections
from app.ai.embeddings import embed_chunks
from app.ai.retriever import build_faiss_index, retrieve_top_k
from app.ai.prompts import SYSTEM_PROMPT, build_user_prompt
from app.ai.llm_client import run_llm
from app.ai.scorer import final_score, rule_based_analysis

app = Flask(__name__)
CORS(app)


@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200


@app.route("/analyze", methods=["POST"])
def analyze_resume():
    if "resume" not in request.files:
        return jsonify({"error": "Resume file missing"}), 400

    resume_file = request.files["resume"]
    job_description = request.form.get("job_description", "")

    if not job_description.strip():
        return jsonify({"error": "Job description missing"}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        resume_path = tmp.name
        resume_file.save(resume_path)

    try:
        resume_text = extract_text_from_pdf(resume_path)
        sections = detect_sections(resume_text)
        chunks = chunk_sections(sections)

        embeddings, metadata = embed_chunks(chunks)
        index = build_faiss_index(embeddings)

        retrieved = retrieve_top_k(
            query=job_description,
            index=index,
            metadata=metadata,
            embed_fn=lambda x: embed_chunks(
                [{"text": t, "section": None, "subsection": None} for t in x]
            )[0],
            top_k=3
        )

        jd_structured = {
            "required_skills": [],
            "responsibilities": [],
            "experience": []
        }

        user_prompt = build_user_prompt(jd_structured, retrieved)
        raw_output = run_llm(SYSTEM_PROMPT, user_prompt)

        try:
            start = raw_output.find("{")
            end = raw_output.rfind("}") + 1
            llm_json = json.loads(raw_output[start:end])
        except Exception:
            llm_json = rule_based_analysis(resume_text, job_description)

        scores = final_score(llm_json, [], resume_text)

        return jsonify({
            "analysis": llm_json,
            "scores": scores
        })

    finally:
        os.remove(resume_path)


if __name__ == "__main__":
    app.run(debug=True)
