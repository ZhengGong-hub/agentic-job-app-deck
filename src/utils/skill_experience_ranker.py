from typing import List
import yaml
from domain.state import State, SelectedItem
from adapters.llm_openai import OpenAIClient

def rank_and_select_skill(state: State, config: dict) -> List[SelectedItem]:

    model_config = config.get("model")
    
    client = OpenAIClient(
        model_name=model_config.get("name", "gpt-4o-mini"),
        temperature=model_config.get("temperature", 0.1),
    )

    caps = config.get("caps")
    tailoring_type = config.get("tailoring_type")
    if tailoring_type == "tech":
        add_prompt = "This job description is in tech, very technical. so please prioritize the hard technical skills and experiences."
    elif tailoring_type == "business":
        add_prompt = "This job description is in business, very business-oriented. so please prioritize the soft business skills and experiences."
    else:
        add_prompt = ""

    with open(config.get("skills"), "r") as f:
        skills_contents = yaml.load(f, Loader=yaml.SafeLoader)

    system_prompt = """You are a resume writer. Your task is to see whether you need to add skills to match the JD. Return strict JSON."""

    jd_summary = state["jd_summary"]
    jd_text = f"""Company: {jd_summary['company']}
                Role: {jd_summary['role']}
                Skills: {', '.join(jd_summary['skills'])}
                Responsibilities: {', '.join(jd_summary['responsibilities'])}
                Must Haves: {', '.join(jd_summary['must_haves'])}
                Nice to Haves: {', '.join(jd_summary['nice_to_haves'])}"""

    user_prompt = f"""You are writing a resume for a given job description. Given the following job description summary and fact bank, select the items for the skills section.

                Job Description Summary:
                {jd_text}

                Skills bullet points:
                {skills_contents}

                First, keep the all categories and items of skills.
                An addition of skills in the categories is allowed and encouraged based on JD.
                Make sure the text is formatted in LaTeX.

                {add_prompt}


                Return a JSON object with this exact structure:
                {{
                    "selected": [{{"categories": "...", "text": "..."}}, {{"categories": "...", "text": "..."}}, ...],
                }}

                Return only valid JSON, no other text."""
    
    result = client.chat_completion_json(system_prompt, user_prompt)
    
    # Validate and structure the result
    selected = result.get("selected")
    return selected