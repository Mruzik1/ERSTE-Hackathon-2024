import re
from typing import Union
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.exceptions import OutputParserException
from langchain.agents.agent import AgentOutputParser


class CustomOutputParser(AgentOutputParser):
    """Output parser for the ReAct agent that handles 'Action:' and 'Action Input:'."""
    
    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        # Define regex pattern for matching both Action and Action Input lines
        pattern = r"Action:\s*(.*?)\s*Action Input:\s*(.*)"
        match = re.search(pattern, text.strip())
        
        # If the pattern doesn't match, raise an exception
        if match is None:
            raise OutputParserException(f"Could not parse LLM Output: {text}")
        
        # Extract action and action input from regex groups
        action = match.group(1).strip()
        action_input = match.group(2).strip()
        
        # Return AgentFinish if the action is 'Finish'
        if action.lower() == "finish":
            return AgentFinish({"output": action_input}, text)
        
        # Otherwise, return AgentAction
        return AgentAction(action, action_input, text)

    @property
    def _type(self) -> str:
        return "react"
