"""Ranker agent: Select best items from bank for JD."""
import json
from domain.state import State, SelectionResult, SelectedItem
from adapters.llm_openai import OpenAIClient
from infra.logging import setup_logger

logger = setup_logger(__name__)


def run(state: State, config: dict, missing_topics_hint: list = None) -> State:
    """
    Rank and select best items from bank per section.
    
    Args:
        state: Current state with jd_summary and bank
        config: Configuration with model settings and caps
        missing_topics_hint: Optional list of topics that must be addressed
        
    Returns:
        Updated state with selected items
    """
    logger.info("Ranking and selecting items from bank...")
    
    model_config = config.get("model", {})
    caps = config.get("caps", {})
    client = OpenAIClient(
        model_name=model_config.get("name", "gpt-4o-mini"),
        temperature=model_config.get("temperature", 0.1),
    )
    
    system_prompt = """You are a resume selector. Rank and SELECT the best items per section for this JD. 
Prefer concrete metrics. Do NOT invent facts. Return strict JSON."""
    
    # Format bank items for prompt
    bank_text = "Bank Items:\n"
    for item in state["bank"]:
        bank_text += f"- ID: {item['id']}, Section: {item['section']}, Text: {item['text']}"
        if item.get("tags"):
            bank_text += f", Tags: {', '.join(item['tags'])}"
        bank_text += "\n"

    jd_summary = state["jd_summary"]
    jd_text = f"""Company: {jd_summary['company']}
                Role: {jd_summary['role']}
                Skills: {', '.join(jd_summary['skills'])}
                Responsibilities: {', '.join(jd_summary['responsibilities'])}
                Must Haves: {', '.join(jd_summary['must_haves'])}
                Nice to Haves: {', '.join(jd_summary['nice_to_haves'])}"""
    
    if missing_topics_hint:
        jd_text += f"\n\nIMPORTANT: You must address these missing topics: {', '.join(missing_topics_hint)}"
    
    user_prompt = f"""You are writing a resume for a given job description. Given the following job description summary and fact bank, select the best items per section.

                Job Description Summary:
                {jd_text}

                {bank_text}

                Selection Budgets (caps):
                - Experience: {caps.get('experience', 6)} items
                - Projects: {caps.get('projects', 2)} items
                - Skills: {caps.get('skills', 12)} items

                Return a JSON object with this exact structure:
                {{
                "selected": {{
                    "Experience": [{{"id": "...", "reason": "..."}}],
                    "Projects": [{{"id": "...", "reason": "..."}}],
                    "Skills": [{{"id": "...", "reason": "..."}}]
                }},
                "missing_topics": ["topic1", "topic2"]
                }}

                Select only from the provided bank items. Do NOT exceed the caps. Include a reason for each selection.
                Return only valid JSON, no other text."""
    
    result = client.chat_completion_json(system_prompt, user_prompt)
    
    # Validate and structure the result
    selected = result.get("selected", {})
    state["selected"] = SelectionResult(
        selected={
            section: [
                SelectedItem(id=item["id"], reason=item.get("reason", ""))
                for item in items
            ]
            for section, items in selected.items()
        },
        missing_topics=result.get("missing_topics", []),
    )
    logger.info(f"Selected {sum(len(v) for v in state['selected']['selected'].values())} items")

    return state

