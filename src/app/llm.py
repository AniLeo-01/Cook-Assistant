import os
from typing import List, Dict, Optional

from dotenv import load_dotenv
from openai import OpenAI


class LLMClient:
    def __init__(self, model_name: str, api_key: Optional[str] = None, timeout_s: float = 60.0):
        """
        Client wrapper around OpenAI chat completions.

        Args:
            model_name: Name of the model to call (e.g., "gpt-4o-mini").
            api_key: Optional API key. Defaults to value from OPENAI_API_KEY.
            timeout_s: Request timeout in seconds.
        """
        load_dotenv()
        self.model_name = model_name

        effective_api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not effective_api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Provide api_key or set the environment variable."
            )

        # Configure the OpenAI client once; timeout applies to all requests
        self.client = OpenAI(api_key=effective_api_key, timeout=timeout_s)

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Generate a text response from the configured OpenAI model.

        Args:
            prompt: The user prompt.
            system_prompt: Optional system instruction to steer the assistant.
            temperature: Sampling temperature for creativity vs. determinism.
            max_tokens: Optional maximum tokens for the response.

        Returns:
            The assistant's message content as a string.
        """
        messages: List[Dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        choice = response.choices[0]
        content = getattr(choice.message, "content", None)
        return content.strip() if content else ""