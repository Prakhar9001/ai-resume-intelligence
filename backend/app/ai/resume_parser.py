import pdfplumber
import re

SECTION_HEADERS = {
    "summary": ["summary", "profile", "objective"],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "internship"
    ],
    "projects": ["projects", "academic projects"],
    "skills": [
        "skills",
        "technical skills",
        "tech stack",
        "technologies"
    ],
    "education": ["education"]
}


def extract_text_from_pdf(pdf_path: str) -> str:
    pages = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text)

    raw_text = "\n".join(pages)
    return clean_text(raw_text)


def clean_text(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = text.replace("•", "-").replace("●", "-")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def detect_sections(text: str) -> dict:
    lines = text.split("\n")
    sections = {}
    current_section = None
    buffer = []

    for line in lines:
        stripped = line.strip()
        upper = stripped.upper()

        found_section = None
        for section, headers in SECTION_HEADERS.items():
            for h in headers:
                if upper.startswith(h.upper()):
                    found_section = section
                    break

        if found_section:
            if current_section and buffer:
                sections[current_section] = "\n".join(buffer).strip()
            current_section = found_section
            buffer = []
        else:
            if current_section:
                buffer.append(stripped)

    if current_section and buffer:
        sections[current_section] = "\n".join(buffer).strip()

    return sections
