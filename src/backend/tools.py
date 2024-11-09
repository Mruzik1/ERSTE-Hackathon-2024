import os
import re
from dotenv import load_dotenv, find_dotenv
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt

from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from langchain_openai import ChatOpenAI
from langchain.agents.react.agent import create_react_agent
from langchain.agents.agent import AgentExecutor
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.memory import ConversationBufferWindowMemory
from langchain.agents import load_agent, AgentType, initialize_agent, Tool, AgentExecutor, create_react_agent

from prompts import PROMPT_DATE

import numpy as np

load_dotenv(find_dotenv())
LLM_API_KEY = os.environ.get("GEMINI_API_KEY")
TODAY = datetime(2024, 11, 8)


# def save_output(output: str):
#     with open("output.txt", "w") as f:
        


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


@tool
def get_max_category_spending(period_and_unit: str) -> str:
    """
    Provides a category with the maximum total spending within a specified period.
    
    Parameters:
    - period_and_unit (str): A combination of 2 values separated by comma (without a space).
        - period: The number of days, months, or years for the date filter.
        - unit: The time unit for the period, either "days", "months", or "years".
    """
    with open("../../data/Receipts.csv", "r", encoding="utf-8") as f:
        dataframe = pd.read_csv(f)
        
    period, unit = period_and_unit.split(",")
    period = int(period)
    
    if 'created_date' not in dataframe.columns or \
       'total_price' not in dataframe.columns or \
       'category' not in dataframe.columns:
        raise ValueError("DataFrame must contain 'created_date', 'total_price', and 'category' columns.")
    
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
    categories_spend = filtered_df.groupby('category')['total_price'].sum().sort_values(ascending=False).items()
    category_spend = [c[0] for c in categories_spend][0]

    # Format the result
    result = f"\nThe most spent in category {category_spend}\n"
    return result


@tool
def visualize_top_5(period_and_unit: str) -> str:
    """
    Visualize top 5 category with the maximum total spending within a specified period from today as a file, return a path to the file.
    
    Parameters:
    - period_and_unit (str): A combination of 2 values separated by comma (without a space).
        - period: The number of days, months, or years for the date filter.
        - unit: The time unit for the period, either "days", "months", or "years".
    """
    with open("../../data/Receipts.csv", "r", encoding="utf-8") as f:
        dataframe = pd.read_csv(f)
        
    period, unit = period_and_unit.split(",")
    period = int(period)
    
    if 'created_date' not in dataframe.columns or \
       'total_price' not in dataframe.columns or \
       'category' not in dataframe.columns:
        raise ValueError("DataFrame must contain 'created_date', 'total_price', and 'category' columns.")
    
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
    top_5_categories = filtered_df.groupby('category')['total_price'].sum().sort_values(ascending=False).head(5)

    # Plotting
    plt.figure(figsize=(10, 6))
    bars = plt.bar(range(1, 6), top_5_categories.values)

    # Adding the category names to the legend
    for i, (category, value) in enumerate(top_5_categories.items(), start=1):
        plt.bar(i, value, label=f"{i}. {category}")

    plt.xlabel('Category')
    plt.ylabel('Total Spend')
    plt.title('Top 5 Spending Categories')
    plt.xticks(range(1, 6), [str(i) for i in range(1, 6)])
    plt.legend(title="Categories")
    plt.tight_layout()
    plt.savefig("../../data/top_5_categories.png")

    return "\nFile saved successfuly to '../../data/top_5_categories.png\n"
    

