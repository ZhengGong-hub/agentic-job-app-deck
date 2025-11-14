from typing import List
import yaml
from domain.state import State, SelectedItem
from adapters.llm_openai import OpenAIClient

def rank_and_select_work_experience(state: State, config: dict, work_name: str) -> List[SelectedItem]:

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

    with open(config.get("work_experience")[work_name], "r") as f:
        work_experience_contents = yaml.load(f, Loader=yaml.SafeLoader)

    system_prompt = """You are a resume selector. Rank and SELECT the best items per section for this JD. 
Prefer concrete metrics. Do NOT invent facts. Return strict JSON."""

    jd_summary = state["jd_summary"]
    jd_text = f"""Company: {jd_summary['company']}
                Role: {jd_summary['role']}
                Skills: {', '.join(jd_summary['skills'])}
                Responsibilities: {', '.join(jd_summary['responsibilities'])}
                Must Haves: {', '.join(jd_summary['must_haves'])}
                Nice to Haves: {', '.join(jd_summary['nice_to_haves'])}"""

    user_prompt = f"""You are writing a resume for a given job description. Given the following job description summary and fact bank, select the best items per section.

                Job Description Summary:
                {jd_text}

                Work Experience bullet points:
                {work_experience_contents}

                Please rank and rewrite (shorten, tailor, etc.) the work experience contents based on the job description summary and the work experience bullet points.
                Note that the first bullet point must describe the company.
                Do not invent facts.

                {add_prompt}

                Selection Budgets (caps): max {caps.get('experience')} items

                Return a JSON object with this exact structure:
                {{
                    "selected": [{{"id": "...", "text": "..."}}, {{"id": "...", "text": "..."}}, ...],
                }}

                Select only from the provided bank items. Do NOT exceed the caps. 
                Return only valid JSON, no other text."""
    
    result = client.chat_completion_json(system_prompt, user_prompt)
    
    # Validate and structure the result
    selected = result.get("selected")
    return selected