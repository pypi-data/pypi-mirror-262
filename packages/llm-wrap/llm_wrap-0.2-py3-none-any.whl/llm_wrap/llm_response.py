from typing import Literal, Generator
from llm_wrap.llms.gpt_api import chatCompletion
from llm_wrap.llms.claude_api import get_message as get_claude_message
from llm_wrap.llms.claude_api import get_stream_message as get_claude_stream_message
from llm_wrap.logger import get_logger
logging = get_logger()

def convert_kwargs_from_openai_to_claude(kwargs) -> dict:
    """
    This function converts keyword arguments from OpenAI's format to Claude's format.

    Parameters:
    **kwargs: Arbitrary keyword arguments. These will be converted to Claude's format.

    Returns:
    The keyword arguments in Claude's format.
    """
    kwargs_claude = kwargs.copy()
    if kwargs["messages"][0]["role"] == "system":
        kwargs_claude["system"] = kwargs["messages"][0]["content"]
        messages = kwargs_claude.pop("messages")
        messages = messages[1:]
        kwargs_claude["messages"] = messages
    return kwargs_claude

def get_streaming_response(llm_api:Literal["openai", "claude"]='openai', api_key=None, **kwargs) -> Generator[str, None, None]:
    """
    Retrieves a streaming response from the specified LLM API.

    This function provides a streaming interface for getting responses from an LLM API. It currently supports streaming from Claude's API. OpenAI's API streaming is not supported yet.

    Parameters:
    llm_api (Literal["openai", "claude"]): The LLM API to use. Default is 'openai'.
    api_key (str, optional): The API key required for accessing the Claude API.
    **kwargs: Keyword arguments. Currently, params for OpenAI's GPT API are supported. When using Claude's API, the parameters are converted to Claude's format. For example, the system message should be included in the first element of "messages".

    Yields:
    Generator[str, None, None]: A generator that yields responses from the LLM API as strings.

    Raises:
    ValueError: If the `llm_api` is 'openai', as streaming is not supported for OpenAI API yet.
    ValueError: If the `api_key` is None when using Claude's API, as it is required.
    ValueError: If an unsupported `llm_api` is specified.

    Example:
    >>> for response in get_streaming_response('claude', api_key='your_api_key', messages=[...]):
    ...     print(response)
    """
    if llm_api == 'openai':
        raise ValueError("get_streaming_response is not supported for OpenAI API yet")
    elif llm_api == 'claude':
        if api_key is None:
            raise ValueError("API key is required for Claude API")
        kwargs_claude = convert_kwargs_from_openai_to_claude(kwargs)
        yield from get_claude_stream_message(api_key=api_key, **kwargs_claude)
    else:
        raise ValueError(f"llm_wrap does not support this API: {llm_api}")

def get_response(llm_api:Literal["openai", "claude"]='openai', api_key=None, **kwargs) -> str:
    """
    This function acts as an interface for consumer libraries to get AI's response.
    It currently supports OpenAI's GPT API, but can be extended to support other APIs.

    Parameters:
    api (str): The API to use. Default is 'openai'.
    api_key (str): The API key to use.
    **kwargs: Keyword arguments. Currently, params for OpenAI's GPT API are supported. When using Claude's API, the parameters are converted to Claude's format. For example, the system message should be included in the first element of "messages".

    Returns:
    The response from the AI.
    """
    logging.info("llm_wrap: llm_api: %s", llm_api)
    if llm_api == 'openai':
        # TODO: Pass "api_key" arg to ChatCompletion
        response = chatCompletion(**kwargs)
        return response.choices[0].message.content
    elif llm_api == 'claude':
        if api_key is None:
            raise ValueError("API key is required for Claude API")
        kwargs_claude = convert_kwargs_from_openai_to_claude(kwargs)
        get_claude_message(api_key=api_key, **kwargs_claude)
    else:
        raise ValueError(f"llm_wrap does not support this API: {llm_api}")