import os
import sys
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import asyncio

load_dotenv()
mcp_tools = []
async def main():

    current_dir = os.path.dirname(os.path.abspath(__file__))
    math_script = os.path.join(current_dir, "mathserver.py")
    client = MultiServerMCPClient(
        {
            "math":{
                "command":sys.executable,
                "args":[math_script], #Ensure correct absolute path
                "transport":"stdio",
            },
        }
    )

    os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")
    tools = await client.get_tools()
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    agent = create_agent(
        model,
        tools
    )

    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "What is (3+5) x 12 ?"}]}
    )
    print("Math_response: ", math_response['messages'][-1].content[0]['text'])

    mcp_tools = await client.get_tools()
    print(f"Loaded {len(mcp_tools)} MCP tools: {[t.name for t in mcp_tools]}")

asyncio.run(main())

