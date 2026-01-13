MAX_CHUNK_WORDS = 300


def chunk_sections(sections: dict) -> list:
    chunks = []

    for section, content in sections.items():
        if section in ["summary", "skills", "education"]:
            chunks.append(make_chunk(section, content))
        else:
            chunks.extend(chunk_by_roles(section, content))

    return chunks


def make_chunk(section, text, subsection=None):
    return {
        "section": section,
        "subsection": subsection,
        "text": text.strip()
    }


def chunk_by_roles(section: str, text: str) -> list:
    lines = text.split("\n")
    chunks = []

    current_role = None
    buffer = []

    for line in lines:
        if is_new_role(line):
            if buffer:
                chunks.append(make_chunk(section, "\n".join(buffer), current_role))
                buffer = []
            current_role = line.strip()
        else:
            buffer.append(line)

    if buffer:
        chunks.append(make_chunk(section, "\n".join(buffer), current_role))

    return split_large_chunks(chunks)


def is_new_role(line: str) -> bool:
    return (
        len(line.split()) <= 8
        and not line.strip().startswith("-")
    )


def split_large_chunks(chunks: list) -> list:
    final_chunks = []

    for chunk in chunks:
        words = chunk["text"].split()
        if len(words) <= MAX_CHUNK_WORDS:
            final_chunks.append(chunk)
        else:
            for i in range(0, len(words), MAX_CHUNK_WORDS):
                split_text = " ".join(words[i:i + MAX_CHUNK_WORDS])
                final_chunks.append({
                    **chunk,
                    "text": split_text
                })

    return final_chunks
