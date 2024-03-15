import anthropic
import os
from typing import Any, Dict, List, Optional, Generator, Union

from ..logger import get_logger
logging = get_logger()

def create_client_and_params(
    api_key: str,
    messages: List[Dict[str, Any]],
    system: str = "Please assist me",
    temperature: float = 0,
    max_tokens: int = 2048,
    stop_sequences: Optional[List[str]] = None,
    top_p: Optional[float] = None,
    top_k: Optional[int] = None,
    metadata: Optional[Dict[str, Any]] = None
):
    client = anthropic.Anthropic(
        api_key=api_key,
    )
    logging.info(f"[claude_api#get_message] api_key: {api_key}")

    # Prepare parameters
    params = {
        "model": "claude-3-opus-20240229",
        "system": system,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    # Optional parameters
    optional_params = {
        "top_p": top_p,
        "top_k": top_k,
        "stop_sequences": stop_sequences,
        "metadata": metadata,
    }

    # Add optional parameters if they are not None
    params.update({k: v for k, v in optional_params.items() if v is not None})
    return client, params

def get_message(
    api_key: str,
    messages: List[Dict[str, Any]],
    system: str = "Please assist me",
    temperature: float = 0,
    max_tokens: int = 2048,
    stop_sequences: Optional[List[str]] = None,
    top_p: Optional[float] = None,
    top_k: Optional[int] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Union[str, Generator[str, None, None]]:
    """
    Constructs and sends a request to the Anthropic API to generate a message based on the provided parameters.

    Args:
        messages (List[Dict[str, Any]]): The messages to be processed.
        stream (bool, optional): Whether to use streaming. Defaults to False.
        system (str, optional): The system message to be used. Defaults to "Please assist me".
        temperature (float, optional): The temperature setting for the generation. Defaults to 0.5.
        max_tokens (int, optional): The maximum number of tokens to generate. Defaults to 2048.
        stop_sequences (Optional[List[str]], optional): Sequences that indicate the end of a generation. Defaults to None.
        top_p (Optional[float], optional): The top p parameter for generation. Defaults to None.
        top_k (Optional[int], optional): The top k parameter for generation. Defaults to None.
        metadata (Optional[Dict[str, Any]], optional): Additional metadata for the request. Defaults to None.

    Returns:
        str: The generated message content.
    """

    client, params = create_client_and_params(
        api_key=api_key,
        messages=messages,
        system=system,
        temperature=temperature,
        max_tokens=max_tokens,
        stop_sequences=stop_sequences,
        top_p=top_p,
        top_k=top_k,
        metadata=metadata
    )
    message = client.messages.create(**params)
    return message.content[0].text

def get_stream_message(
    api_key: str,
    messages: List[Dict[str, Any]],
    system: str = "Please assist me",
    temperature: float = 0,
    max_tokens: int = 2048,
    stop_sequences: Optional[List[str]] = None,
    top_p: Optional[float] = None,
    top_k: Optional[int] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Generator[str, None, None]:
    """
    Constructs and sends a request to the Anthropic API to generate a message based on the provided parameters.

    Args:
        messages (List[Dict[str, Any]]): The messages to be processed.
        stream (bool, optional): Whether to use streaming. Defaults to False.
        system (str, optional): The system message to be used. Defaults to "Please assist me".
        temperature (float, optional): The temperature setting for the generation. Defaults to 0.5.
        max_tokens (int, optional): The maximum number of tokens to generate. Defaults to 2048.
        stop_sequences (Optional[List[str]], optional): Sequences that indicate the end of a generation. Defaults to None.
        top_p (Optional[float], optional): The top p parameter for generation. Defaults to None.
        top_k (Optional[int], optional): The top k parameter for generation. Defaults to None.
        metadata (Optional[Dict[str, Any]], optional): Additional metadata for the request. Defaults to None.

    Returns:
        str: The generated message content.
    """

    client, params = create_client_and_params(
        api_key=api_key,
        messages=messages,
        system=system,
        temperature=temperature,
        max_tokens=max_tokens,
        stop_sequences=stop_sequences,
        top_p=top_p,
        top_k=top_k,
        metadata=metadata
    )

    logging.info(f"[claude_api#get_stream_message] system: {system[0:50]}")

    with client.messages.stream(**params) as stream:
        for text in stream.text_stream:
            print(f"[claude_api#get_stream_message] generated text: {text}")
            yield text
