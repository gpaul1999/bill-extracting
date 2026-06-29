from pydantic import BaseModel
from typing import Optional


class VendorInfo(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    tax_id: Optional[str] = None


class CustomerInfo(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    customer_id: Optional[str] = None


class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    unit_price: Optional[float] = None
    total: Optional[float] = None
    sku: Optional[str] = None
    tax_rate: Optional[float] = None


class BillInfo(BaseModel):
    bill_number: Optional[str] = None
    bill_type: Optional[str] = None  # invoice, receipt, quote, etc.
    issue_date: Optional[str] = None
    due_date: Optional[str] = None
    purchase_order: Optional[str] = None
    reference: Optional[str] = None


class Pricing(BaseModel):
    subtotal: Optional[float] = None
    discount: Optional[float] = None
    discount_percent: Optional[float] = None
    tax: Optional[float] = None
    tax_percent: Optional[float] = None
    shipping: Optional[float] = None
    total: Optional[float] = None
    currency: Optional[str] = None


class PaymentInfo(BaseModel):
    method: Optional[str] = None  # cash, card, bank transfer, etc.
    status: Optional[str] = None  # paid, unpaid, partial
    bank_account: Optional[str] = None
    transaction_id: Optional[str] = None
    paid_date: Optional[str] = None


class BillExtractResult(BaseModel):
    vendor: VendorInfo = VendorInfo()
    customer: CustomerInfo = CustomerInfo()
    bill_info: BillInfo = BillInfo()
    line_items: list[LineItem] = []
    pricing: Pricing = Pricing()
    payment: PaymentInfo = PaymentInfo()
    notes: Optional[str] = None
    raw_text_preview: Optional[str] = None
