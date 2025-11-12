"""YAML storage adapter."""
import yaml
from pathlib import Path
from typing import List, Dict, Any
from infra.logging import setup_logger

logger = setup_logger(__name__)

def load_profile(profile_path: str) -> Dict[str, Any]:
    """
    Load profile YAML.
    
    Args:
        profile_path: Path to profile.yaml
        
    Returns:
        Profile dictionary
    """
    with open(profile_path, "r") as f:
        return yaml.safe_load(f)


def load_bank(bank_dir: str) -> List[Dict[str, Any]]:
    """
    Load all bank YAML files.
    
    Args:
        bank_dir: Directory containing bank YAML files
        
    Returns:
        List of bank items
    """
    bank_path = Path(bank_dir)
    bank_items = []
    
    for yaml_file in bank_path.glob("*.yaml"):
        with open(yaml_file, "r") as f:
            items = yaml.safe_load(f)
            if isinstance(items, list):
                bank_items.extend(items)
    
    return bank_items


def load_jd(jd_path: str) -> str:
    """
    Load JD text file.
    
    Args:
        jd_path: Path to jd.txt
        
    Returns:
        JD text content
    """
    with open(jd_path, "r") as f:
        return f.read()


def load_cl_bank(cl_bank_dir: str) -> dict:
    """
    Load cover letter bank YAML file.
    
    Args:
        cl_bank_dir: Directory containing cl bank YAML files

    Returns:
        Dictionary containing "content" and "stumbling_block" items
    """
    
    cl_bank_path = Path(cl_bank_dir)
    content_file = cl_bank_path / "content.yaml"
    sb_file = cl_bank_path / "stumbling_block.yaml"
    
    if not content_file.exists():
        raise FileNotFoundError(f"Cover letter bank file not found: {content_file}! Please create a content.yaml file in the bank directory.")
    else:
        with open(content_file, "r") as f:
            content_items = yaml.safe_load(f)
            
    if not sb_file.exists():
        raise FileNotFoundError(f"Stumbling block bank file not found: {sb_file}! Please create a stumbling_block.yaml file in the bank directory.")
    else:
        with open(sb_file, "r") as f:
            stumbling_block_items = yaml.safe_load(f)
            
    logger.info(f"Loaded {len(content_items)} content and {len(stumbling_block_items)} stumbling block files")

    return {
        "content": content_items,
        "stumbling_block": stumbling_block_items,
    }
