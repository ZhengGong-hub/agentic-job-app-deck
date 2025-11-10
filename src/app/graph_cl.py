"""LangGraph wiring for the cover letter pipeline."""
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from domain.state import State
from agents import jd_parser, cover_letter_writer, cover_letter_exporter


def create_cover_letter_graph(config: Dict[str, Any]):
    """
    Create and compile the cover letter graph.
    
    Flow:
    - parse -> write_cover_letter -> export_cover_letter
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Compiled StateGraph
    """
    graph = StateGraph(State)
    
    # Add nodes
    graph.add_node("parse", lambda state: jd_parser.run(state, config))
    graph.add_node("write_cover_letter", lambda state: cover_letter_writer.run(state, config))
    graph.add_node("export_cover_letter", lambda state: cover_letter_exporter.run(state, config))
    
    # Main flow
    graph.set_entry_point("parse")
    graph.add_edge("parse", "write_cover_letter")
    graph.add_edge("write_cover_letter", "export_cover_letter")
    graph.add_edge("export_cover_letter", END)
    
    return graph.compile()

