from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Donor:
    donor_id: str
    name: str
    nic: str
    phone: str
    email: str
    username: str
    password: str
    is_verified: bool = True
    created_at: Optional[str] = None

@dataclass
class Child:
    id: int
    name: str
    birthday: str
    guardian: str
    phone: str
    milk_type: str
    last_issue: Optional[str] = None
    created_at: Optional[str] = None

@dataclass
class Donation:
    id: int
    donor_id: str
    amount: float
    payment_slip: Optional[str] = None
    timestamp: str = None
    receipt_generated: bool = False

@dataclass
class Inventory:
    product_id: int
    name: str
    price: float
    stock: int
    min_stock_level: int = 20
    image_path: Optional[str] = None