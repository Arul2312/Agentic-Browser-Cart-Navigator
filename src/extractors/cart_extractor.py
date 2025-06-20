from playwright.async_api import Page as PlaywrightPage
from typing import List, Dict, Any
import re
import asyncio

class CartExtractor:
    """Cart extractor for Amazon cart page"""
    
    def __init__(self, page: PlaywrightPage):
        self.page = page
    
    async def extract_cart_info(self, page: PlaywrightPage = None) -> Dict[str, Any]:
        """
        Extract cart information from the current page.
        
        Args:
            page: Playwright page object (optional, uses self.page if not provided)
            
        Returns:
            dict: Cart information including items and total
        """
        # Use provided page or fallback to self.page
        current_page = page or self.page
        
        cart_info = {
            'items': [],
            'total': 0.0,
            'subtotal': 0.0,
            'item_count': 0
        }
        
        try:
            # Wait a moment for cart to load
            await asyncio.sleep(3)
            
            # Check if cart is empty
            empty_selectors = [
                "[data-name='empty-cart']",
                ".sc-empty-cart",
                "#sc-empty-cart",
                "text=Your cart is empty",
                "text=Your Shopping Cart is empty"
            ]
            
            for selector in empty_selectors:
                try:
                    if await current_page.locator(selector).is_visible(timeout=3000):
                        return cart_info  # Return empty cart info
                except:
                    continue
            
            # Extract items
            await self._extract_items(current_page, cart_info)
            
            # Extract total/subtotal
            await self._extract_totals(current_page, cart_info)
            
        except Exception as e:
            print(f"Error extracting cart info: {e}")
        
        return cart_info
    
    async def _extract_items(self, page: PlaywrightPage, cart_info: Dict[str, Any]):
        """Extract individual cart items"""
        item_selectors = [
            "[data-name='Active Items'] .sc-list-item",
            ".sc-list-item-content",
            ".sc-list-item",
            "[data-item-index]",
            ".a-spacing-mini"
        ]
        
        for selector in item_selectors:
            try:
                items = await page.query_selector_all(selector)
                if items:
                    print(f"Found {len(items)} items with selector: {selector}")
                    for item in items[:10]:  # Limit to 10 items
                        item_info = await self._extract_single_item(item)
                        if item_info:
                            cart_info['items'].append(item_info)
                    break
            except Exception as e:
                continue
        
        cart_info['item_count'] = len(cart_info['items'])
    
    async def _extract_single_item(self, item_locator) -> Dict[str, Any]:
        """Extract information from a single cart item"""
        item_info = {}
        
        try:
            # Extract item name
            name_selectors = [
                ".sc-product-title",
                "[data-truncate-title]",
                ".a-size-medium",
                "h4",
                ".s-size-mini",
                "h3 span",
                ".a-link-normal"
            ]
            
            for selector in name_selectors:
                try:
                    name_element = await item_locator.query_selector(selector)
                    if name_element:
                        name = await name_element.text_content()
                        if name and len(name.strip()) > 3:
                            item_info['name'] = name.strip()
                            break
                except:
                    continue
            
            # Extract price
            price_selectors = [
                ".sc-price",
                ".a-price-whole",
                "[data-a-color='price']",
                ".a-color-price",
                ".a-price .a-offscreen"
            ]
            
            for selector in price_selectors:
                try:
                    price_element = await item_locator.query_selector(selector)
                    if price_element:
                        price_text = await price_element.text_content()
                        if price_text:
                            price = self._parse_price(price_text)
                            if price > 0:
                                item_info['price'] = price
                                break
                except:
                    continue
            
            # Extract quantity (simplified)
            item_info['quantity'] = 1  # Default to 1 for simplicity
            
            # Set defaults
            if 'name' not in item_info:
                item_info['name'] = "Unknown Item"
            if 'price' not in item_info:
                item_info['price'] = 0.0
                
        except Exception as e:
            print(f"Error extracting item: {e}")
        
        return item_info if item_info.get('name') else None
    
    async def _extract_totals(self, page: PlaywrightPage, cart_info: Dict[str, Any]):
        """Extract cart totals"""
        total_selectors = [
            "#sc-subtotal-amount-activecart",
            "#sc-subtotal-amount-buybox",
            ".sc-price-container",
            "[data-testid='cart-subtotal']",
            ".a-size-medium.a-color-price",
            "#sc-subtotal-amount-buybox .a-price .a-offscreen",
            ".sc-subtotal .a-price .a-offscreen"
        ]
        
        for selector in total_selectors:
            try:
                total_element = await page.query_selector(selector)
                if total_element:
                    total_text = await total_element.text_content()
                    if total_text:
                        total = self._parse_price(total_text)
                        if total > 0:
                            cart_info['total'] = total
                            cart_info['subtotal'] = total
                            print(f"Found cart total: ${total:.2f} (selector: {selector})")
                            return
            except Exception as e:
                continue
        
        # If no total found, sum up individual items
        if cart_info['total'] == 0.0 and cart_info['items']:
            total = sum(item.get('price', 0.0) * item.get('quantity', 1) for item in cart_info['items'])
            cart_info['total'] = total
            cart_info['subtotal'] = total
            print(f"Calculated total from items: ${total:.2f}")
    
    def _parse_price(self, price_text: str) -> float:
        """Parse price from text"""
        if not price_text:
            return 0.0
        
        # Remove currency symbols and extract numbers
        price_text = re.sub(r'[^\d.,]', '', price_text.strip())
        
        # Handle different decimal formats
        if ',' in price_text and '.' in price_text:
            # Format like 1,234.56
            if price_text.rindex(',') < price_text.rindex('.'):
                price_text = price_text.replace(',', '')
            else:
                # Format like 1.234,56
                price_text = price_text.replace('.', '').replace(',', '.')
        elif ',' in price_text:
            # Could be 1,234 or 12,34
            if len(price_text.split(',')[1]) == 2:
                price_text = price_text.replace(',', '.')
            else:
                price_text = price_text.replace(',', '')
        
        try:
            return float(price_text)
        except (ValueError, TypeError):
            return 0.0