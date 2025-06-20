from typing import Literal
from .manual_agent import ManualBrowserAgent
from .browser_use_agent import BrowserUseAgent
from ..core.page_graph import PageGraph

AgentType = Literal["manual", "browser_use"]

class AgentFactory:
    """Factory to create different types of browser agents"""
    
    @staticmethod
    def create_agent(agent_type: AgentType, page_graph: PageGraph):
        """Create an agent of the specified type"""
        if agent_type == "manual":
            return ManualBrowserAgent(page_graph)
        elif agent_type == "browser_use":
            return BrowserUseAgent(page_graph)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")
    
    @staticmethod
    def get_available_agents() -> list[AgentType]:
        """Get list of available agent types"""
        return ["manual", "browser_use"]