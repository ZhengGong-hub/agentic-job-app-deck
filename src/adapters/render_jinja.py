"""Jinja2 template rendering."""
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from typing import Dict, Any


def render_latex_template(template_path: str, context: Dict[str, Any]) -> str:
    """
    Render LaTeX template with Jinja2.
    
    Args:
        template_path: Path to .tex.j2 template
        context: Template context dictionary
        
    Returns:
        Rendered LaTeX content as string
    """
    template_file = Path(template_path)
    env = Environment(
        loader=FileSystemLoader(template_file.parent),
        autoescape=False,
    )
    template = env.get_template(template_file.name)
    return template.render(**context)

