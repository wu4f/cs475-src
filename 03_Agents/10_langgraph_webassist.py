import os
import asyncio
import httpx
from typing import TypedDict

from langgraph.graph import StateGraph, END
from langgraph.types import Send

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmCategory,
    HarmBlockThreshold,
)

# ---------------------------------------------------------------------
# LLM (Gemini)
# ---------------------------------------------------------------------

llm = ChatGoogleGenerativeAI(
    model=os.getenv("GOOGLE_MODEL"),
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
    },
)

# ---------------------------------------------------------------------
# Graph state
# ---------------------------------------------------------------------

class State(TypedDict):
    query: str
    nba: str | None
    nfl: str | None

# ---------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------

async def fetch(url: str) -> str:
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url)
        return r.text

async def extract_and_summarize(html: str, sport: str) -> str:
    prompt = f"""
You are given raw HTML from {sport}.com.

1. Identify the main news article headlines on the page.
2. Ignore navigation, ads, and footers.
3. Summarize the current news in ONE concise paragraph.
4. Return only that paragraph as a string

HTML:
{html[:12000]}
"""
    resp = await llm.ainvoke(prompt)
    return resp.content.strip()

# ---------------------------------------------------------------------
# Agents
# ---------------------------------------------------------------------

async def nba_agent(state: State):
    html = await fetch("https://www.espn.com/espn/rss/nba/news")
    summary = await extract_and_summarize(html, "nba")
    return {"nba": summary}

async def nfl_agent(state: State):
    html = await fetch("https://www.espn.com/espn/rss/nfl/news")
    summary = await extract_and_summarize(html, "nfl")
    return {"nfl": summary}

async def coordinator(state: State):
    return {}

async def route(state: State):
    prompt = f"""
User request: {state['query']}

Decide which sports news is requested.
Reply with exactly one word:
nba
nfl
both
"""
    resp = await llm.ainvoke(prompt)
    decision = resp.content.lower().strip()

    if decision == "nba":
        return Send("nba", state)
    if decision == "nfl":
        return Send("nfl", state)
    return [Send("nba", state), Send("nfl", state)]

# Graph

g = StateGraph(State)

g.add_node("coord", coordinator)
g.add_node("nba", nba_agent)
g.add_node("nfl", nfl_agent)

g.set_entry_point("coord")
g.add_conditional_edges("coord", route)

g.add_edge("nba", END)
g.add_edge("nfl", END)

app = g.compile()

# Interactive prompt

print("Welcome to my sports headlines summary application.  Ask me to summarize news from a sport.")

while True:
    line = input("llm>> ")
    if line:
        try:
            result = asyncio.run(app.ainvoke({"query": line}))
            if result.get("nba"):
                print(result["nba"])
            if result.get("nfl"):
                print(result["nfl"])
        except Exception as e:
            print(e)
    else:
        break