@tool
def get_total_spend(period_and_unit: str) -> str:
    """
    Calculates the total spend within a specified period.
    
    Parameters:
    - period_and_unit (str): A combination of 2 values separated by a comma (without a space).
        - period: The number of days, months, or years for the date filter.
        - unit: The time unit for the period, either "days", "months", or "years".
    """
    with open("../../data/Receipts.csv", "r", encoding="utf-8") as f:
        dataframe = pd.read_csv(f)
        
    period, unit = period_and_unit.split(",")
    period = int(period)
    
    if 'created_date' not in dataframe.columns or 'total_price' not in dataframe.columns:
        raise ValueError("DataFrame must contain 'created_date' and 'total_price' columns.")
    
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
    
    # Calculate the total spending
    total_spend = filtered_df['total_price'].sum()
    
    return f"Total spend in the past {period} {unit}: ${total_spend:,.2f}"


@tool
def get_average_spend(period_and_unit: str) -> str:
    """
    Calculates the average spend per receipt within a specified period.
    
    Parameters:
    - period_and_unit (str): A combination of 2 values separated by a comma (without a space).
        - period: The number of days, months, or years for the date filter.
        - unit: The time unit for the period, either "days", "months", or "years".
    """
    with open("../../data/Receipts.csv", "r", encoding="utf-8") as f:
        dataframe = pd.read_csv(f)
        
    period, unit = period_and_unit.split(",")
    period = int(period)
    
    if 'created_date' not in dataframe.columns or 'total_price' not in dataframe.columns:
        raise ValueError("DataFrame must contain 'created_date' and 'total_price' columns.")
    
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
    
    # Calculate the average spending
    if len(filtered_df) > 0:
        average_spend = filtered_df['total_price'].mean()
        return f"\nAverage spend per receipt in the past {period} {unit}: ${average_spend:,.2f}\n"
    else:
        return f"No receipts found in the past {period} {unit}."


@tool
def get_highest_transaction(period_and_unit: str) -> str:
    """
    Retrieves the highest transaction amount within a specified period.
    
    Parameters:
    - period_and_unit (str): A combination of 2 values separated by a comma (without a space).
        - period: The number of days, months, or years for the date filter.
        - unit: The time unit for the period, either "days", "months", or "years".
    """
    with open("../../data/Receipts.csv", "r", encoding="utf-8") as f:
        dataframe = pd.read_csv(f)
        
    period, unit = period_and_unit.split(",")
    period = int(period)
    
    if 'created_date' not in dataframe.columns or 'total_price' not in dataframe.columns:
        raise ValueError("DataFrame must contain 'created_date' and 'total_price' columns.")
    
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
    
    # Find the highest transaction
    if len(filtered_df) > 0:
        highest_transaction = filtered_df['total_price'].max()
        return f"\nHighest transaction in the past {period} {unit}: ${highest_transaction:,.2f}\n"
    else:
        return f"No transactions found in the past {period} {unit}."


@tool
def detect_spend_outliers(period_and_unit: str) -> str:
    """
    Detects unusually high or low transaction amounts (outliers) within a specified period.
    
    Parameters:
    - period_and_unit (str): A combination of 3 values separated by a comma (without a space).
        - period: The number of days, months, or years for the date filter.
        - unit: The time unit for the period, either "days", "months", or "years".
    """
    with open("../../data/Receipts.csv", "r", encoding="utf-8") as f:
        dataframe = pd.read_csv(f)
        
    period, unit = period_and_unit.split(",")
    period = int(period)
    
    if 'created_date' not in dataframe.columns or 'total_price' not in dataframe.columns:
        raise ValueError("DataFrame must contain 'created_date' and 'total_price' columns.")
    
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
    
    # Calculate the Z-score for the total_price column
    method = 'Z-score'
    filtered_df['z_score'] = np.abs((filtered_df['total_price'] - filtered_df['total_price'].mean()) / filtered_df['total_price'].std())
    outliers = filtered_df[filtered_df['z_score'] > 3]  # Z-score threshold (3 is commonly used for outliers)

    plt.figure(figsize=(12, 6))
    plt.scatter(filtered_df['created_date'], filtered_df['total_price'], label='Normal Transactions', color='blue', alpha=0.6)
    plt.scatter(outliers['created_date'], outliers['total_price'], label='Outliers', color='red', alpha=0.8)
    plt.xlabel('Date')
    plt.ylabel('Transaction Amount ($)')
    plt.title(f"Spending Outliers in the Past {period} {unit} (Method: {method})")
    plt.legend()
    
    # Save the plot
    plt.savefig("../../data/spending_outliers.png")
    plt.close()
    
    # Format the result
    if not outliers.empty:
        result = f"Outliers detected in the past {period} {unit}:\n"
        for _, row in outliers.iterrows():
            result += f"Date: {row['created_date'].strftime('%Y-%m-%d')}, Amount: ${row['total_price']:,.2f}, Category: {row['category']}, Recipe_ID: {row['receipt_id']}\n"
    else:
        result = f"No outliers detected in the past {period} {unit}."
    
    return result


