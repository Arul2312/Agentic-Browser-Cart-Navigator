from browser_use import Agent
from langchain_openai import ChatOpenAI
from ..core.models import TaskResult
from .base_agent import BaseAgent
from config.settings import config
import asyncio
import os

class BrowserUseAgent(BaseAgent):
    def __init__(self, page_graph=None):
        super().__init__(config._config)
        self.page_graph = page_graph
        self.llm = None
        
    async def start(self):
        """Initialize OpenAI GPT-4o-mini"""
        self.logger.info("Starting Browser Use agent with OpenAI GPT-4o-mini...")
        
        # Check for API key
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
        self.logger.info("Browser Use agent initialized with OpenAI GPT-4o-mini")
        
    async def close(self):
        """Close agent"""
        self.logger.info("Browser Use agent session ended")
        
    async def execute_task(self, goal=None, price_threshold=100.00):
        """Execute Amazon cart analysis and conditional checkout task"""
        self.log_task_start(f"Amazon cart analysis and conditional checkout with ${price_threshold:.2f} threshold")
        
        try:
            # Simple cart analysis and conditional checkout task
            task = f"Go to Amazon.com. Click cart. Print each item name. Only report the total cart price (not individual prices). If total is below ${price_threshold}, click checkout and stop when asked for personal info. If total is above ${price_threshold}, do not checkout."
            
            self.logger.info("Starting Amazon cart conditional checkout with OpenAI GPT-4o-mini...")
            
            agent = Agent(task=task, llm=self.llm)
            result = await agent.run()
            
            self.logger.info("Browser Use cart conditional checkout completed")
            
            # Parse result for cart contents and checkout status
            result_str = str(result).lower()
            
            # Check if checkout was initiated
            checkout_keywords = ["checkout", "sign in", "login", "personal info", "stopped", "address", "payment"]
            checkout_reached = any(keyword in result_str for keyword in checkout_keywords)
            
            # Try to extract cart value (only total, not individual prices)
            import re
            # Look for total/subtotal patterns first
            total_patterns = [
                r'total[:\s]*\$(\d+\.?\d*)',
                r'subtotal[:\s]*\$(\d+\.?\d*)',
                r'cart total[:\s]*\$(\d+\.?\d*)'
            ]
            
            cart_total = 0.0
            for pattern in total_patterns:
                matches = re.findall(pattern, str(result), re.IGNORECASE)
                if matches:
                    cart_total = max([float(amount) for amount in matches])
                    break
            
            # If no total found, look for any dollar amount (but prefer larger amounts as likely totals)
            if cart_total == 0.0:
                dollar_amounts = re.findall(r'\$(\d+\.?\d*)', str(result))
                if dollar_amounts:
                    amounts = [float(amount) for amount in dollar_amounts]
                    # Assume the largest amount is the total
                    cart_total = max(amounts)
            
            # Extract item names from result (look for item/product patterns)
            item_patterns = [
                r'item[:\s]*([^\n\r\$]+)',
                r'product[:\s]*([^\n\r\$]+)',
                r'([A-Z][^:\n\r\$]{10,50})',  # Capitalized product names
            ]
            
            cart_items = []
            for pattern in item_patterns:
                matches = re.findall(pattern, str(result), re.IGNORECASE)
                cart_items.extend([item.strip() for item in matches if len(item.strip()) > 5])
            
            # Remove duplicates while preserving order
            seen = set()
            unique_items = []
            for item in cart_items:
                if item.lower() not in seen:
                    seen.add(item.lower())
                    unique_items.append(item)
            cart_items = unique_items[:10]  # Limit to first 10 items
            
            # Determine threshold status and expected behavior
            if cart_total > price_threshold:
                threshold_status = "ABOVE_THRESHOLD"
                threshold_message = f"Cart total ${cart_total:.2f} exceeds ${price_threshold:.2f} threshold"
                should_checkout = False
            elif cart_total > 0:
                threshold_status = "BELOW_THRESHOLD" 
                threshold_message = f"Cart total ${cart_total:.2f} below ${price_threshold:.2f} threshold"
                should_checkout = True
            else:
                threshold_status = "UNKNOWN_TOTAL"
                threshold_message = "Could not determine cart total"
                should_checkout = False
            
            # Generate summary message based on threshold and checkout behavior
            if cart_total > price_threshold:
                if checkout_reached:
                    message = f"{threshold_message}. Checkout incorrectly initiated (should not have proceeded)."
                    action = "checkout_error_above_threshold"
                else:
                    message = f"{threshold_message}. Correctly did not proceed to checkout."
                    action = "no_checkout_above_threshold"
            elif cart_total > 0:
                if checkout_reached:
                    message = f"{threshold_message}. Correctly proceeded to checkout and stopped at user info."
                    action = "checkout_correct_below_threshold"
                else:
                    message = f"{threshold_message}. Should have proceeded to checkout but didn't."
                    action = "no_checkout_error_below_threshold"
            else:
                message = f"{threshold_message}. Cart analysis completed."
                action = "cart_analyzed_unknown_total"
            
            return TaskResult(
                success=True,
                message=message,
                data={
                    "result": str(result),
                    "action_taken": action,
                    "cart_total": cart_total,
                    "cart_items": cart_items,
                    "items_count": len(cart_items),
                    "threshold": price_threshold,
                    "threshold_status": threshold_status,
                    "should_checkout": should_checkout,
                    "checkout_reached": checkout_reached,
                    "behavior_correct": (should_checkout and checkout_reached) or (not should_checkout and not checkout_reached),
                    "llm_model": "gpt-4o-mini",
                    "cart_analysis": "Cart contents and total price extracted from agent response",
                    "checkout_logic": f"Only proceed to checkout if total < ${price_threshold:.2f}"
                }
            )
            
        except Exception as e:
            self.logger.error(f"Cart conditional checkout analysis failed: {e}")
            return TaskResult(
                success=False,
                message=f"Cart conditional checkout analysis failed: {str(e)}",
                data={
                    "action_taken": "error",
                    "threshold": price_threshold,
                    "error": str(e)
                }
            )

async def main():
    browser_agent = BrowserUseAgent()
    await browser_agent.start()
    result = await browser_agent.execute_task(price_threshold=100.00)
    print(result)
    await browser_agent.close()

if __name__ == "__main__":
    asyncio.run(main())