"""Critic agent: Check if selected content addresses JD requirements."""
from domain.state import State, CriticResult
from adapters.llm_openai import OpenAIClient
from infra.logging import setup_logger

logger = setup_logger(__name__)


def run(state: State, config: dict) -> State:
    """
    Criticize assembled content against JD requirements.
    
    Args:
        state: Current state with jd_summary and assembled lists
        config: Configuration with model settings
        
    Returns:
        Updated state with critic_result
    """
    logger.info("Criticizing assembled content...")
    
    if not state.get("jd_summary") or not state.get("assembled"):
        logger.error("JD summary or assembled content not available")
        state["critic_result"] = CriticResult(gate_passed=False, missing_topics=[])
        return state
    
    model_config = config.get("model", {})
    client = OpenAIClient(
        model_name=model_config.get("name", "gpt-4o-mini"),
        temperature=model_config.get("temperature", 0.1),
    )
    
    system_prompt = """You are a resume critic. Evaluate if the assembled resume content adequately addresses the job description requirements.
Return strict JSON only."""
    
    jd_summary = state["jd_summary"]
    jd_text = f"""Company: {jd_summary['company']}
                Role: {jd_summary['role']}
                Skills: {', '.join(jd_summary['skills'])}
                Concepts: {', '.join(jd_summary['concepts'])}
                Must Haves: {', '.join(jd_summary['must_haves'])}
                Nice to Haves: {', '.join(jd_summary['nice_to_haves'])}"""
    
    assembled_text = "Assembled Content:\n"
    for section, items in state["assembled"].items():
        assembled_text += f"\n{section}:\n"
        for item in items:
            assembled_text += f"- {item}\n"
    
    user_prompt = f"""Job Description Summary:
            {jd_text}

            {assembled_text}

            Evaluate if the assembled content addresses the JD requirements. List any missing JD topics not covered by the assembled content.

            If acceptable, return: {{"gate_passed": true, "missing_topics": []}}
            Otherwise, return: {{"gate_passed": false, "missing_topics": ["topic1", "topic2"]}}

            Return only valid JSON, no other text."""
    
    result = client.chat_completion_json(system_prompt, user_prompt)
    state["critic_result"] = CriticResult(
        gate_passed=result.get("gate_passed", False),
        missing_topics=result.get("missing_topics", []),
    )
    logger.info(f"Critic gate passed: {state['critic_result']['gate_passed']}")
    return state

