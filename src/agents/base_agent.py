from abc import ABC, abstractmethod
from typing import Dict, Any
from ..core.models import TaskResult
from ..utils.logger import logger

class BaseAgent(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logger
    
    @abstractmethod
    async def start(self):
        """Initialize the agent"""
        pass
    
    @abstractmethod
    async def close(self):
        """Clean up the agent"""
        pass
    
    @abstractmethod
    async def execute_task(self, goal: str) -> TaskResult:
        """Execute a task based on the goal"""
        pass
    
    def log_task_start(self, goal: str):
        """Log task start"""
        self.logger.info(f"Starting task: {goal.strip()}")
    
    def log_task_complete(self, success: bool):
        """Log task completion"""
        if success:
            self.logger.info("Task completed successfully")
        else:
            self.logger.error("Task failed")