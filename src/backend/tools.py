import os
import re
from dotenv import load_dotenv, find_dotenv
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents.react.agent import create_react_agent
from langchain.agents.agent import AgentExecutor

from prompts import PROMPT_DATE

load_dotenv(find_dotenv())
LLM_API_KEY = os.environ.get("GEMINI_API_KEY")
TODAY = datetime(2024, 11, 8)


@tool
def get_num_recent_receipts(period_and_unit: str) -> str:
    """
    Get rows (receipts) within a specified period from today as a file, return a path to the file.
    
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
    with open("../../data/test.csv", "w", encoding="utf-8") as f:
        filtered_df.to_csv(f)

    return "\nFile saved successfuly to '../../data/test.csv'\n"


def infer_llm(query):
    tools = [get_num_recent_receipts]
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        api_key=LLM_API_KEY
    )
    agent = create_react_agent(llm, tools, PROMPT_DATE)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    res = agent_executor.invoke({"input": query})
    path = re.findall(r"'(.*?)'", res["output"])
    if len(path) == 0:
        return res["output"]
    return path[0]


if __name__ == "__main__":
    output = infer_llm("Give me receipts from the past 2 months.")
    print(output)