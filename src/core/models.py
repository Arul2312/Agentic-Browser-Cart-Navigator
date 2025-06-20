from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum

class ElementType(Enum):
    BUTTON = "button"
    TEXTBOX = "textbox" 
    TABLE = "table"
    LINK = "link"
    FORM = "form"
    IMAGE = "image"

class ActionType(Enum):
    CLICK = "click"
    TYPE = "type"
    SUBMIT = "submit"
    NAVIGATE = "navigate"
    WAIT = "wait"

@dataclass
class PageElement:
    id: str
    type: ElementType
    selector: str
    description: str
    fallback_selectors: Optional[List[str]] = None
    
@dataclass
class Action:
    element_id: str
    action_type: ActionType
    target_page: str
    description: str
    parameters: Optional[Dict[str, Any]] = None

@dataclass
class Page:
    id: str
    url: str
    description: str
    elements: List[PageElement]
    actions: List[Action]

@dataclass
class CartItem:
    name: str
    price: float
    quantity: int
    
    @property
    def total_price(self) -> float:
        return self.price * self.quantity

@dataclass
class TaskResult:
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    cart_items: Optional[List[CartItem]] = None
    total: Optional[float] = None