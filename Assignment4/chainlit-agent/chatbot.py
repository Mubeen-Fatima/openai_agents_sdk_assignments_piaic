import chainlit as cl
from my_secrets import Secrets
from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    set_tracing_disabled,
    OpenAIChatCompletionsModel,
)
from typing import cast
from rich import print
import json


@cl.on_chat_start
async def start():
    secrets = Secrets()

    external_client = AsyncOpenAI(
        base_url=secrets.GEMINI_API_URL,
        api_key=secrets.GEMINI_API_KEY,
    )

    set_tracing_disabled(True)

    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant.",
        model=OpenAIChatCompletionsModel(
            model=secrets.GEMINI_API_MODEL,
            openai_client=external_client,
        ),
    )

    cl.user_session.set("agent", agent)

    cl.user_session.set("history", [])

    await cl.Message(
        content="Hello! I am your assistant. How can I help you today?"
    ).send()


@cl.on_message
async def main(message: cl.Message):

    msg = cl.Message(content="Thinking...")
    await msg.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))

    history = cl.user_session.get("history") or []

    history.append({"role": "user", "content": message.content})

    try:
        result = Runner.run_sync(starting_agent=agent, input=history)

        msg.content = result.final_output

        await msg.update()

        cl.user_session.set("history", result.to_input_list())

    except Exception as e:
        
        msg.content = f"An error occurred while processing your request, Please try again. \n Error:{e}"
        await msg.update()

        print(f"Error updating message: {e}")

@cl.on_chat_end
async def end():
    history = cl.user_session.get("history") or []
    
    with open("chat_history.json", "w") as f:
        json.dump(history, f, indent=4)
    