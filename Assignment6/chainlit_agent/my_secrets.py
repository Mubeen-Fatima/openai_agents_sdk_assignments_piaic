import os
from dotenv import load_dotenv
from rich import print

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    print(
        "[red]Error:[/red] [green]GEMINI_API_KEY[/green] is not set in the environment variables."
    )
    exit(1)

gemini_api_url = os.getenv("GEMINI_API_URL")
if not gemini_api_url:
    print(
        "[red]Error:[/red] [green]GEMINI_API_URL[/green] is not set in the environment variables."
    )
    exit(1)

gemini_api_model = os.getenv("GEMINI_API_MODEL")
if not gemini_api_model:
    print(
        "[red]Error:[/red] [green]GEMINI_API_MODEL[/green] is not set in the environment variables."
    )
    exit(1)

weather_api_url = os.getenv("WEATHER_API_URL")
if not weather_api_url:
    print(
        "[red]Error:[/red] [green]WEATHER_API_URL[/green] is not set in the environment variables."
    )
    exit(1)

weather_api_key = os.getenv("WEATHER_API_KEY")
if not weather_api_key:
    print(
        "[red]Error:[/red] [green]WEATHER_API_KEY[/green] is not set in the environment variables."
    )
    exit(1)

alpha_vantage_stock_api = os.getenv("ALPHA_VANTAGE_STOCK_API")
if not alpha_vantage_stock_api:
    print(
        "[red]Error:[/red] [green]ALPHA_VANTAGE_STOCK_API[/green] is not set in the environment variables."
    )
    exit(1)

news_api_key = os.getenv("NEWS_API_KEY")
if not news_api_key:
    print(
        "[red]Error:[/red] [green]NEWS_API_KEY[/green] is not set in the environment variables."
    )
    exit(1) 

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    print(
        "[red]Error:[/red] [green]OPENAI_API_KEY[/green] is not set in the environment variables."
    )
    exit(1)


class Secrets:
    def __init__(self):
        self.gemini_api_key = gemini_api_key
        self.gemini_api_url = gemini_api_url
        self.gemini_api_model = gemini_api_model
        self.openai_api_key = openai_api_key
        self.weather_api_key = weather_api_key
        self.weather_api_url = weather_api_url
        self.alpha_vantage_stock_api = alpha_vantage_stock_api
        self.news_api_key = news_api_key