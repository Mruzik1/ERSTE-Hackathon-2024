import os
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
import pandas as pd

# Initialize the OpenAI LLM
llm = OpenAI(temperature=0)

# Load transaction data globally to be used by the tools
transactions_df = pd.read_csv('transactions.csv')

# Define the tools as functions

def read_csv_tool(query: str) -> str:
    """
    Use this tool to read CSV files containing transaction data and answer questions about them.
    """
    # Implement logic to process the query and extract information from the DataFrame
    # Placeholder implementation:
    return "Here is the information you requested about your transactions."

def statistical_analysis_tool(query: str) -> str:
    """
    Use this tool to perform statistical analysis on transaction data.
    You can ask for summaries, averages, totals, maximums, minimums, counts, etc.
    """
    # Implement logic to parse the query and perform statistical analysis
    # Placeholder implementation:
    query_lower = query.lower()
    response = ""

    if 'average' in query_lower or 'mean' in query_lower:
        average_spending = transactions_df['amount'].mean()
        response = f"Your average transaction amount is {average_spending:.2f}."
    elif 'total' in query_lower or 'sum' in query_lower:
        total_spending = transactions_df['amount'].sum()
        response = f"Your total transaction amount is {total_spending:.2f}."
    elif 'maximum' in query_lower or 'max' in query_lower:
        max_spending = transactions_df['amount'].max()
        response = f"Your maximum transaction amount is {max_spending:.2f}."
    elif 'minimum' in query_lower or 'min' in query_lower:
        min_spending = transactions_df['amount'].min()
        response = f"Your minimum transaction amount is {min_spending:.2f}."
    elif 'count' in query_lower or 'number of transactions' in query_lower:
        count_transactions = transactions_df['amount'].count()
        response = f"You have made {count_transactions} transactions."
    else:
        response = "I'm sorry, I couldn't understand your statistical analysis request. Please specify what statistics you'd like to know (e.g., average, total, maximum)."

    return response

def transaction_sender_tool(query: str) -> str:
    """
    Use this tool to send transactions. If information is missing, ask the user for it.
    """
    # Parse the query to extract transaction details
    transaction_details = parse_transaction_query(query)
    missing_info = [key for key, value in transaction_details.items() if not value]
    if missing_info:
        return f"Please provide the following information to proceed with the transaction: {', '.join(missing_info)}."
    else:
        # Implement logic to send the transaction
        # Placeholder implementation:
        return f"Transaction of {transaction_details['amount']} sent to {transaction_details['recipient']} successfully."

def parse_transaction_query(query: str) -> dict:
    # Implement parsing logic to extract 'recipient', 'amount', and 'currency'
    # Placeholder implementation:
    recipient = None
    amount = None

    # Simple parsing logic (to be improved)
    query_lower = query.lower()
    words = query_lower.split()
    if 'send' in words:
        try:
            idx_send = words.index('send')
            amount_word = words[idx_send + 1]
            if amount_word.replace('.', '', 1).isdigit():
                amount = float(amount_word)
            else:
                amount = None
        except (IndexError, ValueError):
            amount = None

    if 'to' in words:
        idx_to = words.index('to')
        try:
            recipient = words[idx_to + 1]
        except IndexError:
            recipient = None

    return {'recipient': recipient, 'amount': amount}

def stock_advisor_tool(query: str) -> str:
    """
    Use this tool to provide a list of the best stocks to trade.
    """
    # Implement logic to fetch and return stock recommendations
    # Placeholder implementation:
    return "Based on current market trends, the top stocks to consider are AAPL, GOOGL, and AMZN."

def loan_predictor_tool(query: str) -> str:
    """
    Use this tool to predict if a user can get a loan.
    """
    # Implement a simple predictive model or load a pre-trained model
    # Placeholder implementation:
    # For demonstration, let's assume we check the user's average transaction amount
    average_spending = transactions_df['amount'].mean()
    if average_spending > 1000:
        return "Based on your financial data, you are eligible for a loan."
    else:
        return "Based on your financial data, you may not be eligible for a loan at this time."

# Define the tools list using the Tool class from langchain
tools = [
    Tool(
        name="CSVReader",
        func=read_csv_tool,
        description="Use this tool to read CSV files containing transaction data and answer questions about them."
    ),
    Tool(
        name="StatisticalAnalyzer",
        func=statistical_analysis_tool,
        description="Use this tool to perform statistical analysis on transaction data."
    ),
    Tool(
        name="TransactionSender",
        func=transaction_sender_tool,
        description="Use this tool to send transactions. If information is missing, ask the user for it."
    ),
    Tool(
        name="StockAdvisor",
        func=stock_advisor_tool,
        description="Use this tool to provide a list of the best stocks to trade."
    ),
    Tool(
        name="LoanPredictor",
        func=loan_predictor_tool,
        description="Use this tool to predict if a user can get a loan."
    ),
]

# Initialize the agent with ReAct framework
agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True
)

# Main function to interact with the user
def main():
    print("Welcome to the Banking Assistant. How can I assist you today?")
    while True:
        user_input = input("User: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Thank you for using the Banking Assistant. Goodbye!")
            break
        response = agent.run(user_input)
        print(f"Agent: {response}")

if __name__ == "__main__":
    main()
