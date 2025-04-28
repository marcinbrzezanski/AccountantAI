from pydantic import BaseModel, Field
from decimal import Decimal
from typing import List, Optional

class Product(BaseModel):
    """
    Dane pojedynczego produktu lub usługi na fakturze.
    """
    name: str = Field(..., description="Nazwa towaru/usługi")
    quantity: Decimal = Field(
        ..., 
        description="Ilość (np. sztuki, kg); dodatnia, maksymalnie 2 miejsca po przecinku"
    )
    unit: str = Field(
        ..., 
        description="Jednostka miary, np. 'szt.', 'kg', 'm³'"
    )
    net_price: Decimal = Field(
        ..., 
        description="Cena jednostkowa netto; dodatnia, maksymalnie 2 miejsca po przecinku"
    )
    vat_rate: Decimal = Field(
        ..., 
        description="Stawka VAT jako ułamek (np. 0.23 dla 23%)"
    )

class Party(BaseModel):
    """
    Dane strony transakcji (sprzedawca lub nabywca).
    """
    name: str = Field(..., description="Pełna nazwa firmy lub imię i nazwisko")
    address: str = Field(..., description="Adres: ulica, kod pocztowy, miasto")
    nip: str = Field(
        ..., 
        description="NIP – ciąg 10 cyfr bez separatorów"
    )
    email: Optional[str] = Field(
        None, 
        description="Adres e-mail kontaktowy (opcjonalnie)"
    )
    phone: Optional[str] = Field(
        None, 
        description="Numer telefonu kontaktowego (opcjonalnie)"
    )
    bank_account: Optional[str] = Field(
        None, 
        description="Numer rachunku bankowego NRB – 26 cyfr bez spacji (opcjonalnie)"
    )

class Invoice(BaseModel):
    """
    Główna struktura faktury VAT (żadne pole nie generuje w JSON‐Schema klucza 'format').
    """
    invoice_number: str = Field(..., description="Unikalny numer faktury, np. 'FV/2025/04/001'")
    issue_date: str = Field(
        ..., 
        description="Data wystawienia faktury w formacie 'YYYY-MM-DD', np. '2025-04-28'"
    )
    due_date: str = Field(
        ..., 
        description="Termin płatności w formacie 'YYYY-MM-DD', np. '2025-05-12'"
    )
    seller: Party = Field(..., description="Dane sprzedawcy")
    buyer: Party = Field(..., description="Dane nabywcy")
    items: List[Product] = Field(
        ..., 
        description="Lista pozycji (produkty/usługi) na fakturze"
    )
    remarks: Optional[str] = Field(
        None, 
        description="Dodatkowe uwagi do faktury (opcjonalnie)"
    )
