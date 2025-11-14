# Agentic Job Application Deck

An LLM-powered system for generating tailored resumes and cover letters based on job descriptions.

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY=your_api_key_here
```

## Usage

Generate a resume:
```bash
uv run src/run.py -cv
```

Generate a cover letter:
```bash
uv run src/run.py -cl
```

Generate with tailoring type (tech or business):
```bash
uv run src/run.py -cv -t tech
uv run src/run.py -cv -t business
```

## Configuration

Edit `config.yaml` to configure:
- Model settings
- File paths (JD, profile, bank directories)
- Work experience sections
- Caps for experience/projects/skills

## Output

Each run creates a timestamped folder under `out/` containing:
- `resume.tex` or `cover_letter.tex` (LaTeX source)
- `final_state.yaml` (pipeline state)
- Additional artifacts (PDF, audit files, etc.)

## Project Structure

- `bank/` - Your profile, skills, experience, projects
- `cl_bank/` - Cover letter content and stumbling blocks
- `data/jd.txt` - Job description
- `config.yaml` - Configuration
- `templates/` - LaTeX templates

