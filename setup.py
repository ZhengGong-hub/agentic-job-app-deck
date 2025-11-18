#!/usr/bin/env python3
"""
Interactive setup script to create personalized bank/ and cl_bank/ directories.
This script guides you through filling out your profile, skills, experience, and more.
"""

import os
import sys
from pathlib import Path
import yaml

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{text}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'='*60}{Colors.ENDC}\n")

def print_section(text):
    print(f"\n{Colors.OKBLUE}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.OKBLUE}{'-'*len(text)}{Colors.ENDC}")

def get_input(prompt, required=True, default=None):
    """Get user input with validation."""
    while True:
        if default:
            display_prompt = f"{prompt} [{default}]: "
        else:
            display_prompt = f"{prompt}: "

        value = input(Colors.OKCYAN + display_prompt + Colors.ENDC).strip()

        if not value and default:
            return default
        elif not value and required:
            print(f"{Colors.WARNING}This field is required. Please enter a value.{Colors.ENDC}")
            continue
        else:
            return value

def get_multiline_input(prompt):
    """Get multi-line input from user."""
    print(f"{Colors.OKCYAN}{prompt}{Colors.ENDC}")
    print("(Enter text, then press Enter twice to finish)")
    lines = []
    while True:
        line = input()
        if line == "":
            if lines:
                break
        else:
            lines.append(line)
    return " ".join(lines)

def setup_profile():
    """Interactive profile setup."""
    print_section("Personal & Professional Profile")

    profile = {
        "name": get_input("Full name (e.g., John Doe, PhD)"),
        "email": get_input("Email address"),
        "phone": get_input("Phone number (with country code, e.g., +41 XXXXXXXXX)"),
        "location": get_input("Current location (e.g., Zurich, Switzerland)"),
        "linkedin": get_input("LinkedIn profile URL", required=False, default=""),
        "github": get_input("GitHub profile URL", required=False, default=""),
        "address": get_input("Full address (optional)", required=False, default=""),
    }

    # Education
    print_section("Education (most recent first)")

    edu = {}
    for edu_num in [1, 2, 3]:
        print(f"\n{Colors.BOLD}Education {edu_num}{Colors.ENDC}")
        add_edu = get_input(f"Add education entry {edu_num}? (yes/no)", required=False, default="yes")

        if add_edu.lower() in ["yes", "y"]:
            edu_key = f"edu{edu_num}"
            edu[edu_key] = {
                "name": get_input(f"  University/Institution name"),
                "time": get_input(f"  Duration (e.g., 2014 - 2016 or 2014.9 - 2016.6)"),
                "title": get_input(f"  Degree/Title (e.g., MSc in Mathematics)"),
                "city": get_input(f"  City/Location"),
            }
        else:
            continue

    profile.update(edu)

    # Work Experience
    print_section("Work Experience (most recent first)")

    work = {}
    for work_num in [1, 2, 3]:
        print(f"\n{Colors.BOLD}Work Experience {work_num}{Colors.ENDC}")
        add_work = get_input(f"Add work experience {work_num}? (yes/no)", required=False, default="yes")

        if add_work.lower() in ["yes", "y"]:
            work_key = f"work{work_num}"
            work[work_key] = {
                "name": get_input(f"  Company name"),
                "time": get_input(f"  Duration (e.g., 2023.9 - Present or 2023.9 - 2024.6)"),
                "title": get_input(f"  Job title"),
                "city": get_input(f"  City/Location"),
            }
        else:
            continue

    profile.update(work)
    return profile

