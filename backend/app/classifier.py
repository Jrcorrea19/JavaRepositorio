from __future__ import annotations

from .models import AttentionPriority

PURCHASE_KEYWORDS = ["mío", "mio", "me lo llevo", "separo", "quiero", "reservame"]
PRICE_KEYWORDS = ["precio", "cuánto", "cuanto", "valor"]


def detect_priority(message: str) -> AttentionPriority:
    normalized = message.lower().strip()
    if any(keyword in normalized for keyword in PURCHASE_KEYWORDS):
        return AttentionPriority.PURCHASE
    if any(keyword in normalized for keyword in PRICE_KEYWORDS):
        return AttentionPriority.PRICE
    return AttentionPriority.GENERAL


def detect_product(message: str, product_names: list[str]) -> str | None:
    normalized = message.lower()
    for name in product_names:
        if name.lower() in normalized:
            return name
    return None
