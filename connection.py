import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
from agents.run import RunConfig
import asyncio
import requests

# Load environment variables - need parentheses
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("Gemini API key is not set")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# Create agent first
agent = Agent(
    name="Math Tutor",
    instructions="You are a helpful math tutor that solve math problems",
    model=model
)

# Create RunConfig after agent
config = RunConfig(
    model=model,
    tracing_disabled=True  # model_provider is not needed here
)