"""YAML storage adapter."""
import yaml
from pathlib import Path
from typing import List, Dict, Any


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


def load_cl_bank(bank_dir: str) -> list:
    """
    Load cover letter bank YAML file.
    
    Args:
        bank_dir: Directory containing bank YAML files
        
    Returns:
        List of cover letter bank items
    """
    
    bank_path = Path(bank_dir)
    cl_file = bank_path / "cl.yaml"
    sb_file = bank_path / "stumbling_block.yaml"
    
    if not cl_file.exists():
        raise FileNotFoundError(f"Cover letter bank file not found: {cl_file}! Please create a cl.yaml file in the bank directory.")
    if not sb_file.exists():
        raise FileNotFoundError(f"Stumbling block bank file not found: {sb_file}! Please create a stumbling_block.yaml file in the bank directory.")
    
    items = []
    with open(cl_file, "r") as f:
        cl_items = yaml.safe_load(f)
        if isinstance(cl_items, list):
            items.extend(cl_items)
    with open(sb_file, "r") as f:
        sb_items = yaml.safe_load(f)
        if isinstance(sb_items, list):
            items.extend(sb_items)
    return items

