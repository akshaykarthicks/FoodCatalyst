from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from food_catalyst.tools import HTMLGeneratorTool


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
            tools=[SerperDevTool()]
        )

    @agent
    def critic(self) -> Agent:
        return Agent(
            config=self.agents_config['critic'],
            verbose=True,
            tools=[SerperDevTool()]
        )

    @agent
    def planner(self) -> Agent:
        return Agent(
            config=self.agents_config['planner'],
            verbose=True,
            tools=[SerperDevTool()]
        )

    @agent
    def formatter(self) -> Agent:
        return Agent(
            config=self.agents_config['formatter'],
            verbose=True,
            tools=[HTMLGeneratorTool()]
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
        )
