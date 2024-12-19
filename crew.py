import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class ProductDesign():
	"""ProductDesign crew for IKEA innovation team pitch"""

	# Updated config paths to reflect flat structure
	agents_config = 'agents.yaml'
	tasks_config = 'tasks.yaml'

	def __init__(self):
		"""Initialize the ProductDesign crew with necessary tools"""
		self.search_tool = SerperDevTool()

	def _get_base_prompt(self, role):
		return f"""You are a {role}. Provide brief, focused analysis in bullet points.
		Keep responses concise and highlight only the most important points.
		Focus on quick, actionable insights rather than extensive details.
		
		When using tools, use this format:
		Thought: [brief thought]
		Action: [tool name]
		Action Input: [input]
		
		Final Answer format:
		- Key Point 1
		- Key Point 2
		- Key Point 3
		
		Remember:
		1. Be concise and direct
		2. Use bullet points
		3. Maximum 3-4 key points per section
		4. Focus on immediate actionable insights
		"""

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools

	@agent
	def market_analyst(self) -> Agent:
		base_prompt = self._get_base_prompt("Market Intelligence Analyst")
		return Agent(
			config=self.agents_config['market_analyst'],
			tools=[self.search_tool],
			verbose=True,
			llm_config={
				"model": "gpt-4-mini",
				"temperature": 0.5,
				"request_timeout": 60,
				"max_retries": 2,
				"system_prompt": base_prompt
			}
		)

	@agent
	def tech_specialist(self) -> Agent:
		base_prompt = self._get_base_prompt("Technology Specialist")
		return Agent(
			config=self.agents_config['tech_specialist'],
			tools=[self.search_tool],
			verbose=True,
			llm_config={
				"model": "gpt-4-mini",
				"temperature": 0.5,
				"request_timeout": 60,
				"max_retries": 2,
				"system_prompt": base_prompt
			}
		)

	@agent
	def feasibility_assessor(self) -> Agent:
		base_prompt = self._get_base_prompt("Product Feasibility Expert")
		return Agent(
			config=self.agents_config['feasibility_assessor'],
			tools=[self.search_tool],
			verbose=True,
			llm_config={
				"model": "gpt-4-mini",
				"temperature": 0.5,
				"request_timeout": 60,
				"max_retries": 2,
				"system_prompt": base_prompt
			}
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task

	@task
	def market_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['market_analysis_task'],
			description="""Provide a quick market overview with 3-4 key points about market potential and target audience.
			Important: Do not include or reference any images, graphs, or visual content from the internet.
			Focus on clear, text-based bullet points and concise analysis."""
		)

	@task
	def technical_assessment_task(self) -> Task:
		return Task(
			config=self.tasks_config['technical_assessment_task'],
			description="""List 3-4 key technical requirements and potential challenges. Keep it brief and focused.
			Important: Do not include or reference any images, graphs, or visual content from the internet.
			Present all technical information in text format using clear bullet points."""
		)

	@task
	def feasibility_evaluation_task(self) -> Task:
		return Task(
			config=self.tasks_config['feasibility_evaluation_task'],
			description="""Give a quick feasibility assessment with 3-4 main points about viability and implementation.
			Important: Do not include or reference any images, graphs, or visual content from the internet.
			Present all evaluation data in text format using clear bullet points."""
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the ProductDesign crew for IKEA innovation assessment"""
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
			planning=False,  # Disabled planning to speed up process
			max_round=2  # Reduced max rounds
		)
	def get_results(self):
		"""Get the stored results"""
		return self.results

