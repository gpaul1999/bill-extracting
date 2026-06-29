# Bill Extraction Service

Extract structured information from bills, invoices, and receipts using AI.

Supports both raw text and file uploads (PDF, images). Powered by **Groq API** (Llama 3.3-70b).

## Requirements

- Python 3.11+
- Tesseract OCR (for image files)
- Groq API key — get one free at [console.groq.com](https://console.groq.com)

### Install Tesseract

```bash
# Ubuntu/Debian
sudo apt install tesseract-ocr

# macOS
brew install tesseract
```

## Setup

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env and set your GROQ_API_KEY

# 3. Start the server
uvicorn app.main:app --reload
```

Server runs at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

---

## API

### `GET /health`

Check if the service is running.

```bash
curl http://localhost:8000/health
```

```json
{ "status": "ok" }
```

---

### `POST /extract/text`

Extract bill information from raw text.

**Request body:**

```json
{
  "text": "<paste your bill text here>"
}
```

**Example:**

```bash
curl -X POST http://localhost:8000/extract/text \
  -H "Content-Type: application/json" \
  -d '{
    "text": "INVOICE #INV-2024-001\nFrom: ABC Corp, 123 Main St\nTo: John Doe\nDate: 2024-01-15\nDue: 2024-02-15\n\nWeb Design Service  1  $1,500.00\nHosting (1 year)    1  $120.00\n\nSubtotal: $1,620.00\nTax (10%): $162.00\nTotal: $1,782.00\nStatus: Unpaid"
  }'
```

---

### `POST /extract/file`

Extract bill information from a PDF or image file.

**Supported formats:** PDF, PNG, JPG/JPEG, WEBP, TIFF

**Max file size:** 10MB

```bash
curl -X POST http://localhost:8000/extract/file \
  -F "file=@invoice.pdf"
```

---

## Response Schema

All endpoints return the same JSON structure:

```json
{
  "vendor": {
    "name": "ABC Corp",
    "address": "123 Main St",
    "phone": null,
    "email": null,
    "website": null,
    "tax_id": null
  },
  "customer": {
    "name": "John Doe",
    "address": null,
    "phone": null,
    "email": null,
    "customer_id": null
  },
  "bill_info": {
    "bill_number": "INV-2024-001",
    "bill_type": "invoice",
    "issue_date": "2024-01-15",
    "due_date": "2024-02-15",
    "purchase_order": null,
    "reference": null
  },
  "line_items": [
    {
      "description": "Web Design Service",
      "quantity": 1,
      "unit": null,
      "unit_price": 1500.00,
      "total": 1500.00,
      "sku": null,
      "tax_rate": null
    },
    {
      "description": "Hosting (1 year)",
      "quantity": 1,
      "unit": null,
      "unit_price": 120.00,
      "total": 120.00,
      "sku": null,
      "tax_rate": null
    }
  ],
  "pricing": {
    "subtotal": 1620.00,
    "discount": null,
    "discount_percent": null,
    "tax": 162.00,
    "tax_percent": 10.0,
    "shipping": null,
    "total": 1782.00,
    "currency": "USD"
  },
  "payment": {
    "method": null,
    "status": "unpaid",
    "bank_account": null,
    "transaction_id": null,
    "paid_date": null
  },
  "notes": null,
  "raw_text_preview": "INVOICE #INV-2024-001\nFrom: ABC Corp..."
}
```

Fields not found in the bill are returned as `null`.
