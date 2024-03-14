import datetime
from pydantic import BaseModel


def add_offset(augend: int, addend: int) -> int:
    return augend + addend


class Ventas(BaseModel):
    concept: list[str]
    sales_date: list[datetime.date]
    expiration: list[datetime.date]
    status: list[str]
    sales_credit: list[bool]
    customer: list[str]
    prod_serv: list[str]
    amount: list[float]
    paid: list[float]
    unit_price: list[float]
    bank_account: list[str]
    way_pay: list[str]
    sector: list[str]
    invoice_folio: list[float]
    date_issue: list[datetime.date]
    final_price: list[float]
    discount: list[float]
    income: list[float]
    product_cost: list[float]
    delivery_type: list[str]
    shipping_cost: list[float]
    shipping_date: list[datetime.date]
    place_delivery: list[str]
    delivery_date: list[datetime.date]
    billig: list[bool]
    profit: list[float]
    margin_gain: list[float]
    payment_status: list[str]
    sales_number: list[float]
    pending_amount: list[float]
    registration_date: list[datetime.date]
    check: list[bool]
