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
def get_category_spending_breakdown(period_and_unit: str) -> str:
    """
    Provides a breakdown of total spendings by category within a specified period.
    
    Parameters:
    - period_and_unit (str): A combination of 2 values separated by comma (without a space).
        - period: The number of days, months, or years for the date filter.
        - unit: The time unit for the period, either "days", "months", or "years".
    """
    with open("../../data/Receipts.csv", "r", encoding="utf-8") as f:
        dataframe = pd.read_csv(f)
        
    period, unit = period_and_unit.split(",")
    period = int(period)
    
    if 'created_date' not in dataframe.columns or 'total_price' not in dataframe.columns or 'category' not in dataframe.columns:
        raise ValueError("DataFrame must contain 'created_date', 'amount', and 'category' columns.")
    
    # Convert the created_date column to datetime
    dataframe['created_date'] = pd.to_datetime(dataframe['created_date'])
    
    # Calculate the start date based on the specified period and unit
    if unit == "days":
        start_date = TODAY - timedelta(days=period)
    elif unit == "months":
        start_date = TODAY - relativedelta(months=period)
    elif unit == "years":
        start_date = TODAY - relativedelta(years=period)
    else:
        raise ValueError(f"Invalid unit '{unit}'. Unit must be 'days', 'months', or 'years'.")
    
    # Filter receipts by date range
    filtered_df = dataframe[(dataframe['created_date'] >= start_date) & (dataframe['created_date'] <= TODAY)]
    
    # Group by category and calculate the total spending
    category_spend = filtered_df.groupby('category')['total_price'].sum().sort_values(ascending=False)[0]
    # category_spend.to_csv("../../data/category_spend.csv")
    
    print(category_spend)

    # Format the result
    result = "\nCategory-wise Spending Breakdown:\n"
    for category, spend in category_spend.items():
        result += f"{category}: ${spend:,.2f}\n"
    
    return result


def infer_llm(query):
    tools = [get_category_spending_breakdown]
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
    output = infer_llm("Where I was spending the most from the past 2 months.")
    print(output)