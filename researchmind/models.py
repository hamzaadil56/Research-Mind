import os
import json
from pydantic import BaseModel
from openai import OpenAI
from typing import List
from functions import research_fyps, advisory_call, tools_func 

fyp_historian = [
    {
        "role": "system",
        "content": (
            "The Previous Final Year Projects Assistant is responsible for helping students and researchers locate relevant "
            "information from past final year projects (FYPs). This includes fetching related papers, projects, and case studies "
            "based on the research topic provided. The goal of the agent is to ensure that users can access relevant insights, "
            "findings, and methodologies from similar past projects to aid in their own research or project development. By "
            "leveraging existing data, the agent can streamline the research process and reduce the likelihood of redundant work, "
            "ensuring that no significant work from past projects is overlooked."
        )
    },
]
project_advisor = [
    {
        "role": "system",
        "content": (
            "The Project Advisor Agent serves as a virtual advisor, assisting researchers and students by offering suggestions "
            "for improving or expanding their current projects. The agent analyzes the research topic or project and, using the "
            "knowledge of existing work in the domain, suggests new directions, additional areas of focus, or potential improvements. "
            "Its goal is to inspire innovation and guide the researcher towards making impactful contributions, ensuring that the "
            "research or project is well-rounded, up-to-date, and positioned to address critical gaps in the field. This agent "
            "helps researchers think beyond their immediate focus and explore opportunities for growth. The model will also give "
            "estimated times for the project timeline and will develop a thorough and complete path for the given final year project "
        )
    }
]


client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-3.5-turbo",
)

# Function to interact with GPT-o1

def core_gpt_model(messages: List) -> str:
    """
    Interact with GPT model, allowing function calls.
    
    :param messages: List of messages in chat format to be passed to the model.
    :return: Processed response from the model.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4-0613",  # Supports function calling
            messages=messages,
            # functions=tools_func,  # Add the functions you want to expose
            # function_call="auto"  # Let GPT decide when to call the function
        )

        # Check if the response contains a function call
        # if response['choices'][0]['message'].get('function_call'):
        #     # Extract function arguments
        #     function_name = response['choices'][0]['message']['function_call']['name']
        #     function_args = json.loads(response['choices'][0]['message']['function_call']['arguments'])

        #     # Call the appropriate function based on function_name
        #     if function_name == "research_fyps":
        #         result = research_fyps(**function_args)
        #     elif function_name == "advisory_call":
        #         result = advisory_call(**function_args)
        #     else:
        #         result = "Function not recognized."
            
        #     return result
        
        # Return the model's response (strip any leading/trailing whitespace)
        return response['choices'][0]['message']['content'].strip()

    except Exception as e:
        return f"Error interacting with GPT model: {str(e)}"


class OldFypAgent(BaseModel):
    role: str = "Previous Final Year Projects Assistant"
    goal: str = (
        "The Previous Final Year Projects Assistant is responsible for helping students and researchers locate relevant "
        "information from past final year projects (FYPs). This includes fetching related papers, projects, and case studies "
        "based on the research topic provided. The goal of the agent is to ensure that users can access relevant insights, "
        "findings, and methodologies from similar past projects to aid in their own research or project development. By "
        "leveraging existing data, the agent can streamline the research process and reduce the likelihood of redundant work, "
        "ensuring that no significant work from past projects is overlooked."
    )

    def perform_task(self, fyp_project: str) -> str:
        # Create the user query
        user_query = {
            "role": "user",
            "content": f"Find research papers and studies on {fyp_project}. Provide relevant findings and insights."
        }
        
        # Append user query to the message list
        fyp_historian.append(user_query)
        
        # Get result from GPT model
        result = core_gpt_model(fyp_historian)
        
        # Append GPT's response as 'assistant' role in the conversation
        fyp_historian.append({"role": "assistant", "content": result})
        
        # Return the result
        return result

class ProjectAdvisorAgent(BaseModel):
    role: str = "Project Advisor"
    goal: str = (
        "The Project Advisor Agent serves as a virtual advisor, assisting researchers and students by offering suggestions "
        "for improving or expanding their current projects. The agent analyzes the research topic or project and, using the "
        "knowledge of existing work in the domain, suggests new directions, additional areas of focus, or potential improvements. "
        "Its goal is to inspire innovation and guide the researcher towards making impactful contributions, ensuring that the "
        "research or project is well-rounded, up-to-date, and positioned to address critical gaps in the field. This agent "
        "helps researchers think beyond their immediate focus and explore opportunities for growth."
    )

    def perform_task(self, fyp_project: str) -> str:
        # Create the user query
        user_query = {
            "role": "user",
            "content": f"Provide suggestions and improvements for research on {fyp_project}. Recommend new directions or areas of focus."
        }
        
        # Append user query to the message list
        fyp_historian.append(user_query)
        
        # Get result from GPT model
        result = core_gpt_model(fyp_historian)
        
        # Append GPT's response as 'assistant' role in the conversation
        fyp_historian.append({"role": "assistant", "content": result})
        
        # Return the result
        return result
