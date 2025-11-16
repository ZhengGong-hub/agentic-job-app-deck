"""Assembler agent: Build final section lists from selected IDs."""
from domain.state import State
from infra.logging import setup_logger

logger = setup_logger(__name__)


def run(state: State, config: dict) -> State:
    """
    Assemble final section lists from selected item IDs.
    
    Args:
        state: Current state with selected items and bank
        config: Configuration
        
    Returns:
        Updated state with assembled lists
    """
    logger.info("Assembling final sections...")

    work_indices = config.get("work_experience").keys()
    education_indices = config.get("edu_experience").keys()
    assembled = dict.fromkeys(list(work_indices) + list(education_indices), [])

    # work experience
    for work in work_indices:
        text = [item["text"] for item in state['ranked'][work]['selected']]
        assembled[work] = text

    # education
    for education in education_indices:
        text = [item["text"] for item in state['ranked'][education]['selected']]
        assembled[education] = text

    # skills
    # TODO: implement skills assembly

    state['assembled'] = assembled
    logger.info(f"Assembled {len(assembled)} items")

    return state
