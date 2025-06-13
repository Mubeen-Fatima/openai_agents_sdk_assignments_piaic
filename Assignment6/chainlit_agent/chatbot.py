import chainlit as cl
from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
    function_tool,
)
from my_secrets import Secrets
from typing import cast
import json
from openai.types.responses import ResponseTextDeltaEvent
import requests
from rich import print

secrets = Secrets()


@function_tool("current_weather_tool")
@cl.step(type="weather tool")
async def get_current_weather(location: str) -> str:
    """
    Retrieves current weather information for a specified location.

    This function makes an asynchronous API call to fetch real-time weather data
    including temperature, weather conditions, wind speed, humidity, and UV index
    for the given location.

    Args:
        location (str): The location for which to fetch weather data. Can be a city name,
                       coordinates, or other location identifier supported by the weather API.

    Returns:
        str: A formatted string containing comprehensive weather information including:
             - Location details (name, region, country)
             - Current date and time
             - Temperature in Celsius and "feels like" temperature
             - Weather condition description
             - Wind speed (km/h) and direction
             - Humidity percentage
             - UV index

             If the API request fails, returns an error message indicating the failure.

    Raises:
        This function handles HTTP errors internally and returns error messages as strings
        rather than raising exceptions.

    Example:
        >>> weather = await get_current_weather("London")
        >>> print(weather)
        Current weather in London, England, United Kingdom as of 2023-10-15 14:30 is 18°C (Partly cloudy), feels like 17°C, wind 15 km/h SW, humidity 65% and UV index is 4.
    """
    result = requests.get(
        f"{secrets.weather_api_url}//current.json?key={secrets.weather_api_key}&q={location}"
    )
    if result.status_code != 200:
        return f"Error fetching weather data for {location}. Please try again later."
    data = result.json()
    return f"Current weather in {data['location']['name']}, {data['location']['region']}, {data['location']['country']} as of {data['location']['localtime']} is {data['current']['temp_c']}°C ({data['current']['condition']['text']}), feels like {data['current']['feelslike_c']}°C, wind {data['current']['wind_kph']} km/h {data['current']['wind_dir']}, humidity {data['current']['humidity']}% and UV index is {data['current']['uv']}."



import requests

@function_tool("stock_quote_tool")
@cl.step(type="stock quote tool")
async def get_stock_quote(symbol: str) -> str:
    """
    Retrieves current stock quote information for a specified ticker.

    This function makes an asynchronous API call to fetch real-time stock data
    including latest price, price change, change percent, and the last trading day
    for the given stock symbol.

    Args:
        symbol (str): Stock ticker symbol (e.g., "AAPL").

    Returns:
        str: A formatted string containing:
             - Symbol and last trading date
             - Current price in USD
             - Price change and percent change

             If the API request fails, returns an error message.

    Example:
        >>> quote = await get_stock_quote("AAPL")
        >>> print(quote)
        AAPL as of 2025-06-12: Price = 172.15 USD, Change = +1.23 (+0.72%).
    """
    api_key = secrets.alpha_vantage_stock_api
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": api_key
    }
    result = requests.get(url, params=params)
    if result.status_code != 200:
        return f"Error fetching data for {symbol}: HTTP {result.status_code}"

    data = result.json().get("Global Quote")
    if not data:
        return f"No data found for symbol {symbol}."

    return (f"{symbol} as of {data['07. latest trading day']}: "
            f"Price = {data['05. price']} USD, "
            f"Change = {data['09. change']} ({data['10. change percent']}).")


import requests

@function_tool("global_news_tool")
@cl.step(type="global news tool")
async def get_global_news(query: str = None) -> str:
    """
    Retrieves current global news based on a search query.

    This function makes an asynchronous API call to fetch the top news articles
    matching the given query from a global news API (e.g., NewsAPI).
    Returns a concise summary of the top News.

    Args:
        query (str): Search keyword or phrase (e.g., "climate change", "bitcoin").
        if no topic is given just return top global news available

    Returns:
        str: Formatted string containing:
             - Number of articles returned
             - Titles, sources, date and summary of contect of the top News

             If the API request fails, returns an error message.

    Example:
        >>> news = await get_global_news("bitcoin")
        >>> print(news)
        5 top news articles found for "bitcoin":
        1. Bitcoin falls below $30K – Reuters
        2. ...
    """
    api_key = secrets.news_api_key
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "q": query,
        "pageSize": 5,
        "apiKey": api_key,
        "language": "en"
    }
    result = requests.get(url, params=params)
    
    if result.status_code != 200:
        return f"Error fetching news for '{query}': HTTP {result.status_code}"

    data = result.json()
    print(data)
    if data.get("status") != "ok":
        return f"API error fetching news: {data.get('code', '')} – {data.get('message', '')}"

    articles = data.get("articles", [])
    if not articles:
        return f"No news articles found for \"{query}\"."

    response_lines = [f"{len(articles)} top news articles found for \"{query}\":"]
    for i, art in enumerate(articles, start=1):
        title = art.get("title", "No title")
        source = art.get("source", {}).get("name", "Unknown source")
        date = art.get("publishedAt", "Unknown date")
        content = art.get("content", "No content")
        response_lines.append(f"{i}.Title: {title} \n Source: {source} \n Date: {date} \n Content: {content}")

    return "\n".join(response_lines)



