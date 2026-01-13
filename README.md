# ai-resume-intelligence
AI-assisted resume and job description analysis system
# AI Resume Intelligence

AI Resume Intelligence is an end-to-end AI-assisted resume and job description analysis system.  
It uses a combination of **rule-based heuristics**, **vector similarity search (FAISS)**, and **LLM-assisted analysis** to generate explainable resume–job match scores.

> ⚠️ This project is an **MVP focused on architecture, robustness, and explainability**, not a production-grade hiring decision engine.

---

## 🔍 What This Project Does

- Parses resumes (PDF)
- Splits resumes into semantic sections
- Embeds resume chunks and job descriptions
- Retrieves the most relevant resume sections using FAISS
- Applies **rule-based scoring** for deterministic results
- Uses an LLM for qualitative analysis (with safe fallback handling)
- Presents results through a clean, modern web UI

---

## 🧠 Key Design Principles

- **Explainability over black-box scoring**
- **Deterministic fallbacks** when LLM output is unreliable
- **Heuristic scoring**, not absolute hiring judgments
- **End-to-end product thinking**, not just model usage

---

## 🏗️ Architecture Overview

Resume (PDF)
↓
Text Extraction & Section Detection
↓
Chunking
↓
Embeddings (Sentence Transformers)
↓
FAISS Vector Index
↓
Relevant Resume Chunks
↓
Rule-Based + LLM-Assisted Analysis
↓
Scoring Engine
↓
Flask API
↓
Next.js + Tailwind UI

## ⚙️ Tech Stack

### Backend
- Python
- Flask + Flask-CORS
- FAISS
- Sentence Transformers
- Hugging Face Transformers
- pdfplumber

### Frontend
- Next.js (App Router)
- Tailwind CSS

---

## 📊 Scoring Philosophy

The system produces **heuristic match scores**, broken down into:
- Skill Alignment
- Experience Signals
- Keyword Coverage

> These scores are **relative indicators**, designed to help understand alignment patterns — not to make hiring decisions.

Low scores do **not** mean a candidate is weak.  
They indicate **partial alignment** with a given job description.

---

## 🛡️ Why Rule-Based + LLM?

Local LLMs may return:
- Unstructured output
- Incomplete JSON
- Inconsistent formatting

To ensure system stability:
- Rule-based scoring guarantees **deterministic output**
- LLMs are used only for **qualitative insights**
- Fallback logic prevents crashes or misleading results

This mirrors how real-world AI systems are designed.

---

## 🚀 Current Status

- ✅ End-to-end working MVP
- ✅ Clean, professional UI
- ✅ Robust backend with fallbacks
- 🔜 Deployment (Vercel + Render)

---

## 📌 Disclaimer

This project is intended for:
- Learning
- Demonstrating AI system design
- Portfolio and interview discussions

It is **not** a replacement for real recruitment tools.

---

## 📄 License

MIT
