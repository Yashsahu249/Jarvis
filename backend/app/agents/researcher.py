import json
import re
from typing import Any
from loguru import logger
from app.services.llm_service import llm_service
from app.core.config import settings


class ResearcherAgent:
    def __init__(self):
        self.id = "researcher"
        self.name = "Researcher Agent"
        self.role = "researcher"

    async def search_web(self, query: str, max_results: int = 5) -> list[dict]:
        if settings.TAVILY_API_KEY:
            return await self._search_tavily(query, max_results)
        return await self._search_fallback(query, max_results)

    async def _search_tavily(self, query: str, max_results: int) -> list[dict]:
        try:
            import httpx
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.post(
                    "https://api.tavily.com/search",
                    json={
                        "api_key": settings.TAVILY_API_KEY,
                        "query": query,
                        "max_results": max_results,
                        "search_depth": "advanced",
                    },
                )
                if resp.status_code == 200:
                    data = resp.json()
                    return [
                        {
                            "title": r.get("title", ""),
                            "url": r.get("url", ""),
                            "content": r.get("content", ""),
                            "score": r.get("score", 0),
                        }
                        for r in data.get("results", [])
                    ]
        except Exception as e:
            logger.warning(f"Tavily search failed: {e}")
        return []

    async def _search_fallback(self, query: str, max_results: int) -> list[dict]:
        prompt = (
            f"Provide search results for: {query}\n\n"
            f"Respond with a JSON array of {max_results} results. "
            f"Each result must have: 'title', 'url', 'content' (a brief summary), 'score'.\n"
            "Only respond with the JSON array."
        )
        messages = [{"role": "user", "content": prompt}]
        response = await llm_service.chat(messages, temperature=0.5)

        try:
            cleaned = re.sub(r"```json\s*|\s*```", "", response.strip())
            return json.loads(cleaned)
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse search results")
            return [{"title": query, "url": "", "content": response[:200], "score": 1}]

    async def synthesize(self, query: str, results: list[dict]) -> str:
        context = "\n\n".join([
            f"Source {i+1}: {r.get('title', 'Untitled')}\nURL: {r.get('url', '')}\n{r.get('content', '')[:500]}"
            for i, r in enumerate(results[:5])
        ])
        prompt = (
            f"Research Question: {query}\n\n"
            f"Based on the following sources, provide a comprehensive synthesis:\n\n{context}\n\n"
            "Provide a well-structured answer with key findings, supporting evidence, and source citations."
        )
        messages = [{"role": "user", "content": prompt}]
        return await llm_service.chat(messages, temperature=0.5)

    async def fact_check(self, claim: str) -> dict:
        prompt = (
            f"Fact check the following claim: {claim}\n\n"
            "Respond with a JSON object containing: 'claim' (string), 'verdict' (true/false/partially_true/uncertain), "
            "'confidence' (0-1), 'explanation' (string), 'sources' (list of strings).\n"
            "Only respond with the JSON object."
        )
        messages = [{"role": "user", "content": prompt}]
        response = await llm_service.chat(messages, temperature=0.3)

        try:
            cleaned = re.sub(r"```json\s*|\s*```", "", response.strip())
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return {"claim": claim, "verdict": "uncertain", "confidence": 0.0, "explanation": response[:200], "sources": []}

    async def extract_info(self, text: str, schema: dict[str, str] | None = None) -> dict:
        prompt = f"Extract structured information from the following text.\n\nText: {text}\n\n"
        if schema:
            prompt += f"Extract these fields: {json.dumps(schema)}\n"
        prompt += (
            "Respond with a JSON object containing the extracted information.\n"
            "Only respond with the JSON object."
        )
        messages = [{"role": "user", "content": prompt}]
        response = await llm_service.chat(messages, temperature=0.3)

        try:
            cleaned = re.sub(r"```json\s*|\s*```", "", response.strip())
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return {"extracted": response[:200]}


researcher_agent = ResearcherAgent()
