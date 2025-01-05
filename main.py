from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    model = Groq(id="llama-3.3-70b-versatile"),
    # use latest data to get the best results
    version = "latest",
    tools = [YFinanceTools(stock_price=True, stock_fundamentals=True, analyst_recommendations=True)],
    markdown=True,
    show_tool_calls=True,
    instructions=["Use table to display the data"],
    debug_mode=False

)

# Ensure the agent is properly initialized before calling print_response
if agent:
    print(agent.print_response("analyze NVDA"))
else:
    print("Failed to initialize the agent.")
