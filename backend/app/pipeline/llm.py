import json
import re
from typing import Optional

genai = None
genai_types = None

try:
    from google import genai
    from google.genai import types as genai_types
    USE_NEW_SDK = True
except ImportError:
    try:
        import google.generativeai as genai_old
    except ImportError:
        genai_old = None
    USE_NEW_SDK = False

from app.core.config import settings

EXTRACTION_PROMPT = """You are a legal compliance analyst for Karnataka government of India.
Extract ONLY actionable directives from the ORDER/DIRECTIONS section of the judgment below.

RULES:
1. Only extract sentences containing: "shall", "is directed to", "are directed to", "must", "is hereby ordered", "is required to", "forthwith", "stand directed", "hereby directed"
2. For each directive output a JSON object with these exact keys:
   - directive_text: the full directive sentence (string)
   - responsible_designation: job title of the person responsible e.g. "Secretary, Revenue Department" (string)
   - responsible_department: department name (string)
   - action_type: one of "compliance", "report", "payment", "regularisation", "investigation" (string)
   - due_date_text: the deadline phrase from the text, e.g. "within 30 days", "forthwith", or null
   - source_sentence: copy the directive sentence verbatim (string)
   - confidence: your confidence 0.0 to 1.0 (number)

3. Output ONLY a valid JSON array. No explanation. No markdown. No preamble.
4. If no directives found, output: []

CASE: {case_id}
ORDER DATE: {order_date}

ORDER SECTION:
{order_text}
"""

def extract_actions_from_text(order_text: str, case_id: str = "UNKNOWN", order_date: str = "") -> list[dict]:
    """Call Gemini to extract structured action items from order section."""
    prompt = EXTRACTION_PROMPT.format(
        case_id=case_id,
        order_date=order_date or "Not specified",
        order_text=order_text[:4000]
    )

    try:
        if USE_NEW_SDK:
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            response = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
                config=genai_types.GenerateContentConfig(
                    temperature=0.1,
                    max_output_tokens=2000,
                )
            )
            text = response.text.strip()
        else:
            if genai_old is None:
                raise RuntimeError("No Gemini SDK installed")
            genai_old.configure(api_key=settings.GEMINI_API_KEY)
            model = genai_old.GenerativeModel(settings.GEMINI_MODEL)
            response = model.generate_content(prompt)
            text = response.text.strip()

        # Clean markdown fences if present
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        text = text.strip()

        if not text:
            return _fallback_extraction(order_text)

        if text == '[]':
            return _fallback_extraction(order_text)

        data = json.loads(text)
        if isinstance(data, list) and data:
            return data
        return _fallback_extraction(order_text)

    except json.JSONDecodeError:
        # Try to extract JSON array from response
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass
        return _fallback_extraction(order_text)
    except Exception as e:
        print(f"Gemini API error: {e}")
        return _fallback_extraction(order_text)

def _fallback_extraction(text: str) -> list[dict]:
    """Rule-based fallback if Gemini fails."""
    from app.pipeline.classifier import classify_sentence, detect_department
    results = []
    sentences = re.split(r'(?<=[.!?])\s+', text)
    for sent in sentences:
        classification = classify_sentence(sent)
        if classification["is_directive"] and classification["tier"] == "HIGH":
            dept, dept_conf = detect_department(sent)
            results.append({
                "directive_text": sent.strip(),
                "responsible_designation": f"Secretary, {dept}",
                "responsible_department": dept,
                "action_type": "compliance",
                "due_date_text": None,
                "source_sentence": sent.strip(),
                "confidence": classification["confidence"] * 0.8
            })
    return results[:10]
