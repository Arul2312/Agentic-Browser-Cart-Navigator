from typing import List, Dict

class AmazonSelectors:
    """Centralized Amazon selectors with fallbacks"""
    
    CART_LINK = [
        "#nav-cart",
        "#nav-cart-count-container", 
        ".nav-cart-icon",
        "a[href*='cart']"
    ]
    
    CART_ITEMS = [
        "#sc-active-cart [data-name='Active Items'] .sc-list-item",
        "#sc-active-cart .sc-list-item",
        ".sc-list-item",
        "[data-name='Active Items'] > div"
    ]
    
    ITEM_NAME = [
        ".sc-product-title",
        ".a-size-medium",
        "h3 span",
        ".sc-grid-item-product-title",
        "[data-cy='title']"
    ]
    
    ITEM_PRICE = [
        ".sc-price .a-price-whole",
        ".a-price-whole",
        ".sc-product-price .a-price",
        ".a-price .a-offscreen",
        "[data-cy='price']"
    ]
    
    CHECKOUT_BUTTON = [
        "input[name='proceedToRetailCheckout']",
        ".sc-proceed-to-checkout button",
        "#sc-buy-box-ptc-button",
        "input[value*='checkout']"
    ]
    
    CART_TOTAL = [
        "#sc-subtotal-amount-buybox .a-price .a-offscreen",
        ".sc-subtotal .a-price .a-offscreen", 
        "#sc-subtotal-amount-activecart .a-price-whole",
        ".a-price.a-text-bold .a-offscreen"
    ]

class SelectorManager:
    def __init__(self, selectors_class=AmazonSelectors):
        self.selectors = selectors_class
    
    def get_selectors(self, element_type: str) -> List[str]:
        """Get selectors for a specific element type"""
        return getattr(self.selectors, element_type.upper(), [])