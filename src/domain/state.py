"""Shared state TypedDict for the CV tailoring pipeline."""
from typing import TypedDict, List, Dict, Any, Optional


class JDSummary(TypedDict):
    """Structured JD summary."""
    company: str
    role: str
    skills: List[str]
    responsibilities: List[str]
    must_haves: List[str]
    nice_to_haves: List[str]


class BankItem(TypedDict):
    """Single item from the fact bank."""
    id: str
    section: str
    text: str
    tags: Optional[List[str]]
    priority: float


class SelectedItem(TypedDict):
    """Selected item with reasoning."""
    id: str
    reason: str


class SelectionResult(TypedDict):
    """Result from ranker agent."""
    selected: Dict[str, List[SelectedItem]]
    missing_topics: List[str]


class CriticResult(TypedDict):
    """Result from critic agent."""
    gate_passed: bool
    missing_topics: List[str]


class CoverLetterContent(TypedDict):
    """Cover letter content using AIDA method."""
    attention: str
    interest: str
    desire: str
    action: str


class State(TypedDict):
    """Main state dictionary for the pipeline."""
    jd_raw: str
    jd_summary: Optional[JDSummary]
    bank: List[BankItem]
    profile: Dict[str, Any]
    plan: Optional[Dict[str, Any]]
    selected: Optional[SelectionResult]
    assembled: Optional[Dict[str, List[str]]]
    critic_result: Optional[CriticResult]
    latex_ctx: Optional[Dict[str, Any]]
    cover_letter_content: Optional[CoverLetterContent]
    cl_bank: List[Dict[str, Any]]  # Cover letter bank items
    artifacts: Dict[str, str]  # e.g., {"tex": "path/to/file.tex", "explain": "path/to/explain.json", "cover_letter": "path/to/cover_letter.tex"}
    config: Dict[str, Any]
    meta: Dict[str, Any]  # e.g., retry_count, errors

