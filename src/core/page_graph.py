from typing import Dict, List, Optional
from .models import Page, PageElement, Action, ElementType, ActionType

class PageGraph:
    def __init__(self):
        self.pages: Dict[str, Page] = {}
        self.current_page: Optional[str] = None
    
    def add_page(self, page: Page):
        """Add a page to the graph"""
        self.pages[page.id] = page
    
    def get_page(self, page_id: str) -> Optional[Page]:
        """Get a page by ID"""
        return self.pages.get(page_id)
    
    def get_actions_from_page(self, page_id: str) -> List[Action]:
        """Get all available actions from a page"""
        page = self.get_page(page_id)
        return page.actions if page else []
    
    def find_path(self, start_page: str, target_page: str) -> List[Action]:
        """Find path between two pages using BFS"""
        if start_page == target_page:
            return []
            
        visited = set()
        queue = [(start_page, [])]
        
        while queue:
            current, path = queue.pop(0)
            if current in visited:
                continue
                
            visited.add(current)
            
            for action in self.get_actions_from_page(current):
                new_path = path + [action]
                if action.target_page == target_page:
                    return new_path
                queue.append((action.target_page, new_path))
        
        return []  # No path found

class AmazonGraphBuilder:
    @staticmethod
    def build() -> PageGraph:
        """Build Amazon-specific page graph"""
        graph = PageGraph()
        
        # Homepage
        homepage = Page(
            id="homepage",
            url="https://amazon.com",
            description="Amazon homepage",
            elements=[
                PageElement(
                    id="search_box",
                    type=ElementType.TEXTBOX,
                    selector="#twotabsearchtextbox",
                    description="Main search box",
                    fallback_selectors=["[data-cy='search-input']", ".nav-search-field input"]
                ),
                PageElement(
                    id="cart_link",
                    type=ElementType.LINK,
                    selector="#nav-cart",
                    description="Shopping cart link",
                    fallback_selectors=["#nav-cart-count-container", ".nav-cart-icon"]
                ),
            ],
            actions=[
                Action("cart_link", ActionType.CLICK, "cart_page", "Go to shopping cart"),
            ]
        )
        
        # Cart page
        cart_page = Page(
            id="cart_page",
            url="https://amazon.com/gp/cart/view.html",
            description="Shopping cart page",
            elements=[
                PageElement(
                    id="cart_items",
                    type=ElementType.TABLE,
                    selector="#sc-active-cart",
                    description="Cart items container",
                    fallback_selectors=[".sc-list-item", "[data-name='Active Items']"]
                ),
                PageElement(
                    id="checkout_btn",
                    type=ElementType.BUTTON,
                    selector="input[name='proceedToRetailCheckout']",
                    description="Proceed to checkout",
                    fallback_selectors=["#sc-buy-box-ptc-button", ".sc-proceed-to-checkout button"]
                ),
            ],
            actions=[
                Action("checkout_btn", ActionType.CLICK, "checkout_page", "Proceed to checkout"),
            ]
        )
        
        # Add pages to graph
        graph.add_page(homepage)
        graph.add_page(cart_page)
        
        return graph