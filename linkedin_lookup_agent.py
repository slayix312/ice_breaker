import os
from dotenv import load_dotenv

load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (create_react_agent, AgentExecutor)
from langchain import hub

from tools.tools import get_profile_url_tavily


def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")

    template = """ given the full name {name_of_person} I want you to get the persons full LinkedIn url.
    Return only the url in the following format https://www.linkedin.com/in/linkedin_username
    """
    prompt_template = PromptTemplate(template = template, input_variables = ["name_of_person"])

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 LinkedIn profile page",
            func=get_profile_url_tavily,
            description="useful when you need the LinkedIn URL of a person" # Super important as this is the main determinent of if the LLM uses this tool or not. Needs to be small and concise and not ambiguous. 
        )
    ]

    react_prompt = hub.pull("hwchase17/react")        # prompt from langchain hub that is being used. 
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)  # Creates an agent that orchestrates the tools and LLM to acheive the goal.                     
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linked_profile_url = result["output"]
    return linked_profile_url

if __name__ == "__main__":
    linkedin_url = lookup("Guillermo Gaytan")
    print(linkedin_url)




