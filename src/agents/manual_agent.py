import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from typing import List, Optional
from .base_agent import BaseAgent
from ..core.models import TaskResult, CartItem
from ..core.page_graph import PageGraph
from ..extractors.cart_extractor import CartExtractor
from ..extractors.price_extractor import PriceExtractor
from config.settings import config

class ManualBrowserAgent(BaseAgent):
    def __init__(self, page_graph: PageGraph):
        # Pass the actual config dict
        super().__init__(config._config)
        self.graph = page_graph
        self.browser = None
        self.page = None
        self.playwright = None
        self.cart_extractor = None
        self.price_extractor = PriceExtractor()
        self.current_page_id = None
        self.headless = False  # Default to visible for debugging
        
    async def start(self):
        """Initialize the browser"""
        self.logger.info("Starting manual browser agent...")
        
        try:
            self.playwright = await async_playwright().start()
            
            # Launch browser with better settings
            browser_config = config.get('browser', {})
            self.browser = await self.playwright.chromium.launch(
                headless=getattr(self, 'headless', browser_config.get('headless', False)),
                slow_mo=500,  # Slow down for stability
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor'
                ]
            )
            
            # Create new page with extended timeouts
            self.page = await self.browser.new_page()
            
            # Set longer timeouts
            self.page.set_default_timeout(120000)  # 120 seconds
            self.page.set_default_navigation_timeout(120000)  # 120 seconds
            
            # Set viewport on the page
            await self.page.set_viewport_size({
                'width': browser_config.get('viewport_width', 1280),
                'height': browser_config.get('viewport_height', 720)
            })
            
            # FIXED: Correct Playwright API method name
            await self.page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            
            # FIXED: Initialize cart extractor with page parameter after page is created
            self.cart_extractor = CartExtractor(self.page)
            
            self.logger.info("Browser started successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to start browser: {e}")
            raise
        
    async def close(self):
        """Close the browser"""
        try:
            if self.page:
                await self.page.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            self.logger.info("Browser closed successfully")
        except Exception as e:
            self.logger.warning(f"Error during cleanup: {e}")
            
    def print_cart_contents(self, cart_items: list, total: float, threshold: float):
        """Print detailed cart contents to console"""
        print("\n" + "="*60)
        print(" AMAZON CART CONTENTS")
        print("="*60)
        
        if not cart_items or len(cart_items) == 0:
            print("    Cart Status: EMPTY")
            print("    Total: $0.00")
        else:
            print(f"    Items Found: {len(cart_items)}")
            print(f"    Cart Total: ${total:.2f}")
            print("\n    Items in Cart:")
            
            for i, item in enumerate(cart_items, 1):
                if isinstance(item, dict):
                    name = item.get('name', 'Unknown Item')
                    price = item.get('price', 0.0)
                    if price > 0:
                        print(f"      {i}. {name} - ${price:.2f}")
                    else:
                        print(f"      {i}. {name}")
                else:
                    print(f"      {i}. {str(item)}")
        
        print(f"\n    Price Threshold: ${threshold:.2f}")
        
        if total == 0.0:
            print(f"    Status: Cart is empty")
            print(f"    Action: Add items to cart")
        elif total < threshold:
            print(f"    Status:  BELOW THRESHOLD (${total:.2f} < ${threshold:.2f})")
            print(f"    Action:  ELIGIBLE FOR CHECKOUT")
            # print(f"   💡 Recommendation: You can proceed with purchase")
        else:
            print(f"    Status:  EXCEEDS THRESHOLD (${total:.2f} ≥ ${threshold:.2f})")
            print(f"    Action:  DO NOT CHECKOUT")
            # print(f"   💡 Recommendation: Remove items or increase threshold")
        
        print("="*60)
            
    async def execute_task(self, goal: str) -> TaskResult:
        """Execute the cart checking task - simplified for manual mode"""
        self.log_task_start(goal)
        
        try:
            threshold = self.price_extractor.extract_threshold(goal)
            
            # Step 1: Navigate to Amazon
            self.logger.info("Navigating to Amazon...")
            print("\n Navigating to Amazon.com...")
            amazon_url = config.get('amazon', {}).get('base_url', 'https://amazon.com')
            
            try:
                await self.page.goto(amazon_url, wait_until="domcontentloaded", timeout=60000)
                await asyncio.sleep(3)
                self.logger.info(f"Successfully navigated to {self.page.url}")
                print(f" Successfully loaded Amazon homepage")
                
            except Exception as e:
                print(f" Failed to navigate to Amazon: {e}")
                return TaskResult(False, f"Failed to navigate to Amazon: {e}")
            
            # Step 2: Navigate to cart
            self.logger.info("Navigating to cart...")
            print("🛒 Navigating to shopping cart...")
            
            cart_success = False
            
            # Try clicking cart icon first
            cart_selectors = [
                "#nav-cart-count-container",
                "#nav-cart", 
                ".nav-cart-icon",
                "a[href*='cart']"
            ]
            
            for selector in cart_selectors:
                try:
                    element = await self.page.wait_for_selector(selector, timeout=10000, state="visible")
                    if element:
                        await element.click()
                        self.logger.info(f"Successfully clicked cart link using selector: {selector}")
                        print(f" Found and clicked cart button")
                        cart_success = True
                        break
                except:
                    continue
            
            # If cart click failed, navigate directly to cart URL
            if not cart_success:
                print(" Cart button not found, trying direct URL...")
                try:
                    await self.page.goto("https://amazon.com/gp/cart/view.html", wait_until="domcontentloaded", timeout=60000)
                    cart_success = True
                    print(" Navigated directly to cart page")
                except Exception as e:
                    print(f" Failed to access cart: {e}")
                    return TaskResult(False, f"Failed to access cart: {e}")
            
            # Step 3: Give page time to load and check if sign-in is needed
            await asyncio.sleep(5)
            current_url = self.page.url.lower()
            
            # If on sign-in page, give user time to sign in manually
            if "signin" in current_url or "login" in current_url or "ap/signin" in current_url:
                print("\n" + "="*60)
                print(" AMAZON SIGN-IN DETECTED")
                print("="*60)
                print("Please sign in to your Amazon account in the browser window.")
                print("Take your time - the script will wait for you to complete sign-in.")
                print("Press Enter here after you've signed in and can see your cart...")
                print("="*60)
                
                # Wait for user to press Enter after signing in
                input("Press Enter after signing in and you can see your cart: ")
                
                # Give page time to load after sign-in
                await asyncio.sleep(3)
                print(" Continuing with cart analysis...")
            
            # Step 4: Extract cart information regardless of URL
            print(" Loading cart contents...")
            print(" Analyzing cart contents...")
            
            try:
                # Check if cart is empty first
                empty_cart_indicators = [
                    "Your cart is empty",
                    "Your Shopping Cart is empty",
                    "cart is empty"
                ]
                
                cart_is_empty = False
                page_content = await self.page.content()
                page_text = page_content.lower()
                
                for indicator in empty_cart_indicators:
                    if indicator.lower() in page_text:
                        cart_is_empty = True
                        break
                
                if cart_is_empty:
                    print(" Cart analysis complete!")
                    self.print_cart_contents([], 0.0, threshold)
                    
                    return TaskResult(
                        True, 
                        "Amazon cart is empty",
                        data={
                            "cart_items": [],
                            "total": 0.0,
                            "threshold": threshold,
                            "action_taken": "cart_empty",
                            "items_count": 0
                        }
                    )
                
                # Use CartExtractor to get cart info
                cart_info = await self.cart_extractor.extract_cart_info(self.page)
                
                # Extract data from cart_info
                total = cart_info.get('total', 0.0)
                items = cart_info.get('items', [])
                
                print(" Cart analysis complete!")
                
                # Convert items to simple list for printing
                item_names = []
                for item in items:
                    if isinstance(item, dict):
                        item_names.append(item.get('name', 'Unknown Item'))
                    else:
                        item_names.append(str(item))
                
                # Print detailed cart contents
                self.print_cart_contents(items, total, threshold)
                
                # Make decision based on threshold
                if total == 0.0 and len(items) == 0:
                    action_taken = "cart_empty_or_undetected"
                    message = "Cart appears empty or could not extract cart information"
                    # print(f"\n💡 Note: If you can see items in the cart but they're not detected, this may be due to Amazon's dynamic loading.")
                elif total < threshold:
                    action_taken = "eligible_for_checkout"
                    message = f"Cart total ${total:.2f} is below threshold ${threshold:.2f}. Eligible for checkout."
                    # print(f"\n💡 RECOMMENDATION: You can proceed with checkout!")
                else:
                    action_taken = "exceeds_threshold"
                    message = f"Cart total ${total:.2f} meets or exceeds threshold ${threshold:.2f}. Do not checkout."
                    # print(f"\n💡 RECOMMENDATION: Cart exceeds threshold - remove items before checkout!")
                
                return TaskResult(
                    True,
                    message,
                    data={
                        "cart_items": item_names,
                        "total": total,
                        "threshold": threshold,
                        "action_taken": action_taken,
                        "items_count": len(items)
                    }
                )
                    
            except Exception as e:
                self.logger.error(f"Error extracting cart information: {e}")
                print(f" Error analyzing cart: {e}")
                print(f" The browser window is still open - you can manually check your cart contents.")
                
                # Still return success but with manual note
                return TaskResult(
                    True,
                    f"Cart analysis had issues but browser is available for manual verification",
                    data={
                        "action_taken": "manual_verification_needed",
                        "threshold": threshold,
                        "total": 0.0,
                        "cart_items": [],
                        "note": "Check cart manually in the browser window"
                    }
                )
                
        except Exception as e:
            self.logger.error(f"Task execution failed: {e}")
            print(f" Task execution failed: {e}")
            return TaskResult(
                False,
                f"Task execution failed: {e}",
                data={
                    "action_taken": "general_error",
                    "threshold": threshold,
                    "error_type": "general",
                    "total": 0.0,
                    "cart_items": []
                }
            )