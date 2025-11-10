"""Agent Protocol interface."""
from typing import Protocol, Dict, Any
from src.domain.state import State


class AgentProtocol(Protocol):
    """Contract for all agents in the pipeline."""
    
    def run(self, state: State, config: Dict[str, Any]) -> State:
        """
        Execute the agent's logic and update state.
        
        Args:
            state: Current pipeline state
            config: Configuration dictionary
            
        Returns:
            Updated state
        """
        ...

