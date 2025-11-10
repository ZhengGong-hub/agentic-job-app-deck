"""Cover Letter Exporter agent: Render LaTeX template and write output files."""
from pathlib import Path
from domain.state import State
from adapters.render_jinja import render_latex_template
from infra.logging import setup_logger

logger = setup_logger(__name__)


def run(state: State, config: dict) -> State:
    """
    Export cover letter to LaTeX.
    
    Args:
        state: Current state with profile, jd_summary, and cover_letter_content
        config: Configuration with templating and paths
        
    Returns:
        Updated state with artifacts
    """
    logger.info("Exporting cover letter...")
    
    if not state.get("cover_letter_content"):
        logger.error("Cover letter content not available")
        return state
    
    templating_config = config.get("templating", {})
    paths_config = config.get("paths", {})
    out_dir = Path(paths_config.get("out_dir", "out"))
    out_dir.mkdir(exist_ok=True)
    
    # Build LaTeX context
    jd_summary = state.get("jd_summary", {})
    company = jd_summary.get("company", "unknown").replace(" ", "_")
    role = jd_summary.get("role", "unknown").replace(" ", "_")
    
    # Default cover letter context (can be extended later)
    cl_context = {
        "recipient": "Hiring Manager",
        "greeting": "Dear",
        "closer": "Kind Regards",
    }
    
    latex_ctx = {
        "profile": state["profile"],
        "jd_summary": jd_summary,
        "cover_letter_content": state["cover_letter_content"],
        "cl_context": cl_context,
    }
    
    # Render LaTeX template
    template_path = templating_config.get("cover_letter_template_path", "templates/cl.tex.j2")
    latex_content = render_latex_template(template_path, latex_ctx)
    
    # Write LaTeX file
    cl_filename = f"cover_letter.tex"
    cl_path = out_dir / cl_filename
    with open(cl_path, "w") as f:
        f.write(latex_content)
    
    logger.info(f"Exported cover letter to {cl_path}")
    
    state["artifacts"]["cover_letter"] = str(cl_path)
    
    return state