def setup_skills():
    """Interactive skills setup."""
    print_section("Skills & Expertise")
    print("Add skill categories. Each category can have multiple skills.")

    skills = []
    skill_num = 1

    while True:
        print(f"\n{Colors.BOLD}Skill Category {skill_num}{Colors.ENDC}")
        add_skill = get_input(f"Add skill category {skill_num}? (yes/no)", required=False, default="yes" if skill_num == 1 else "no")

        if add_skill.lower() in ["yes", "y"]:
            skill_text = get_input(f"  Skills/Tools (comma-separated, e.g., Python, C++, Docker)")
            skill_category = get_input(f"  Category name (e.g., Programming Languages)")
            skill_tags = get_input(f"  Tags (comma-separated, e.g., programming, web, devops)")

            skills.append({
                "id": f"skill_{skill_num}",
                "text": skill_text,
                "category": skill_category,
                "tags": [tag.strip() for tag in skill_tags.split(",")]
            })
            skill_num += 1
        else:
            break

    return skills

def setup_achievements():
    """Interactive achievements setup."""
    print_section("Achievements & Recognitions")
    print("List your major accomplishments, awards, and recognitions.")

    achievements = []
    ach_num = 1

    while True:
        print(f"\n{Colors.BOLD}Achievement {ach_num}{Colors.ENDC}")
        add_ach = get_input(f"Add achievement {ach_num}? (yes/no)", required=False, default="yes" if ach_num <= 3 else "no")

        if add_ach.lower() in ["yes", "y"]:
            ach_text = get_multiline_input(f"  Describe achievement {ach_num}")
            ach_tags = get_input(f"  Tags (comma-separated, e.g., award, research, competition)")
            ach_priority = get_input(f"  Priority/importance (0.0-1.0, e.g., 0.85)", default="0.8")

            try:
                priority = float(ach_priority)
            except ValueError:
                priority = 0.8

            achievements.append({
                "id": f"ach_{ach_num}",
                "section": "Achievements",
                "text": ach_text,
                "tags": [tag.strip() for tag in ach_tags.split(",")],
                "priority": priority
            })
            ach_num += 1
        else:
            break

    return achievements

def setup_projects():
    """Interactive projects setup."""
    print_section("Projects & Portfolio")
    print("Describe your personal and professional projects.")

    projects = []
    proj_num = 1

    while True:
        print(f"\n{Colors.BOLD}Project {proj_num}{Colors.ENDC}")
        add_proj = get_input(f"Add project {proj_num}? (yes/no)", required=False, default="yes" if proj_num <= 3 else "no")

        if add_proj.lower() in ["yes", "y"]:
            proj_text = get_multiline_input(f"  Describe project {proj_num} (include technologies and impact)")
            proj_tags = get_input(f"  Tags (comma-separated, e.g., python, web, ml)")
            proj_priority = get_input(f"  Priority/relevance (0.0-1.0, e.g., 0.85)", default="0.8")

            try:
                priority = float(proj_priority)
            except ValueError:
                priority = 0.8

            projects.append({
                "id": f"proj_{proj_num}",
                "section": "Projects",
                "text": proj_text,
                "tags": [tag.strip() for tag in proj_tags.split(",")],
                "priority": priority
            })
            proj_num += 1
        else:
            break

    return projects

def setup_work_experience_details():
    """Interactive work experience details setup."""
    print_section("Work Experience Details")

    work_details = {}

    for work_num in [1, 2]:
        print(f"\n{Colors.BOLD}Work Experience {work_num} - Detailed Description{Colors.ENDC}")
        add_details = get_input(f"Add details for work {work_num}? (yes/no)", required=False, default="yes" if work_num == 1 else "no")

        if add_details.lower() in ["yes", "y"]:
            print(f"  (You can add up to 5 points for this role)\n")

            entries = []
            for point_num in range(1, 6):
                add_point = get_input(f"  Add point {point_num}? (yes/no)", required=False, default="yes" if point_num <= 3 else "no")

                if add_point.lower() in ["yes", "y"]:
                    point_text = get_multiline_input(f"    Describe responsibility/achievement {point_num}")
                    point_tags = get_input(f"    Tags for this point (comma-separated)")

                    entries.append({
                        "id": f"exp_{point_num}",
                        "text": point_text,
                        "tags": [tag.strip() for tag in point_tags.split(",")]
                    })
                else:
                    break

            work_details[f"w{work_num}.yaml"] = entries

    return work_details

