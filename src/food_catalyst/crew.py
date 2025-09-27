import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from food_catalyst.tools import HTMLGeneratorTool

# Initialize the LLM for the entire crew
gemini_llm = LLM(
    model='gemini/gemini-2.5-flash',
    api_key=os.environ.get("GEMINI_API_KEY")
)

@CrewBase
class FoodCatalyst():
    """FoodCatalyst crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def scout(self) -> Agent:
        return Agent(
            config=self.agents_config['scout'],
            verbose=True,
            tools=[SerperDevTool(n_results=5)],
            llm=gemini_llm
        )

    @agent
    def critic(self) -> Agent:
        return Agent(
            config=self.agents_config['critic'],
            verbose=True,
            tools=[SerperDevTool(n_results=5)],
            llm=gemini_llm
        )

    @agent
    def planner(self) -> Agent:
        return Agent(
            config=self.agents_config['planner'],
            verbose=True,
            tools=[SerperDevTool(n_results=5)],
            llm=gemini_llm
        )

    @agent
    def formatter(self) -> Agent:
        return Agent(
            config=self.agents_config['formatter'],
            verbose=True,
            tools=[HTMLGeneratorTool()],
            llm=gemini_llm
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
        )

    @task
    def analyze_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_task'],
        )

    @task
    def planning_task(self) -> Task:
        return Task(
            config=self.tasks_config['planning_task'],
        )

    @task
    def formatting_task(self) -> Task:
        return Task(
            config=self.tasks_config['formatting_task'],
            output_file='report.html',
        )

    @crew
    def crew(self) -> Crew:
        """Creates the FoodCatalyst crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            llm=gemini_llm, # Assign the LLM to the crew
        )
