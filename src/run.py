"""Main entry point for CV tailoring pipeline."""
import sys
import argparse
from infra.config import load_config
from infra.logging import setup_logger
from adapters.storage_yaml import load_profile, load_bank, load_jd, load_cl_bank
from domain.state import State
from app.graph import create_graph
from app.graph_cl import create_cover_letter_graph
import yaml
import uuid
from pathlib import Path
from datetime import datetime

logger = setup_logger(__name__)


def main():
    """Main entry point."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="CV Tailoring Pipeline")
    parser.add_argument("-cl", "--cover-letter", action="store_true",
                       help="Generate cover letter instead of resume")
    args = parser.parse_args()
    
    generate_cover_letter = args.cover_letter
    
    # Load configuration
    config = load_config("config.yaml")

    # for each unique run, create a new out directory under the out directory
    out_dir = Path(config.get("paths").get("out_dir")) / str(datetime.now().strftime("%Y%m%d_%H%M%S"))
    config.get("paths")["out_dir"] = out_dir 
    out_dir.mkdir(exist_ok=True)

    logger.info("Loaded configuration")
    
    # Load data
    paths = config.get("paths")
    jd_raw = load_jd(paths.get("jd"))
    profile = load_profile(paths.get("profile"))
    bank = load_bank(paths.get("bank_dir"))

    # Load cover letter bank
    cl_bank = load_cl_bank(paths.get("cl_bank_dir"))

    # Initialize state
    state: State = {
        "jd_raw": jd_raw,
        "jd_summary": None, # will be populated by the jd_parser agent
        "bank": bank,
        "profile": profile,
        "plan": None,
        "selected": None,
        "assembled": None,
        "critic_result": None,
        "latex_ctx": None,
        "cover_letter_content": None,
        "cl_bank": cl_bank,
        "artifacts": {},
        "config": config,
        "meta": {"retry_count": 0, "errors": []},
    }
    
    if generate_cover_letter:
        logger.info("Generating cover letter...")
        
        # Compile and run cover letter graph
        logger.info("Compiling cover letter graph...")
        graph = create_cover_letter_graph(config)
        
        logger.info("Running cover letter pipeline...")
        final_state = graph.invoke(state)

        # save the final_state to a yaml file
        with open(out_dir / "final_state.yaml", "w") as f:
            yaml.dump(final_state, f)

    else:
        logger.info(f"Loaded JD, profile, and {len(bank)} bank items")
        
        # Compile and run resume graph
        logger.info("Compiling resume graph...")
        graph = create_graph(config)
        
        logger.info("Running resume pipeline...")
        final_state = graph.invoke(state)
        
        # Print results
        artifacts = final_state.get("artifacts", {})
        tex_path = artifacts.get("tex", "")
        critic_result = final_state.get("critic_result", {})
        
        if tex_path:
            logger.info(f"Exported resume to: {tex_path}")
            print(f"\n✓ Resume exported to: {tex_path}")
            print(f"Critic result: {critic_result}")
        else:
            logger.error("No artifacts produced")
            print("✗ Error: No artifacts produced")
            sys.exit(1)


if __name__ == "__main__":
    main()

