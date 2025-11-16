"""Exporter agent: Render LaTeX template and write output files."""
import json
from pathlib import Path
from domain.state import State
from adapters.render_jinja import render_latex_template
from infra.logging import setup_logger
import os
from datetime import datetime

logger = setup_logger(__name__)


def run(state: State, config: dict) -> State:
    """
    Export resume to LaTeX and write explain.json.
    
    Args:
        state: Current state with profile, assembled lists, and all results
        config: Configuration with templating and paths
        
    Returns:
        Updated state with artifacts
    """
    logger.info("Exporting resume...")
    
    templating_config = config.get("templating")
    paths_config = config.get("paths")
    out_dir = Path(paths_config.get("out_dir", "out"))
    out_dir.mkdir(exist_ok=True)
    
    # Build LaTeX context
    jd_summary = state.get("jd_summary")
    latex_ctx = {
        "profile": state["profile"],
        "jd_summary": jd_summary,
        "selected": state["assembled"],
        "works": config.get("works"),
        "educations": config.get("educations"),
    }
    state["latex_ctx"] = latex_ctx
    
    # Render LaTeX template
    template_path = templating_config.get("cv_template_path",)
    latex_content = render_latex_template(template_path, latex_ctx)
    
    # Write LaTeX file
    tex_filename = "resume.tex"
    tex_path = out_dir / tex_filename

    os.makedirs(out_dir, exist_ok=True)
    with open(tex_path, "w") as f:
        f.write(latex_content)
    
    logger.info(f"Exported LaTeX to {tex_path}")
    
    # Write explain.json
    # other files to export
    audit_data = {
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "jd_raw": state.get("jd_raw"),
        "jd_summary": state.get("jd_summary"),
        "ranked": state.get("ranked"),
    }
    audit_path = out_dir / "audit_cv.json"
    with open(audit_path, "w") as f:
        json.dump(audit_data, f, indent=2)   

    logger.info(f"Exported audit.json to {audit_path}")
    return state

