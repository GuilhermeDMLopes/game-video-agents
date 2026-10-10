import os
from pathlib import Path

from crewai import Agent, Crew, Process, Task
from dotenv import load_dotenv
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_openai import ChatOpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key or api_key == "Insira sua chave da OPENAI aqui":
    raise ValueError(
        "Set OPENAI_API_KEY in the .env file before running the project."
    )


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
)

game_search_tool = DuckDuckGoSearchResults(
    backend="news",
    num_results=5,
)


video_scriptwriter = Agent(
    role="Video Game YouTube Scriptwriter",
    goal=(
        "Research the video topic {query} and write a detailed, engaging "
        "YouTube video script for a gaming audience."
    ),
    backstory=(
        "You are a specialist in video game content, storytelling, and "
        "YouTube audience retention. You research reliable gaming information "
        "and transform it into entertaining Brazilian Portuguese scripts."
    ),
    verbose=True,
    llm=llm,
    max_iter=5,
    tools=[game_search_tool],
    allow_delegation=False,
    memory=True,
)

thumbnail_creator = Agent(
    role="YouTube Gaming Thumbnail Designer",
    goal=(
        "Create three visually attractive thumbnail concepts based on the "
        "video script about {query}."
    ),
    backstory=(
        "You are a graphic designer specialized in high-click-through-rate "
        "YouTube thumbnails for gaming channels. You know how to combine "
        "game characters, contrast, short text, emotion, and visual focus."
    ),
    verbose=True,
    llm=llm,
    max_iter=5,
    allow_delegation=False,
    memory=True,
)

reviewer = Agent(
    role="Video Content Reviewer",
    goal=(
        "Review the script and thumbnail concepts, then deliver the final "
        "video package with one selected thumbnail."
    ),
    backstory=(
        "You are a detail-oriented editor for a gaming YouTube channel. "
        "You improve clarity, consistency, audience appeal, and ensure the "
        "final deliverable is ready for production."
    ),
    verbose=True,
    llm=llm,
    max_iter=5,
    allow_delegation=False,
    memory=True,
)


write_script = Task(
    description=(
        "Research the topic {query} using the news search tool. "
        "Write a detailed YouTube script in Brazilian Portuguese for a "
        "complete video about this topic. Include: a strong hook, introduction, "
        "organized main sections, transitions, call to action, and conclusion. "
        "Use only information relevant to the topic and avoid invented facts."
    ),
    expected_output=(
        "A complete Markdown video script in Brazilian Portuguese with a title, "
        "hook, introduction, main sections, call to action, and conclusion."
    ),
    agent=video_scriptwriter,
)

create_thumbnails = Task(
    description=(
        "Based on the generated script about {query}, create exactly three "
        "different YouTube thumbnail options in Brazilian Portuguese. "
        "For each option, describe: main image or character, facial expression "
        "or action, background, colors, short text on the thumbnail, and why "
        "the concept is attractive to a gaming audience."
    ),
    expected_output=(
        "Three numbered and detailed thumbnail design briefs in Markdown. "
        "Each option must be visually distinct and ready to be produced by a designer."
    ),
    agent=thumbnail_creator,
    context=[write_script],
)

review_video_package = Task(
    description=(
        "Review the video script and the three thumbnail options for {query}. "
        "Improve the script only when necessary for clarity and engagement. "
        "Deliver a final Brazilian Portuguese package containing the reviewed "
        "script, all three thumbnail options, and one selected thumbnail with "
        "a short justification."
    ),
    expected_output=(
        "A complete Markdown document containing: "
        "1. Video title; "
        "2. Reviewed video script; "
        "3. Three thumbnail options; "
        "4. A section named 'Selected Thumbnail' with the chosen option and justification."
    ),
    agent=reviewer,
    context=[write_script, create_thumbnails],
)


crew = Crew(
    agents=[video_scriptwriter, thumbnail_creator, reviewer],
    tasks=[write_script, create_thumbnails, review_video_package],
    verbose=True,
    process=Process.sequential,
    full_output=True,
)


def run_video_content_crew(query: str) -> Path:
    result = crew.kickoff(inputs={"query": query})

    output_directory = Path("outputs")
    output_directory.mkdir(exist_ok=True)

    output_file = output_directory / "video_package.md"
    output_file.write_text(result.raw, encoding="utf-8")

    return output_file


if __name__ == "__main__":
    video_topic = input("Video topic: ").strip()

    if not video_topic:
        raise ValueError("The video topic cannot be empty.")

    generated_file = run_video_content_crew(video_topic)

    print(f"Video package created at: {generated_file}")
