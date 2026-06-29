import json
from groq import Groq
from app.schema import BillExtractResult

SYSTEM_PROMPT = """You are a bill/invoice data extraction expert.
Extract all information from the provided bill text and return ONLY a valid JSON object.
Use null for any field you cannot find. Do not add any explanation or markdown.

The JSON must follow this exact structure:
{
  "vendor": {
    "name": null,
    "address": null,
    "phone": null,
    "email": null,
    "website": null,
    "tax_id": null
  },
  "customer": {
    "name": null,
    "address": null,
    "phone": null,
    "email": null,
    "customer_id": null
  },
  "bill_info": {
    "bill_number": null,
    "bill_type": null,
    "issue_date": null,
    "due_date": null,
    "purchase_order": null,
    "reference": null
  },
  "line_items": [
    {
      "description": null,
      "quantity": null,
      "unit": null,
      "unit_price": null,
      "total": null,
      "sku": null,
      "tax_rate": null
    }
  ],
  "pricing": {
    "subtotal": null,
    "discount": null,
    "discount_percent": null,
    "tax": null,
    "tax_percent": null,
    "shipping": null,
    "total": null,
    "currency": null
  },
  "payment": {
    "method": null,
    "status": null,
    "bank_account": null,
    "transaction_id": null,
    "paid_date": null
  },
  "notes": null
}"""


def extract_bill(client: Groq, text: str) -> BillExtractResult:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Extract information from this bill:\n\n{text}"},
        ],
        temperature=0,
        max_tokens=2048,
    )

    raw = response.choices[0].message.content.strip()

    # Strip markdown code blocks if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    data = json.loads(raw)
    result = BillExtractResult(**data)
    result.raw_text_preview = text[:500] if len(text) > 500 else text
    return result
