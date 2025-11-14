"""Ranker agent: Select best items from bank for JD."""
from domain.state import State, SelectionResult, SelectedItem
from adapters.llm_openai import OpenAIClient
from infra.logging import setup_logger
from utils.work_experience_ranker import rank_and_select_work_experience

logger = setup_logger(__name__)


def run(state: State, config: dict) -> State:
    """
    Rank and select best items from bank per section.
    
    Args:
        state: Current state with jd_summary and bank
        config: Configuration with model settings and caps
        
    Returns:
        Updated state with selected items
    """
    logger.info("Ranking and selecting items from bank...")

    # Initialize with expected sections (empty lists)
    work_indices = config.get("work_experience").keys()

    ranked = dict.fromkeys(work_indices, [])

    #  ----- work experience contents ----- #
    for work in work_indices:
        selected = rank_and_select_work_experience(state, config, work)
        
        ranked[work] = SelectionResult(
            selected=[
                SelectedItem(id=item["id"], text=item["text"])
                for item in selected
            ]
        )
        
    logger.info(f"Ranked {len(ranked)} items")

    state["ranked"] = ranked
    return state

