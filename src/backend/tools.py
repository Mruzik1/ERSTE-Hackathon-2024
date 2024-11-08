import os
from dotenv import load_dotenv, find_dotenv
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from langchain.tools import tool
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents.react.agent import create_react_agent
from langchain.agents.agent import AgentExecutor
from langchain.agents.react.output_parser import ReActOutputParser

from prompts import PROMPT_DATE
from parser import CustomOutputParser

load_dotenv(find_dotenv())
LLM_API_KEY = os.environ.get("GEMINI_API_KEY")
TODAY = datetime(2024, 11, 8)


@tool
def get_num_recent_receipts(period_and_unit: str) -> str:
    """
    Get a number of rows (receipts) within a specified period from today.
    
    Parameters:
    - period_and_unit (str): A combination of 2 values separated by comma (without a space).
        - period: The number of days, months, or years for the date filter.
        - unit: The time unit for the period, either "days", "months", or "years".
    """
    with open("../../data/Receipts.csv", "r", encoding="utf-8") as f:
        dataframe = pd.read_csv(f)
    period, unit = period_and_unit.split(",")
    period = int(period)

    if 'created_date' not in dataframe.columns:
        raise ValueError("DataFrame must contain a 'created_date' column.")
    dataframe['created_date'] = pd.to_datetime(dataframe['created_date'])

    if unit == "days":
        start_date = TODAY - timedelta(days=period)
    elif unit == "months":
        start_date = TODAY - relativedelta(months=period)
    elif unit == "years":
        start_date = TODAY - relativedelta(years=period)
    else:
        raise ValueError(f"Invalid unit '{unit}'. Unit must be 'days', 'months', or 'years'.")

    filtered_df = dataframe[(dataframe['created_date'] >= start_date) & (dataframe['created_date'] <= TODAY)]
    return f"\nNumber of receipts: {len(filtered_df)}\n"


if __name__ == "__main__":
    tools = [get_num_recent_receipts]
    # prompt = hub.pull("hwchase17/react")
    # llm = ChatOpenAI(
    #     base_url="http://localhost:5555/v1",
    #     temperature=0,
    #     api_key="lm-studio"
    # )
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        api_key=LLM_API_KEY
    )
    agent = create_react_agent(llm, tools, PROMPT_DATE)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    res = agent_executor.invoke({"input": "Give me receipts from the past 4 months."})
    print(res)