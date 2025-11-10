"""Assembler agent: Build final section lists from selected IDs."""
from domain.state import State
from infra.logging import setup_logger

logger = setup_logger(__name__)


def run(state: State, config: dict) -> State:
    """
    Assemble final section lists from selected item IDs.
    
    Args:
        state: Current state with selected items and bank
        config: Configuration with caps
        
    Returns:
        Updated state with assembled lists
    """
    logger.info("Assembling final sections...")
    
    caps = config.get("caps", {})
    bank_dict = {item["id"]: item for item in state["bank"]}
    
    # Initialize with expected sections (empty lists)
    assembled = {
        "Experience": [],
        "Projects": [],
        "Skills": [],
        "Achievements": [],
    }
    
    if not state.get("selected"):
        logger.error("Selected items not available")
        state["assembled"] = assembled
        return state
    
    selected = state["selected"].get("selected", {})
    
    for section, selected_items in selected.items():
        section_items = []
        cap = caps.get(section.lower(), float("inf"))
        
        for selected_item in selected_items[:cap]:  # Enforce cap
            item_id = selected_item["id"]
            if item_id in bank_dict:
                section_items.append(bank_dict[item_id]["text"])
            else:
                logger.warning(f"Selected item ID {item_id} not found in bank")
        
        assembled[section] = section_items
        logger.info(f"Assembled {len(section_items)} items for {section}")
    
    state["assembled"] = assembled
    return state

