from playwright.async_api import Page as PlaywrightPage
from typing import Optional
from ..utils.logger import logger
from .selectors import SelectorManager

class Navigator:
    def __init__(self, page: PlaywrightPage, selector_manager: SelectorManager = None):
        self.page = page
        self.selector_manager = selector_manager or SelectorManager()
    
    async def click_element(self, selectors: list, description: str = "element") -> bool:
        """Try to click an element using multiple selectors"""
        for selector in selectors:
            try:
                await self.page.wait_for_selector(selector, timeout=5000)
                await self.page.click(selector)
                logger.info(f"Successfully clicked {description} using selector: {selector}")
                return True
            except Exception as e:
                logger.debug(f"Failed to click {description} with selector {selector}: {e}")
                continue
        
        logger.error(f"Failed to click {description} with any selector")
        return False
    
    async def navigate_to_url(self, url: str) -> bool:
        """Navigate to a URL"""
        try:
            await self.page.goto(url)
            await self.page.wait_for_load_state('networkidle')
            logger.info(f"Successfully navigated to {url}")
            return True
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {e}")
            return False
    
    async def go_to_cart(self) -> bool:
        """Navigate to cart page"""
        logger.info("Navigating to cart...")
        
        cart_selectors = self.selector_manager.get_selectors("cart_link")
        
        if await self.click_element(cart_selectors, "cart link"):
            await self.page.wait_for_load_state('networkidle')
            return True
        
        # Fallback: direct navigation
        logger.info("Trying direct cart navigation...")
        return await self.navigate_to_url("https://amazon.com/gp/cart/view.html")