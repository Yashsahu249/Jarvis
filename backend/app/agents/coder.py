import re
from typing import Any
from loguru import logger
from app.services.llm_service import llm_service
from app.services.repo_service import repo_service


class CoderAgent:
    def __init__(self):
        self.id = "coder"
        self.name = "Coder Agent"
        self.role = "coder"

    async def generate_code(self, description: str, language: str = "python", context: str | None = None) -> dict:
        prompt = (
            f"Generate {language} code for the following task.\n\n"
            f"Description: {description}\n\n"
        )
        if context:
            prompt += f"Context:\n{context}\n\n"
        prompt += (
            "Provide the code in a single code block. Include necessary imports and comments.\n"
            "Respond with the code block and a brief explanation."
        )

        messages = [{"role": "user", "content": prompt}]
        code = await llm_service.chat(messages, temperature=0.3)
        return self._parse_code(code, language)

    async def review_code(self, code: str, language: str = "python") -> dict:
        prompt = (
            f"Review the following {language} code for bugs, security issues, "
            f"performance problems, and style improvements.\n\n"
            f"```{language}\n{code}\n```\n\n"
            "Provide your review as a JSON object with: 'issues' (list of dicts with "
            "'severity', 'line', 'description', 'suggestion'), 'overall_quality' (1-10), "
            "'summary' (string).\n"
            "Only respond with the JSON object."
        )
        messages = [{"role": "user", "content": prompt}]
        response = await llm_service.chat(messages, temperature=0.3)

        try:
            cleaned = re.sub(r"```json\s*|\s*```", "", response.strip())
            return __import__("json").loads(cleaned)
        except (__import__("json").JSONDecodeError, Exception):
            return {"issues": [], "overall_quality": 5, "summary": response[:200]}

    async def debug_code(self, code: str, error: str, language: str = "python") -> dict:
        prompt = (
            f"Debug the following {language} code that produces this error:\n\n"
            f"Error: {error}\n\n"
            f"Code:\n```{language}\n{code}\n```\n\n"
            "Analyze the root cause and provide a fix.\n"
        )
        messages = [{"role": "user", "content": prompt}]
        analysis = await llm_service.chat(messages, temperature=0.3)
        return {"analysis": analysis, "original_error": error}

    async def refactor_code(self, code: str, instructions: str, language: str = "python") -> dict:
        prompt = (
            f"Refactor the following {language} code according to these instructions:\n\n"
            f"Instructions: {instructions}\n\n"
            f"Code:\n```{language}\n{code}\n```\n\n"
            "Provide the refactored code and a summary of changes."
        )
        messages = [{"role": "user", "content": prompt}]
        result = await llm_service.chat(messages, temperature=0.3)
        refactored_code, explanation = self._parse_code(result, language)
        return {"code": refactored_code, "explanation": explanation, "original_length": len(code)}

    async def explain_code(self, code: str, language: str = "python") -> str:
        prompt = (
            f"Explain the following {language} code in simple terms:\n\n"
            f"```{language}\n{code}\n```\n\n"
            "Provide a clear, concise explanation of what this code does."
        )
        messages = [{"role": "user", "content": prompt}]
        return await llm_service.chat(messages, temperature=0.5)

    def _parse_code(self, response: str, language: str) -> dict:
        pattern = rf"```{language}\s*\n(.*?)```"
        match = re.search(pattern, response, re.DOTALL)
        if match:
            code = match.group(1).strip()
            explanation = response[:match.start()].strip() + response[match.end():].strip()
        else:
            pattern = r"```\s*\n(.*?)```"
            match = re.search(pattern, response, re.DOTALL)
            if match:
                code = match.group(1).strip()
                explanation = response[:match.start()].strip() + response[match.end():].strip()
            else:
                code = response.strip()
                explanation = ""
        return {"code": code, "explanation": explanation}


coder_agent = CoderAgent()