def setup_education_experience_details():
    """Interactive education experience details setup."""
    print_section("Education Experience Details")

    edu_details = {}

    for edu_num in [2, 3]:
        print(f"\n{Colors.BOLD}Education {edu_num} - Detailed Description{Colors.ENDC}")
        add_details = get_input(f"Add details for education {edu_num}? (yes/no)", required=False, default="yes")

        if add_details.lower() in ["yes", "y"]:
            print(f"  (Add details like thesis, awards, achievements)\n")

            entries = []
            for point_num in range(1, 4):
                add_point = get_input(f"  Add detail {point_num}? (yes/no)", required=False, default="yes" if point_num <= 2 else "no")

                if add_point.lower() in ["yes", "y"]:
                    point_text = get_multiline_input(f"    Describe detail {point_num}")

                    entries.append({
                        "id": f"exp_{point_num}",
                        "text": point_text,
                    })
                else:
                    break

            edu_details[f"e{edu_num}.yaml"] = entries

    return edu_details

def setup_cover_letter_content():
    """Interactive cover letter content setup."""
    print_section("Cover Letter - Content & Narratives")
    print("Create narrative elements that will be used in your cover letters.")

    content = []
    narratives = [
        ("Background and motivation", "Tell your professional journey and what drives you"),
        ("Bridge-building narrative", "How you connect different disciplines or experiences"),
        ("Philosophy on your field", "Your perspective on what matters in your work"),
        ("Experience and impact", "Concrete examples of your accomplishments"),
        ("Work approach philosophy", "How you approach problems and your values"),
    ]

    for idx, (label, hint) in enumerate(narratives, 1):
        print(f"\n{Colors.BOLD}Narrative {idx}: {label}{Colors.ENDC}")
        print(f"  ({hint})")

        include = get_input(f"Include this narrative? (yes/no)", required=False, default="yes")

        if include.lower() in ["yes", "y"]:
            text = get_multiline_input(f"  Write your narrative for '{label}'")

            content.append({
                "id": f"cl_{idx}",
                "text": text,
                "tags": [label.replace(" ", "-").lower()]
            })

    return content

def setup_stumbling_blocks():
    """Interactive stumbling blocks setup."""
    print_section("Cover Letter - Potential Concerns")
    print("Identify and address potential concerns a recruiter might have about your background.")

    stumbling_blocks = []

    concern_num = 1
    while True:
        print(f"\n{Colors.BOLD}Concern {concern_num}{Colors.ENDC}")
        add_concern = get_input(f"Add potential concern {concern_num}? (yes/no)", required=False, default="yes" if concern_num <= 3 else "no")

        if add_concern.lower() in ["yes", "y"]:
            concern = get_input(f"  What might a recruiter be concerned about?")
            context = get_multiline_input(f"  How does your background address this concern?")
            tags = get_input(f"  Category/tag for this concern (e.g., career-gap, overqualification)")

            stumbling_blocks.append({
                "id": f"sb_{concern_num}",
                "text": f"Potential concern: {concern} — {context}",
                "tags": [tag.strip() for tag in tags.split(",")]
            })
            concern_num += 1
        else:
            break

    return stumbling_blocks

