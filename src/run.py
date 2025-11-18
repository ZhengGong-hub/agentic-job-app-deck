"""Main entry point for CV tailoring pipeline."""
import sys
import argparse
from infra.config import load_config
from infra.logging import setup_logger
from adapters.storage_yaml import load_profile, load_bank, load_jd, load_cl_bank
from domain.state import State
from app.graph_cv import create_cv_graph
from app.graph_cl import create_cover_letter_graph
import yaml
from pathlib import Path
from datetime import datetime

logger = setup_logger(__name__)


def main():
    """Main entry point."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="CV Tailoring Pipeline")
    parser.add_argument("-cl", "--cover-letter", action="store_true",
                       help="Generate cover letter instead of resume")
    parser.add_argument("-cv", "--generate-cv", action="store_true",
                       help="Generate resume instead of cover letter")
    parser.add_argument("-t", "--type", choices=["tech", "business"], default="tech",
                       help="Type of tailoring: 'tech' or 'business' (default: 'tech')")
    args = parser.parse_args()

    generate_cv = args.generate_cv
    generate_cover_letter = args.cover_letter
    tailoring_type = args.type  # either 'tech' or 'business'

    # If neither option is specified, ask the user
    if not generate_cv and not generate_cover_letter:
        print("\nWhat would you like to generate?")
        print("1. CV (Resume)")
        print("2. Cover Letter")
        choice = input("Enter your choice (1 or 2): ").strip()

        if choice == "1":
            generate_cv = True
        elif choice == "2":
            generate_cover_letter = True
        else:
            print("Invalid choice. Please enter 1 or 2.")
            sys.exit(1)
    
    # Load configuration
    config = load_config("config.yaml")
    config["tailoring_type"] = tailoring_type  # Add selected type to config

    # for each unique run, create a new out directory under the out directory
    out_dir = Path(config.get("paths").get("out_dir")) / str(datetime.now().strftime("%Y%m%d_%H%M%S"))
    out_dir.mkdir(parents=True, exist_ok=True)
    config.get("paths")["out_dir"] = out_dir

    logger.info(f"Loaded configuration with type: {tailoring_type}")
    
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

    final_state = None

    if generate_cover_letter:
        logger.info("Generating cover letter...")

        # Compile and run cover letter graph
        logger.info("Compiling cover letter graph...")
        graph = create_cover_letter_graph(config)

        logger.info("Running cover letter pipeline...")
        final_state = graph.invoke(state)
        logger.info(f"Exported cover letter to: {out_dir / 'cover_letter.tex'}")

    if generate_cv:
        # Compile and run resume graph
        logger.info("Compiling resume graph...")
        graph = create_cv_graph(config)

        logger.info("Running resume pipeline...")
        final_state = graph.invoke(state)

        logger.info(f"Exported resume to: {out_dir / 'resume.tex'}")

    # save the final_state to a yaml file
    if final_state:
        with open(out_dir / "final_state.yaml", "w") as f:
            yaml.dump(final_state, f)
        logger.info(f"Saved state to: {out_dir / 'final_state.yaml'}")
    else:
        logger.error("No output generated. final_state is None.")

if __name__ == "__main__":
    main()

