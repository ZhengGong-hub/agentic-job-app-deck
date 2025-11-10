"""Agent registry for swapping agents later."""
# TODO: Implement agent registry pattern if needed for swapping agents
from src.agents import jd_parser, ranker, assembler, critic, exporter


# Placeholder registry - can be extended later
AGENT_REGISTRY = {
    "jd_parser": jd_parser.run,
    "ranker": ranker.run,
    "assembler": assembler.run,
    "critic": critic.run,
    "exporter": exporter.run,
}

