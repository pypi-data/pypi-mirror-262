from pypilot.agent import base
from pypilot.parser import json_parser      
from pypilot.agent.prompt import Prompt
PROMPT = Prompt(messages=[
        {"role": "system", "content": """
Given a user request inside a python terminal, select the best suited agent to handle the request. 

Answer with a markdown code snippet with a JSON object formatted to look like:
```json
{{
    "thought": explain your thought process of selecting the agent,
    "agent": name of the agent,
}}
```

Agents:
- PythonCodeAgent: A python coding assistant that writes python code.
- ChatAgent: A chatbot that engage in a conversation mostly about coding and python.

Prefer the code agent when possible, use the chat agent only when no code needed or when you need to gather more information from the user.

Here is the python terminal recent history:
{history}
"""},
            {"role": "user", "content": "{instruction}"}
    ])

OUTPUT_PARSER = json_parser

class RouterAgent(base.AgentBase):
    output_parser = OUTPUT_PARSER
    prompt: Prompt = PROMPT