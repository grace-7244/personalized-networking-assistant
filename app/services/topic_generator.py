from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")

def generate_conversation(description: str, interests: list[str]) -> list[str]:
    interests_str = ", ".join(interests) if interests else "general topics"
    prompt = f"At an event about {description}, a great conversation starter about {interests_str} is:"

    outputs = generator(
        prompt,
        max_new_tokens=40,
        num_return_sequences=3,
        do_sample=True,
        temperature=0.8,
        pad_token_id=generator.tokenizer.eos_token_id,
    )

    starters = []
    for out in outputs:
        text = out["generated_text"].replace(prompt, "").strip()
        text = text.split(".")[0].strip() + "."
        if text and text != ".":
            starters.append(text)

    return starters if starters else ["Tell me more about your interest in this event."]