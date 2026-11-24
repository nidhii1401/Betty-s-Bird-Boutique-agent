"""
agent.py

Defines the root agent for Betty's Bird Boutique's customer service chatbot.
The root agent has three tools available to it:
    1. get_product_price   -- MySQL product pricing, via MCP Toolbox.
    2. search_store_documents -- Vertex AI Search over store PDF documents.
    3. general_bird_search_tool -- Grounding with Google Search (as a
       sub-agent wrapped in an AgentTool).
"""

import os

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from toolbox_core import ToolboxSyncClient

from .datastore import search_store_documents
from .search_agent import general_bird_search_tool

load_dotenv()

# --- Short-term session storage -------------------------------------------
# The agent only needs to remember facts within a single conversation (e.g.
# which bird a customer asked about earlier in the chat) -- it does not need
# to persist memory across separate conversations/sessions. InMemorySessionService
# is the right fit: it's built into ADK, requires no extra infrastructure,
# and keeps turn history available for the lifetime of the process, which is
# all this project needs for local development in the adk web previewer.
session_service = InMemorySessionService()

# --- Product database tool (MCP Toolbox) -----------------------------------
TOOLBOX_URL = os.environ.get("TOOLBOX_URL", "http://127.0.0.1:5000")
db_client = ToolboxSyncClient(TOOLBOX_URL)
product_price_tool = db_client.load_tool("get_product_price")

# --- Agent prompt ------------------------------------------------------------
_PROMPT_PATH = os.path.join(os.path.dirname(__file__), "agent-prompt.txt")
with open(_PROMPT_PATH, "r", encoding="utf-8") as f:
    ROOT_AGENT_INSTRUCTION = f.read()

# --- Model selection ---------------------------------------------------------
# gemini-2.5-flash was chosen for the root agent after testing all three
# candidates:
#   - gemini-2.5-pro:        Most careful about following the topic
#                            guardrail and choosing the right tool, but
#                            noticeably slower -- not ideal for a live chat
#                            widget where customers expect quick replies.
#   - gemini-2.5-flash:      Nearly as accurate as pro on tool selection and
#                            guardrail adherence in testing, with much lower
#                            latency. Best overall fit for this use case.
#   - gemini-2.5-flash-lite: Fastest, but noticeably less reliable at
#                            correctly choosing between the three tools and
#                            at politely enforcing the bird/store-only
#                            guardrail, so it was not used for the final
#                            configuration.
ROOT_AGENT_MODEL = "gemini-2.5-flash"

root_agent = Agent(
    name="betty_bird_boutique_agent",
    model=ROOT_AGENT_MODEL,
    description=(
        "Customer service agent for Betty's Bird Boutique, a pet store "
        "specializing in birds. Answers questions about store products and "
        "pricing, store information (hours, location, history, staff), and "
        "general bird knowledge. Does not take orders."
    ),
    instruction=ROOT_AGENT_INSTRUCTION,
    tools=[
        product_price_tool,
        search_store_documents,
        general_bird_search_tool,
    ],
)