from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

CANDIDATE_LABELS = [
    "technology", "artificial intelligence", "sustainability",
    "urban planning", "healthcare", "finance", "education",
    "climate change", "business", "science", "art", "networking"
]

def analyze_event(description: str) -> list[str]:
    result = classifier(description, candidate_labels=CANDIDATE_LABELS, multi_label=True)
    themes = [label for label, score in zip(result["labels"], result["scores"]) if score > 0.3]
    return themes[:5] if themes else [result["labels"][0]]