@function_tool("student_info_tool")
@cl.step(type="student tool")
async def get_student_info(student_id: int) -> str:
    """
    Get information about a student by their ID.
    """
    students = {
        1: {"name": "John Doe", "age": 20, "major": "Computer Science"},
        2: {"name": "Jane Smith", "age": 22, "major": "Mathematics"},
        3: {"name": "Alice Johnson", "age": 21, "major": "Physics"},
        4: {"name": "Bob Brown", "age": 23, "major": "Chemistry"},
    }
    # Simulate fetching student data
    student_info = students.get(student_id)
    if student_info:
        return f"Student ID: {student_id}, Name: {student_info['name']}, Age: {student_info['age']}, Major: {student_info['major']}."
    else:
        return f"No student found with ID {student_id}."


@cl.set_starters
async def starters():
    return [
        cl.Starter(
            label="Get Current Weather",
            message="Fetch the current weather for a specified location.",
            icon="/public/weather.svg",
        ),
        cl.Starter(
            label="Get Current Stock Quote",
            message="Fetch the current Stock Quote for a specified symbol.",
            icon="/public/stock.svg",
        ),
        cl.Starter(
            label="Get Current Global News",
            message="Fetch the current Global news for a specified topic.",
            icon="/public/news.svg",
        ),
        cl.Starter(
            label="Get Student Info",
            message="Retrieve information about a student using their ID.",
            icon="/public/student.svg",
        ),
        cl.Starter(
            label="Explore General Questions",
            message="Find answers to the given questions.",
            icon="/public/question.svg",
        ),
        cl.Starter(
            label="Write an Essay",
            message="Generate an 300 words essay on a given topic.",
            icon="/public/essay.svg",
        ),
    ]

@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(
            name="Gemini",
            markdown_description="The underlying LLM model is **Gemini**. An open source model",
            icon="https://picsum.photos/250",
            # starters=["Get Current Weather", "Get Current Stock Quote", "Get Current Global News"],
        ),
        cl.ChatProfile(
            name="GPT-4o-mini",
            markdown_description="The underlying LLM model is **GPT-4o-mini**.Balanced for intelligence, speed, and cost",
            icon="https://picsum.photos/250",
            # starters=["Get Student Info", "Explore General Questions"]
        ),
        cl.ChatProfile(
            name="o4-mini",
            markdown_description="The underlying LLM model is **GPT-4**. Faster, more affordable reasoning model",
            icon="https://picsum.photos/250",
            # starters=[ "Explore General Questions", "Write an Essay"]
        ),
    ]
@cl.on_chat_start
async def start():

    external_client = AsyncOpenAI(
        base_url=secrets.gemini_api_url,
        api_key=secrets.gemini_api_key,
    )
    set_tracing_disabled(True)

    chat_profile = cl.user_session.get("chat_profile")

    if chat_profile == "GPT-4o-mini":
        profile_model = "gpt-4o-mini"
    elif chat_profile == "o4-mini":
        profile_model = "o4-mini"
    else:
       profile_model = OpenAIChatCompletionsModel(
            openai_client=external_client,
            model=secrets.gemini_api_model,
        )

    essay_agent = Agent(
        name="Essay Writer",
        instructions="You are an expert essay writer. You can write 1000 word essays on various topics.",
        model=OpenAIChatCompletionsModel(
            openai_client=external_client,
            model=secrets.gemini_api_model,
        ),
    )

    agent = Agent(
        name="Chatbot",
        instructions=""""
        You are a friendly and informative assistant. You can answer general questions and provide specific information.
        * For **weather inquiries**, you may fetch and share the current weather.
        * For **student-related queries**, you can retrieve details using the student ID.
        * For **essay writing**, you can retrieve an essay on a given topic.
        * Use tools **only when necessary**, not by default.
        * If a question falls outside essay writing, weather or student information, provide a helpful general response or ask for clarification.
        * If you're unsure of the answer, say "I don't know" or ask for more details.
        """,
        
        model= profile_model,

        tools=[
            get_current_weather,
            get_student_info,
            get_stock_quote,
            get_global_news,
            essay_agent.as_tool(
                tool_name="essay_writer_tool",
                tool_description="Write a 300 word essay on a given topic.",
            )
        ],
    )

    cl.user_session.set("agent", agent)
    cl.user_session.set("chat_history", [])


@cl.on_message
async def main(message: cl.Message):
    thinking_msg = cl.Message(content="Thinking...")
    await thinking_msg.send()

    agent = cast(Agent, cl.user_session.get("agent"))
    chat_history: list = cl.user_session.get("chat_history") or []
    chat_history.append(
        {
            "role": "user",
            "content": message.content,
        }
    )

    try:
        result = Runner.run_streamed(
            starting_agent=agent,
            input=chat_history,
        )

        response_message = cl.Message(
            content="",
        )
        first_response = True
        async for chunk in result.stream_events():
            if chunk.type == "raw_response_event" and isinstance(
                chunk.data, ResponseTextDeltaEvent
            ):
                if first_response:
                    await thinking_msg.remove()
                    await response_message.send()
                    first_response = False
                await response_message.stream_token(chunk.data.delta)

        chat_history.append(
            {
                "role": "assistant",
                "content": response_message.content,
            }
        )
        cl.user_session.set("chat_history", chat_history)
        await response_message.update()
    except Exception as e:
        response_message.content = (
            "An error occurred while processing your request. Please try again."
        )
        await response_message.update()


@cl.on_chat_end
def end():
    chat_history: list = cl.user_session.get("chat_history") or []
    with open("chat_history.json", "w") as f:
        json.dump(chat_history, f, indent=4)