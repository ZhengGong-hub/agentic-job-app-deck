"""LangGraph wiring for the CV tailoring pipeline."""
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from domain.state import State
from agents import jd_parser, ranker, assembler, critic, exporter


def create_graph(config: Dict[str, Any]):
    """
    Create and compile the CV tailoring graph.
    
    Flow:
    - parse -> rank -> assemble -> critic -> export
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Compiled StateGraph
    """
    graph = StateGraph(State)
    
    # Add nodes
    graph.add_node("parse", lambda state: jd_parser.run(state, config))
    graph.add_node("rank", lambda state: ranker.run(state, config))
    graph.add_node("assemble", lambda state: assembler.run(state, config))
    # graph.add_node("critic", lambda state: critic.run(state, config))
    graph.add_node("export", lambda state: exporter.run(state, config))
    
    # Main flow
    graph.set_entry_point("parse")
    graph.add_edge("parse", "rank")
    graph.add_edge("rank", "assemble")
    graph.add_edge("assemble", "export")
    graph.add_edge("export", END)
    
    return graph.compile()