def save_yaml_file(path, data):
    """Save data to YAML file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    print(f"{Colors.OKGREEN}✓ Created {path}{Colors.ENDC}")

def check_existing_dirs():
    """Check if bank/ or cl_bank/ directories already exist."""
    bank_exists = Path("bank").exists()
    cl_bank_exists = Path("cl_bank").exists()

    if bank_exists or cl_bank_exists:
        print(f"{Colors.WARNING}Warning: Personal directories already exist!{Colors.ENDC}")
        if bank_exists:
            print(f"  - {Colors.FAIL}bank/{Colors.ENDC} (found)")
        if cl_bank_exists:
            print(f"  - {Colors.FAIL}cl_bank/{Colors.ENDC} (found)")

        print(f"\n{Colors.WARNING}This script will NOT overwrite existing directories.{Colors.ENDC}")
        print("If you want to restart, please backup and delete these directories first.")
        proceed = get_input("Continue anyway?", required=False, default="no")

        if proceed.lower() not in ["yes", "y"]:
            print(f"{Colors.OKGREEN}Setup cancelled.{Colors.ENDC}")
            sys.exit(0)

def main():
    """Main setup flow."""
    print_header("Welcome to Agentic Job Application Deck Setup")

    print("This interactive setup will help you create your personal profile,")
    print("skills, experience, and cover letter content.\n")
    print("All information will be saved to:")
    print(f"  {Colors.OKCYAN}bank/{Colors.ENDC} (your personal/professional info)")
    print(f"  {Colors.OKCYAN}cl_bank/{Colors.ENDC} (cover letter content)\n")

    # Check for existing directories
    check_existing_dirs()

    # Collect all data
    print_header("Step 1: Personal & Professional Profile")
    profile = setup_profile()

    print_header("Step 2: Skills & Expertise")
    skills = setup_skills()

    print_header("Step 3: Achievements & Recognitions")
    achievements = setup_achievements()

    print_header("Step 4: Projects & Portfolio")
    projects = setup_projects()

    print_header("Step 5: Work Experience - Detailed")
    work_details = setup_work_experience_details()

    print_header("Step 6: Education - Detailed")
    edu_details = setup_education_experience_details()

    print_header("Step 7: Cover Letter - Narratives")
    cl_content = setup_cover_letter_content()

    print_header("Step 8: Cover Letter - Address Concerns")
    cl_stumbling_blocks = setup_stumbling_blocks()

    # Save all files
    print_header("Saving Your Data")

    # Create bank/ directory
    bank_dir = Path("bank")
    if bank_dir.exists():
        print(f"{Colors.WARNING}bank/ directory already exists, skipping...{Colors.ENDC}")
    else:
        bank_dir.mkdir(parents=True, exist_ok=True)
        save_yaml_file(bank_dir / "profile.yaml", profile)
        save_yaml_file(bank_dir / "skills.yaml", skills)
        save_yaml_file(bank_dir / "achievements.yaml", achievements)
        save_yaml_file(bank_dir / "projects.yaml", projects)

        # Work experience details
        (bank_dir / "work_experience_contents").mkdir(exist_ok=True)
        for filename, data in work_details.items():
            save_yaml_file(bank_dir / "work_experience_contents" / filename, data)

        # Education details
        (bank_dir / "edu_experience_contents").mkdir(exist_ok=True)
        for filename, data in edu_details.items():
            save_yaml_file(bank_dir / "edu_experience_contents" / filename, data)

    # Create cl_bank/ directory
    cl_bank_dir = Path("cl_bank")
    if cl_bank_dir.exists():
        print(f"{Colors.WARNING}cl_bank/ directory already exists, skipping...{Colors.ENDC}")
    else:
        cl_bank_dir.mkdir(parents=True, exist_ok=True)
        save_yaml_file(cl_bank_dir / "content.yaml", cl_content)
        save_yaml_file(cl_bank_dir / "stumbling_block.yaml", cl_stumbling_blocks)

    # Final message
    print_header("Setup Complete!")
    print(f"{Colors.OKGREEN}✓ Your personal data has been saved to bank/ and cl_bank/{Colors.ENDC}\n")
    print("You can now generate your CV and cover letters with:")
    print(f"  {Colors.OKCYAN}python -m uv run src/run.py -cv{Colors.ENDC}   (Generate CV)")
    print(f"  {Colors.OKCYAN}python -m uv run src/run.py -cl{Colors.ENDC}   (Generate Cover Letter)\n")
    print("These directories are in .gitignore and won't be committed to version control.")

if __name__ == "__main__":
    main()
