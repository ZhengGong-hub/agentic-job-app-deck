from typing import List
import yaml
from domain.state import State, SelectedItem
from adapters.llm_openai import OpenAIClient
from infra.logging import setup_logger
logger = setup_logger(__name__)

def rank_and_select_edu_experience(state: State, config: dict, edu_name: str) -> List[SelectedItem]:

    # no LLM needed for edu experience
    try:
        with open(config.get("edu_experience")[edu_name], "r") as f:
            edu_experience_contents = yaml.load(f, Loader=yaml.SafeLoader)
    except:
        logger.info(f"Education experience contents file not found: {config.get('edu_experience')[edu_name]}")
        return []

    return edu_experience_contents