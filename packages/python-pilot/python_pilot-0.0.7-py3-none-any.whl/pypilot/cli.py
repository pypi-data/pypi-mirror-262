import argparse
import os
from dotenv import load_dotenv
from pypilot.console import InteractiveConsoleAgent
from pypilot.agent.python_chat import PythonTerminalChatAgent
from pypilot import utils
from pypilot.version import VERSION as PYPILOT_VERSION

parser = argparse.ArgumentParser(description="Python Pilot - A python terminal assistant")
parser.add_argument("--api-key", help="API key for OPENAI (optional)")
parser.add_argument("--provider", help="API key for OPENAI (optional)")


def main():
    args = parser.parse_args()

    load_dotenv()
    api_key=args.api_key or os.getenv("OPENAI_API_KEY")
    provider = args.provider or "openai"
    
    console = InteractiveConsoleAgent(
        auto_approve_llm_use=True,
        token_count_limit=2048,
        stream=True,
        agent=PythonTerminalChatAgent(
            provider=provider, 
            model="gpt-3.5-turbo", 
            api_key=api_key, 
            # auto_select_code=True
        ),
    )
    # console.load("/Users/roypasternak/GIT/larium/agnets/py-agent/console-agent.txt")
    console.interact(
        banner=f"""============
PyPilot {PYPILOT_VERSION} - Python Terminal Agent
- Use # to communicate with the agent, e.g. `# create simple http server`.
- Use ! to run a system command, e.g. `!pip install numpy`.
- The agent is aware of the terminal history and locals.
- Type {console.repr_custom_commands()} for custom commands.
- Any key will approve, ctrl+c will cancel.
{utils.add_color('- You must set API KEY to use the agent, use the set_api_key() command.', 'orange') if api_key is None else ''}"""
    )
    # print(console.history())
    # print(console.get_user_locals())
    
if __name__ == '__main__':
    main()