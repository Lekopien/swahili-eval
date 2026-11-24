import anthropic
from sacrebleu.metrics import CHRF

_chrf = CHRF()
JUDGE_MODEL = "claude-sonnet-5-5"


def chrf(output: str, reference: str) -> float:
    """Character n-gram F-score, 0-100. Robust for morphologically rich languages like Swahili."""
    return _chrf.sentence_score(output, [reference]).score


def judge(prompt: str, output: str, reference: str) -> int:
    """LLM-as-judge: score 1-5 for correctness and fluency against the reference."""
    msg = anthropic.Anthropic().messages.create(
        model=JUDGE_MODEL,
        max_tokens=10,
        system="Rate the answer from 1 (wrong) to 5 (excellent) for correctness and natural fluency in the target language, using the reference as a guide. Reply with the digit only.",
        messages=[{"role": "user", "content": f"Task: {prompt}\nReference: {reference}\nAnswer: {output}"}],
    )
    try:
        return int(msg.content[0].text.strip()[0])
    except (ValueError, IndexError):
        return 0
