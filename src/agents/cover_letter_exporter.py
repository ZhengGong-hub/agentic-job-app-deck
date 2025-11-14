"""Cover Letter Exporter agent: Render LaTeX template and write output files."""
from pathlib import Path
import json
from domain.state import State
from adapters.render_jinja import render_latex_template
from infra.logging import setup_logger
from datetime import datetime

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
    
    latex_ctx = {
        "profile": state["profile"],
        "jd_summary": state.get("jd_summary"),
        "cover_letter_content": state["cover_letter_content"],
    }
    
    # Render LaTeX template
    template_path = templating_config.get("cover_letter_template_path", "templates/cl.tex.j2")
    latex_content = render_latex_template(template_path, latex_ctx)
    
    # Write LaTeX file
    cl_filename = f"cover_letter.tex"
    cl_path = out_dir / cl_filename
    with open(cl_path, "w") as f:
        f.write(latex_content)

    # other files to export
    audit_data = {
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "jd_raw": state.get("jd_raw"),
        "jd_summary": state.get("jd_summary"),
        "cover_letter_content": state.get("cover_letter_content"),
    }
    audit_path = out_dir / "audit_cl.json"
    with open(audit_path, "w") as f:
        json.dump(audit_data, f, indent=2)   

    logger.info(f"Exported audit.json to {cl_path}")
    return state