@tool
def plot_rolling_average_spend(period_and_unit: str) -> str:
    """
    Generates a line chart showing the rolling average spend over time within a specified period.
    
    Parameters:
    - period_and_unit (str): A combination of 2 values separated by a comma (without a space).
        - period: The number of days, months, or years for the date filter.
        - unit: The time unit for the period, either "days", "months", or "years".
        - window_size : The window size for calculating the rolling average (default is 7 days).
    """
    # Load data
    with open("../../data/Receipts.csv", "r", encoding="utf-8") as f:
        dataframe = pd.read_csv(f)
        
    period, unit, window_size= period_and_unit.split(",")
    period = int(period)
    window_size = int(window_size)
    
    if 'created_date' not in dataframe.columns or 'total_price' not in dataframe.columns:
        raise ValueError("DataFrame must contain 'created_date' and 'total_price' columns.")
    
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
    
    # Sort by date for proper rolling calculation
    filtered_df = filtered_df.sort_values('created_date')
    
    # Calculate the rolling average
    filtered_df['rolling_average'] = filtered_df['total_price'].rolling(window=window_size).mean()
    
    # Plot the rolling average
    plt.figure(figsize=(12, 6))
    plt.plot(filtered_df['created_date'], filtered_df['rolling_average'], label=f'{window_size}-Day Rolling Average', color='blue')
    plt.xlabel('Date')
    plt.ylabel('Average Spend ($)')
    plt.title(f"Rolling {window_size}-Day Average Spend in the past {period} {unit}")
    plt.legend()
    plt.grid(True)
    
    # Save the plot
    plt.savefig("../../data/rolling_average_spend.png")
    plt.close()
    
    return f"\nRolling average spend chart saved to ../../data/rolling_average_spend.png.\n"


def infer_llm(query):
    tools = [
        get_num_recent_receipts,
        plot_rolling_average_spend,
        get_max_category_spending,
        visualize_top_5,
        get_total_spend,
        get_average_spend,
        get_highest_transaction,
        detect_spend_outliers
    ]
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        api_key=LLM_API_KEY,
        disable_streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()],
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_TOXICITY: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_VIOLENCE: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DEROGATORY: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        },
    )
    agent = create_react_agent(llm, tools, PROMPT_DATE)
        
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    result = agent_executor.invoke({"input": query})
    
    path = re.findall(r"'(.*?)'", result["output"])
    if len(path) == 0:
        return result["output"]
    else:
        return path[0]


if __name__ == "__main__":
    # output = infer_llm("Give me receipts from the past 2 months.")
    # output = infer_llm("Where did I spend the most of money from the past 3 months?")
    # output = infer_llm("Visualize top 5 categories from the past 2 months.")
    # output = infer_llm("What is the total spend from the past 3 months?")
    # output = infer_llm("What is the average spend from the past 2 months?")
    # output = infer_llm("What is the highest transaction from the past 3 months?")
    # output = infer_llm("Detect spend outliers from the past 2 months.")
    output = infer_llm("Plot rolling average spend from the past 1 months,7 days")
    print(output)