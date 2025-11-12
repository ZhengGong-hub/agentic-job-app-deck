"""JD Parser agent: Extract structured summary from JD text."""
from domain.state import State, JDSummary
from adapters.llm_openai import OpenAIClient
from infra.logging import setup_logger

logger = setup_logger(__name__)


def run(state: State, config: dict) -> State:
    """
    Parse JD text into structured summary.
    
    Args:
        state: Current state with jd_raw
        config: Configuration with model settings
        
    Returns:
        Updated state with jd_summary
    """
    logger.info("Parsing JD...")
    
    model_config = config.get("model", {})
    client = OpenAIClient(
        model_name=model_config.get("name", "gpt-4o-mini"),
        temperature=model_config.get("temperature", 0.1),
    )
    
    system_prompt = "Extract a structured summary from a short JD. Return strict JSON only."
    
    user_prompt = f"""Parse the following job description and return a JSON object with these exact fields:
        {{
        "company": "",
        "role": "",
        "skills": [],
        "responsibilities": [],
        "must_haves": [],
        "nice_to_haves": [],
        "hr": "",
        "address": "",
        "zip": "",
        "city": ""
        }}

        "hr" is the assumed Ms./Mr. (do assume the gender!) + last name of the hiring manager if available, otherwise "Hiring Manager".

        "address" is the address of the company if available, otherwise "xxxxxxx x".
        "zip" is the zip code of the company if available, otherwise "1000".
        "city" is the city of the company if available, otherwise "Zurich".

        Job Description:
        {state["jd_raw"]}

        Return only valid JSON, no other text."""
    
    result = client.chat_completion_json(system_prompt, user_prompt)
    state["jd_summary"] = JDSummary(
            company=result.get("company", ""),
            role=result.get("role", ""),
            skills=result.get("skills", []),
            responsibilities=result.get("responsibilities", []),
            must_haves=result.get("must_haves", []),
            nice_to_haves=result.get("nice_to_haves", []),
            hr=result.get("hr", "Hiring Manager"),
            address=result.get("address", "xxxxxxx x"),
            zip=result.get("zip", "1000"),
            city=result.get("city", "Zurich"),
        )
    logger.info(f"Parsed JD: {state['jd_summary']['role']} at {state['jd_summary']['company']}")
    return state

