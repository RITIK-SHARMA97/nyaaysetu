import re
from typing import Optional

ORDER_PATTERNS = [
    r'(?i)(IN\s+THE\s+RESULT|IN\s+VIEW\s+OF\s+THE\s+ABOVE|FOR\s+THE\s+FOREGOING\s+REASONS|ACCORDINGLY|THEREFORE|HENCE|IN\s+THE\s+CIRCUMSTANCES|ORDER)',
    r'(?i)(OPERATIVE\s+PART|DIRECTIONS?|THE\s+FOLLOWING\s+DIRECTIONS?)',
    r'(?i)(DISPOSED\s+OFF?|ALLOWED|DISMISSED)',
]

def extract_pages(pdf_path: str) -> list[dict]:
    import fitz  # PyMuPDF

    doc = fitz.open(pdf_path)
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text("text")
        blocks = page.get_text("dict")["blocks"]
        words = page.get_text("words")  # (x0,y0,x1,y1,word,block,line,word_num)
        is_scanned = len(text.strip()) < 100 and len(blocks) > 0
        pages.append({
            "page_num": i + 1,
            "text": text,
            "words": [(w[0], w[1], w[2], w[3], w[4]) for w in words],
            "is_scanned": is_scanned,
            "char_count": len(text.strip())
        })
    doc.close()
    return pages

def detect_page_type(text: str) -> str:
    kannada_chars = re.findall(r'[\u0C80-\u0CFF]', text)
    if len(kannada_chars) > 20:
        return "kannada"
    if len(text.strip()) < 100:
        return "scanned"
    return "digital"

def find_order_section(pages: list[dict]) -> tuple[str, int]:
    """Returns (order_section_text, start_page_num)"""
    full_text = ""
    page_map = {}  # char_offset -> page_num
    offset = 0
    for p in pages:
        page_map[offset] = p["page_num"]
        full_text += p["text"] + "\n"
        offset += len(p["text"]) + 1

    best_pos = _find_order_start(pages, full_text)

    order_text = _clean_order_text(full_text[best_pos:])
    # Find which page this falls on
    start_page = 1
    for char_offset, page_num in sorted(page_map.items()):
        if char_offset <= best_pos:
            start_page = page_num

    return order_text[:5000], start_page  # Limit to 5000 chars for LLM

def _find_order_start(pages: list[dict], full_text: str) -> int:
    best_candidate = None
    fallback_pos = len(full_text) // 2
    offset = 0

    for page in pages:
        page_text = page["text"]
        for match in re.finditer(r"[^\n]+", page_text):
            line = match.group().strip()
            if not line or _is_footer_line(line):
                continue

            score = _score_order_line(line)
            if score <= 0:
                continue

            start = offset + match.start()
            if start > fallback_pos:
                fallback_pos = start

            candidate = (score, start)
            if best_candidate is None or candidate > best_candidate:
                best_candidate = candidate

        offset += len(page_text) + 1

    return best_candidate[1] if best_candidate else fallback_pos

def _score_order_line(line: str) -> int:
    normalized = " ".join(line.lower().split())
    if _is_footer_line(normalized):
        return 0
    if "following directions are issued" in normalized:
        return 6
    if any(marker in normalized for marker in ["accordingly", "therefore", "hence", "in the result", "operative part"]):
        return 5
    if "is hereby directed" in normalized or "shall" in normalized or "directed to" in normalized:
        return 4
    if "directions" in normalized:
        return 3
    if normalized == "order":
        return 1
    return 0

def _is_footer_line(line: str) -> bool:
    normalized = " ".join(line.lower().split())
    return (
        "official order" in normalized
        or normalized.startswith("page ")
        or normalized == "judge"
        or normalized == "sd/-"
    )

def _clean_order_text(text: str) -> str:
    lines = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or _is_footer_line(line):
            continue
        lines.append(raw_line)
    return "\n".join(lines).strip() + "\n\n" if lines else ""

def get_word_bbox(pages: list[dict], target_text: str, page_num: int) -> Optional[list]:
    """Find bounding box of a text fragment in a specific page."""
    if page_num <= 0 or page_num > len(pages):
        return None
    page = pages[page_num - 1]
    words = page.get("words", [])
    # Find first word of target_text
    first_word = target_text.strip().split()[0].lower() if target_text.strip() else ""
    for w in words:
        if w[4].lower().startswith(first_word[:4]):
            return [w[0], w[1], w[2], w[3]]
    return None

def find_text_location(
    pages: list[dict],
    target_text: str,
    preferred_page: Optional[int] = None,
) -> tuple[Optional[int], Optional[list]]:
    normalized_tokens = _tokenize(target_text)
    if not normalized_tokens:
        return None, None

    page_lookup = {page["page_num"]: page for page in pages}
    page_order = []
    if preferred_page and preferred_page in page_lookup:
        page_order.append(preferred_page)
    page_order.extend(page["page_num"] for page in pages if page["page_num"] not in page_order)

    for page_num in page_order:
        page = page_lookup.get(page_num)
        if not page:
            continue
        bbox = _find_bbox_on_page(page.get("words", []), normalized_tokens)
        if bbox:
            return page_num, bbox

    return None, None

def _find_bbox_on_page(words: list, target_tokens: list[str]) -> Optional[list]:
    normalized_words = []
    for word in words:
        token = _normalize_token(word[4])
        if token:
            normalized_words.append((token, word))

    if not normalized_words:
        return None

    min_match_len = max(1, min(len(target_tokens), 4))
    for start in range(len(normalized_words)):
        matched_words = []
        target_index = 0
        cursor = start

        while cursor < len(normalized_words) and target_index < len(target_tokens):
            token, original = normalized_words[cursor]
            if token != target_tokens[target_index]:
                break
            matched_words.append(original)
            target_index += 1
            cursor += 1

        if target_index >= min_match_len:
            x0 = min(word[0] for word in matched_words)
            y0 = min(word[1] for word in matched_words)
            x1 = max(word[2] for word in matched_words)
            y1 = max(word[3] for word in matched_words)
            return [x0, y0, x1, y1]

    return None

def _tokenize(text: str) -> list[str]:
    return [_normalize_token(part) for part in text.split() if _normalize_token(part)]

def _normalize_token(token: str) -> str:
    return re.sub(r"[^\w]", "", token.lower())

def get_pdf_metadata(pdf_path: str) -> dict:
    import fitz  # PyMuPDF

    doc = fitz.open(pdf_path)
    meta = doc.metadata
    total_pages = len(doc)
    doc.close()
    return {"total_pages": total_pages, "title": meta.get("title", ""), "author": meta.get("author", "")}
