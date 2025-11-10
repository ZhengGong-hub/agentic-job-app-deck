"""Small helper functions."""
from typing import Dict, Any, List


def get_retry_count(state: Dict[str, Any]) -> int:
    """Get current retry count from state meta."""
    return state.get("meta", {}).get("retry_count", 0)


def increment_retry_count(state: Dict[str, Any]) -> Dict[str, Any]:
    """Increment retry count in state meta."""
    if "meta" not in state:
        state["meta"] = {}
    state["meta"]["retry_count"] = state["meta"].get("retry_count", 0) + 1
    return state

