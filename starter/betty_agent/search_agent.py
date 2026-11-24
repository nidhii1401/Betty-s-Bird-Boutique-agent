"""
search_agent.py

Defines a dedicated sub-agent that answers general bird-related questions
using Grounding with Google Search, and wraps it as an AgentTool so the
root agent (in agent.py) can delegate to it.

Grounding with Google Search only works when a model calls the built-in
`google_search` tool directly, so this has to be a *separate* agent/model
configuration rather than just another tool bolted onto the root agent.
"""

import os

from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool

# Load the search agent's persona/instructions from a text file, matching
# the pattern used for the root agent's prompt.
_PROMPT_PATH = os.path.join(os.path.dirname(__file__), "search-prompt.txt")
with open(_PROMPT_PATH, "r", encoding="utf-8") as f:
    SEARCH_AGENT_INSTRUCTION = f.read()

# Model choice: gemini-2.5-flash is used for this search agent because
# Grounding with Google Search is latency-sensitive in this architecture --
# this agent is invoked as a *sub-tool* from inside the root agent's own
# turn, so its response time is added directly on top of the root agent's
# own thinking time. gemini-2.5-flash supports Google Search grounding
# (available on the full 2.0/2.5 Gemini family, not just pro-tier models)
# while responding noticeably faster than gemini-2.5-pro. In testing,
# gemini-2.5-pro produced marginally richer summaries of search results,
# but flash's grounded, cited answers were accurate enough for general bird
# facts, and the latency savings mattered more for a live chat experience.
# gemini-2.5-flash-lite was not used here because its grounded answers were
# less consistent about surfacing clear source attribution.
SEARCH_AGENT_MODEL = "gemini-2.5-flash"

search_agent = Agent(
    name="general_bird_search_agent",
    model=SEARCH_AGENT_MODEL,
    description=(
        "Answers general knowledge questions about birds (species, diet, "
        "behavior, care, current bird-related news) by grounding its "
        "answers in Google Search results."
    ),
    instruction=SEARCH_AGENT_INSTRUCTION,
    tools=[google_search],
)

# Wrap the search agent as a tool so the root agent can call it like any
# other tool. The name/description here are what the root agent's model
# sees when deciding whether to delegate to this tool.
general_bird_search_tool = AgentTool(
    agent=search_agent,
)