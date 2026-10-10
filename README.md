# Game Video Agents

A multi-agent AI system that creates a complete gaming YouTube video package from a single video topic.

## Objective

The project automates three tasks:

1. Research and write a detailed gaming video script.
2. Create three attractive YouTube thumbnail design options based on the script.
3. Review the material and select the strongest thumbnail option.

## Agents

### Video Game YouTube Scriptwriter

Researches the requested topic using a news search tool and writes a complete YouTube script in Brazilian Portuguese.

### YouTube Gaming Thumbnail Designer

Creates three distinct thumbnail design briefs. Each option describes the visual focus, colors, text, action or expression, and audience appeal.

### Video Content Reviewer

Reviews the script and thumbnail options, then generates the final Markdown package with one selected thumbnail and its justification.

## Workflow

```text
Video topic
    ↓
Scriptwriter + news search
    ↓
Detailed video script
    ↓
Thumbnail designer
    ↓
Three thumbnail options
    ↓
Reviewer
    ↓
Final video package
```

## Technologies

- Python 3.11
- CrewAI
- LangChain
- OpenAI API
- DuckDuckGo Search
- python-dotenv

## Project Structure

```text
.
├── outputs/
├── .env.example
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

## Setup

1. Create and activate a Python 3.11 virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file based on `.env.example`.
4. Add a valid OpenAI API key:

```text
OPENAI_API_KEY=your_openai_api_key
```

The OpenAI API key requires available API credits. Never commit a real key to GitHub.

## Running the Project

Run:

```bash
python main.py
```

Then provide a topic when prompted. For example:

```text
Video topic: Best games released in 2020
```

The final package is saved to:

```text
outputs/video_package.md
```

## Output

The generated Markdown file contains:

- A reviewed video title and complete script;
- Three gaming thumbnail design options;
- One selected thumbnail with a short justification.

## Notes

This project creates detailed thumbnail design briefs for production. The `outputs/` folder is ignored by Git because it contains generated content.
