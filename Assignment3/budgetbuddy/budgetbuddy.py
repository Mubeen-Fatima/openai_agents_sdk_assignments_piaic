from agents import Agent, Runner
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# 1. Define the agent
budgetbuddy = Agent(
    name="BudgetBuddy",
    instructions="""
    You are BudgetBuddy, a friendly personal finance assistant.
    Your goal is to help users plan and track a weekly budget.
    First, ask for the user's weekly income.
    Then, ask for expense categories one by one, until the user types 'done'.
    After gathering categories and estimated amounts,
    suggest allocations using the 50/30/20 rule: 50% needs, 30% wants, 20% savings.
    Finally, summarize the plan and ask the user to enter actual spending for each category.
    Compute differences and produce a Markdown report.
    Once complete, save the report to 'output.md' in the project root.
    """
)

# 2. Run the agent synchronously
result = Runner.run_sync(budgetbuddy, "")

# 3. Write the final_output to output.md
with open("output.md", "w") as f:
    f.write(result.final_output)

print("Budget planning complete! See output.md for your report.")
