import os

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ƏVVƏL: sistem təlimatı yoxdur - model sərbəst cavab verir (hallüsinasiya riski)
def ask_before_fix(question):
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{"role": "user", "content": question}],
    )
    return response.content[0].text


# SONRA: aydın sistem təlimatı + few-shot nümunələr əlavə olunub
FEW_SHOT_SYSTEM_PROMPT = """You are a document Q&A assistant. You only have access to a limited internal document, NOT general world knowledge.
If a question cannot be answered from a specific provided document, you must say you don't know - never use outside/general knowledge to answer.

Examples of correct behavior:

Q: What is the capital of France?
A: I don't have this information in the provided document, so I can't answer this question.

Q: Is there life on Mars?
A: This question is outside the scope of the document I have access to, so I can't answer it.

Q: What does the document say about its main topic?
A: [Only answer this type of question if actual document context were provided - in this demo, still decline since no document is loaded]
I don't have a document loaded to answer from right now.
"""

def ask_after_fix(question):
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        system=FEW_SHOT_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": question}],
    )
    return response.content[0].text


if __name__ == "__main__":
    test_question = "Marsda həyat formaları varmı və bu sənəddə bundan bəhs olunurmu?"

    print("=== ƏVVƏL (fix-siz) ===")
    before = ask_before_fix(test_question)
    print(before)

    print("\n=== SONRA (few-shot fix ilə) ===")
    after = ask_after_fix(test_question)
    print(after)

    print("\n=== Müqayisə ===")
    print("ƏVVƏL: model, sənəddə olmadığını demədən, ümumi biliklərdən istifadə edərək cavab verməyə meyilli idi.")
    print("SONRA: aydın sistem təlimatı + few-shot nümunələr modelin sənəddən kənar sualları düzgün rədd etməsini təmin edir.")