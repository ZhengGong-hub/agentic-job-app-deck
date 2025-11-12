"""Cover Letter Writer agent: Generate cover letter using AIDA method."""
from domain.state import State
from adapters.llm_openai import OpenAIClient
from infra.logging import setup_logger

logger = setup_logger(__name__)


def run(state: State, config: dict) -> State:
    """
    Generate cover letter using AIDA method (Attention, Interest, Desire, Action).
    
    Args:
        state: Current state with jd_summary, profile, and cl_bank
        config: Configuration with model settings
        
    Returns:
        Updated state with cover_letter_content
    """
    logger.info("Generating cover letter using AIDA method...")
    
    if not state.get("jd_summary"):
        logger.error("JD summary not available")
        return state
    
    model_config = config.get("model", {})
    client = OpenAIClient(
        model_name=model_config.get("name", "gpt-4o"),
        temperature=model_config.get("temperature", 0.1),
    )
    
    system_prompt = """You are an expert cover letter writer. Write a compelling one-page cover letter using the AIDA method:
                - Attention: Grab the reader's attention with a strong opening hook
                - Interest: Show understanding of the role and company, demonstrate genuine interest
                - Desire: Create desire by showcasing relevant skills, experience, and value proposition
                - Action: End with a clear call to action"""
    
    jd_summary = state["jd_summary"]
    profile = state["profile"]
    cl_bank = state.get("cl_bank")
    
    # Format cl_bank items
    cl_material = "\n\nPersonal material to incorporate (use these naturally in the letter):\n"
    for item in cl_bank:
        cl_material += f"- {item.get('text', '')}\n"
    
    jd_text = f"""Company: {jd_summary['company']}
                    Role: {jd_summary['role']}
                    Hiring Manager: {jd_summary['hr']}
                    Key Skills Required: {', '.join(jd_summary.get('skills', []))}
                    Must Haves: {', '.join(jd_summary.get('must_haves', []))}
                    Nice to Haves: {', '.join(jd_summary.get('nice_to_haves', []))}
                    Responsibilities: {', '.join(jd_summary.get('responsibilities', []))}"""
    
    user_prompt = f"""Write a professional cover letter (about 600 words) for the following job application using the AIDA method. 

    Four paragraphs: 1. it's about the company and the role. 2. it's about me. 3. it's about what sets me apart for the role. 4. it's about the call to action.
    
    
    Return strict JSON only with the following structure:
    {{
        "paragraph_1": "...",
        "paragraph_2": "...",
        "paragraph_3": "...",
        "paragraph_4": "..."
    }}

                Job Description Summary:
                {jd_text}

                Applicant Profile:
                Name: {profile.get('name', '')}
                Background: {profile.get('summary', '')}
                {cl_material}

                Requirements:
                1. Use AIDA structure (Attention, Interest, Desire, Action)
                3. Incorporate relevant material from the personal bank naturally
                4. Tailor content to the specific role and responsibilities of the job description.
                5. Show enthusiasm and professionalism
                6. Do not focus on the past, this cover letter focuses on the future.
                7. do story telling if possible.
                8. try to address the stumbling blocks. But: No negativity even it is to address the concerns, phrase it positively.
                9. Start with the content, not the salutation. And do not end with the closer.

                Return only valid JSON with 4 paragraphs, no other text."""
                    
    result = client.chat_completion_json(system_prompt, user_prompt)
    state["cover_letter_content"] = {
        "paragraph_1": result.get("paragraph_1", ""),
        "paragraph_2": result.get("paragraph_2", ""),
        "paragraph_3": result.get("paragraph_3", ""),
        "paragraph_4": result.get("paragraph_4", ""),
    }
    logger.info("Cover letter generated successfully")
    logger.info(f"Cover letter content: {state['cover_letter_content']}")

    return state

