from transformers import pipeline

_llm = None

def get_llm():
    global _llm
    if _llm is None:
        _llm = pipeline(
            task="text2text-generation",
            model="google/flan-t5-base",
            max_new_tokens=512,
            truncation=True,
        )
    return _llm


def run_llm(system_prompt: str, user_prompt: str) -> str:
    llm = get_llm()
    prompt = system_prompt + "\n\n" + user_prompt
    output = llm(prompt)
    return output[0]["generated_text"]
