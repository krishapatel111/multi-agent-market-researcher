import os
from crewai import Agent, Task, Crew, LLM

#1. Load the secret GITHUB_TOKEN from your hidden .env file
# (we need a small extra package to read .env files easily in standard python)
from dotenv import load_dotenv
load_dotenv()

#2. Configure our free AI "Brain" targetting Meta's Llama 3 via Github Models
free_llm = LLM(
    model="github/meta-llama-3-70b-instruct",
    api_key=os.environ.get("GITHUB_TOKEN"),
    base_url="https://azure.com",
    temperature = 0.7
)

# Agent 1: The Researcher

researcher = Agent(
    role="Market Research Specialist",
    goal="gather raw facts, current statistics, and ket trends about the assigned topic.",
    backstory="You are an expert data detective. you excel at filtering through noise to find hard evidence, numbers, and reliable updates.",
    verbose= True,
    llm=free_llm
)

analyst = Agent(
    role="Business Data Analyst",
    goal="Filter out useless noise from raw research data and identify key market drivers, challenges, and insights.",
    backstory="You are a sharp business strategist. You don't care about generic fluff; you care about patterns, risks, and strategic opportunities hidden inside raw text.",
    verbose=True,
    llm=free_llm
)

# Agent 3: The Report Writer
writer = Agent(
    role="Professional Report Writer",
    goal="Compile analytical insights into a structured, executive-ready Markdown report.",
    backstory="You are a seasoned corporate communications expert. You know exactly how to use layout, bold text, and clear sections to make dense facts easy and engaging for busy leaders to read.",
    verbose=True,
    llm=free_llm
)

# 1. Define the topic yu want to investigate
research_topic = "The integration off AI agents in enterprise software development by 2026"

# 2. Assignment for the researcher
task_research = Task(
    description = f"Gather detailed current trends, statistics, and challenges regarding: {research_topic}.",
    expected_output="A comprehensive list of raw notes, data points, and facts about the topic.",
    agent = researcher

)

# 3. Assignment for the Analyst
task_analysis = Task(
    description = "Review the raw data provided by the research task. Identify the top 3 drivers, top 3 inhibitors, and summarize the busineed imapact.",
    expected_output = "A structured summary breaking down drivers, inhibitors, and overall business impacts. ",
    agent = analyst
)

task_write_report = Task(
    description = "Take the structured anallysis and format it into a professional market research report using clean markdown syntax.",
    expected_output = "A beatifully formatted final report in markdown format.",
    agent=writer,
    output_file="market_research_report.md" # CrewAI will auto-save this file to your directory!



)

software_crew = Crew(
    agents= [researcher, analyst, writer],
    tasks=[task_research, task_analysis, task_write_report],
    verbose=True # this llets you watch their interbal logs in your console!
)

# 6. Kickoff the execution
print("\n Starting the Multi-Agent Research Process...\n")
software_crew.kickoff()
print("\n process complete! Check ypur project folder for 'market_research_report.md'")










