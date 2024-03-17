"""
Defines internal configuration for mapping user inputs to supported LLM providers and models.
This configuration helps in estimating costs by detailing the per-token price for inputs and outputs across different models.

Format: 
    {
        "provider": "Name of provider",
        "adapter_path": "Path to provider specific adapter",
        "models": [
            {
                "name": "name of model",
                "cost_per_token_input": Flat price per output token,
                "cost_per_token_output": Flat price per input token,
            },
        ],
    }
]
"""

from typing import Any, Dict, List

internal_config: List[Dict[str, Any]] = [
    {
        "provider": "OpenAI",
        "adapter_path": "proxyllm.provider.openai.chatgpt.OpenAIAdapter",
        "models": [
            # GPT-4 Turbo
            {
                "name": "gpt-4-0125-preview",
                "cost_per_token_input": 10e-06,
                "cost_per_token_output": 30e-06,
            },
            {
                "name": "gpt-4-1106-preview",
                "cost_per_token_input": 10e-06,
                "cost_per_token_output": 30e-06,
            },
            # GPT-4
            {
                "name": "gpt-4",
                "cost_per_token_input": 30e-06,
                "cost_per_token_output": 60e-06,
            },
            {
                "name": "gpt-4-32k",
                "cost_per_token_input": 60e-06,
                "cost_per_token_output": 120e-06,
            },
            # GPT-3.5 Turbo || LEGACY
            # {
            #     "name": "gpt-3.5-turbo-instruct",
            #     "cost_per_token_input": 1.5e-06,
            #     "cost_per_token_output": 2e-06,
            # },
            {
                "name": "gpt-3.5-turbo-0125",
                "cost_per_token_input": 0.5e-06,
                "cost_per_token_output": 1.5e-06,
            },
            # Older Models
            {
                "name": "gpt-3.5-turbo-1106",
                "cost_per_token_input": 1e-06,
                "cost_per_token_output": 2e-06,
            },
            {
                "name": "gpt-3.5-turbo-0613",
                "cost_per_token_input": 1.5e-06,
                "cost_per_token_output": 2e-06,
            },
            {
                "name": "gpt-3.5-turbo-16k-0613",
                "cost_per_token_input": 3e-06,
                "cost_per_token_output": 4e-06,
            },
            {
                "name": "gpt-3.5-turbo-0301",
                "cost_per_token_input": 1.5e-06,
                "cost_per_token_output": 2e-06,
            },
        ],
    },
    {
        "provider": "Llama2",
        "adapter_path": "proxyllm.provider.huggingface.llama2.Llama2Adapter",
        "models": [
            {
                "name": "llama-2-7b-chat-hf",
                "cost_per_token_input": 5e-08,
                "cost_per_token_output": 2.5e-07,
            },
            {
                "name": "llama-2-7b-chat",
                "cost_per_token_input": 5e-08,
                "cost_per_token_output": 2.5e-07,
            },
            {
                "name": "llama-2-7b-hf",
                "cost_per_token_input": 5e-08,
                "cost_per_token_output": 2.5e-07,
            },
            {
                "name": "llama-2-7b",
                "cost_per_token_input": 5e-08,
                "cost_per_token_output": 2.5e-07,
            },
            {
                "name": "llama-2-13b-chat-hf",
                "cost_per_token_input": 1e-07,
                "cost_per_token_output": 5e-07,
            },
            {
                "name": "llama-2-13b-chat",
                "cost_per_token_input": 1e-07,
                "cost_per_token_output": 5e-07,
            },
            {
                "name": "llama-2-13b-hf",
                "cost_per_token_input": 1e-07,
                "cost_per_token_output": 5e-07,
            },
            {
                "name": "llama-2-13b",
                "cost_per_token_input": 1e-07,
                "cost_per_token_output": 5e-07,
            },
            {
                "name": "llama-2-70b-chat-hf",
                "cost_per_token_input": 6.5e-07,
                "cost_per_token_output": 2.75e-06,
            },
            {
                "name": "llama-2-70b-chat",
                "cost_per_token_input": 6.5e-07,
                "cost_per_token_output": 2.75e-06,
            },
            {
                "name": "llama-2-70b-hf",
                "cost_per_token_input": 6.5e-07,
                "cost_per_token_output": 2.75e-06,
            },
            {
                "name": "llama-2-70b",
                "cost_per_token_input": 6.5e-07,
                "cost_per_token_output": 2.75e-06,
            },
        ],
    },
    {
        "provider": "Mistral",
        "adapter_path": "proxyllm.provider.huggingface.mistral.MistralAdapter",
        "models": [
            {
                "name": "mistral-7b-v0.1",
                "cost_per_token_input": 5e-08,
                "cost_per_token_output": 2.5e-07,
            },
            {
                "name": "mistral-7b-instruct-v0.2",
                "cost_per_token_input": 5e-08,
                "cost_per_token_output": 2.5e-07,
            },
            {
                "name": "mixtral-8x7b-instruct-v0.1",
                "cost_per_token_input": 3e-07,
                "cost_per_token_output": 1e-06,
            },
        ],
    },
    {
        "provider": "Cohere",
        "adapter_path": "proxyllm.provider.cohere.cohere.CohereAdapter",
        "models": [
            {
                "name": "command-r",
                "cost_per_token_input": 0.5e-06,
                "cost_per_token_output": 1.5e-06,
            },
            {
                "name": "command",
                "cost_per_token_input": 1.5e-06,
                "cost_per_token_output": 2e-06,
            },
            {
                "name": "command-light",
                "cost_per_token_input": 1.5e-06,
                "cost_per_token_output": 2e-06,
            },
            {
                "name": "command-nightly",
                "cost_per_token_input": 1.5e-06,
                "cost_per_token_output": 2e-06,
            },
            {
                "name": "command-light-nightly",
                "cost_per_token_input": 1.5e-06,
                "cost_per_token_output": 2e-06,
            },
        ],
    },
    {
        "provider": "Vertexai",
        "adapter_path": "proxyllm.provider.google.vertexai.VertexAIAdapter",
        "models": [
            {
                "name": "text-bison",
                "cost_per_token_input": 1.5e-06,
                "cost_per_token_output": 2e-06,
            },
            {
                "name": "gemini-pro",
                "cost_per_token_input": 1.25e-07,
                "cost_per_token_output": 3.75e-07,
            },
            {
                "name": "chat-bison",
                "cost_per_token_input": 1.5e-06,
                "cost_per_token_output": 2e-06,
            },
        ],
    },
]
