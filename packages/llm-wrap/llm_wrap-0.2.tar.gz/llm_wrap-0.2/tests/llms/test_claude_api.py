import os
import unittest
from unittest import skipIf

USE_ACTUAL_LLM_API = False
def skip_if_no_api():
    return skipIf(not USE_ACTUAL_LLM_API, "Skipping this test because USE_ACTUAL_LLM_API is False")

from unittest.mock import patch, MagicMock
from llm_wrap.llms.claude_api import get_message, get_stream_message

class TestGetMessage(unittest.TestCase):
    # @patch('llm_wrap.llms.claude_api.os.getenv')
    # @patch('llm_wrap.llms.claude_api.anthropic.Anthropic')
    @skip_if_no_api()
    def test_get_message_with_actual_API(self): #, mock_anthropic, mock_getenv):
        """
        Test the get_message function to ensure it calls client.messages.create and returns a valid string.
        """
        # Setup
        # mock_getenv.return_value = 'fake_api_key'
        # mock_client_instance = MagicMock()
        # mock_anthropic.return_value = mock_client_instance
        # expected_message_content = "Test response"
        # mock_client_instance.messages.create.return_value = MagicMock(content=expected_message_content)
        api_key = os.getenv("ANTHROPIC_API_KEY")

        # Execute
        actual_message_content = get_message(api_key=api_key, messages=[{"role": "user", "content": "Hello, Claude"}])

        # Verify
        self.assertIsInstance(actual_message_content, str)
        # self.assertEqual(actual_message_content, expected_message_content)
        # mock_client_instance.messages.create.assert_called_once()
        print(actual_message_content)

    @patch('llm_wrap.llms.claude_api.os.getenv')
    @patch('llm_wrap.llms.claude_api.anthropic.Anthropic')
    def test_get_message_with_None_params(self, mock_anthropic, mock_getenv):
        # Setup
        mock_getenv.return_value = 'fake_api_key'
        mock_client_instance = MagicMock()
        mock_anthropic.return_value = mock_client_instance
        expected_message_content = "Test response"
        # Correctly adjust the mock to return a structure that matches the expected format
        mock_client_instance.messages.create.return_value = MagicMock(content=[MagicMock(text=expected_message_content)])

        # Execute
        actual_message_content = get_message(api_key='fake_api_key', messages=[{"role": "user", "content": "Hello, Claude"}])

        # Verify
        self.assertEqual(actual_message_content, expected_message_content)
        mock_anthropic.assert_called_once_with(api_key='fake_api_key')
        mock_client_instance.messages.create.assert_called_once_with(
            model="claude-3-opus-20240229",
            system="Please assist me",
            messages=[{"role": "user", "content": "Hello, Claude"}],
            temperature=0,
            max_tokens=2048,
        )

    @patch('llm_wrap.llms.claude_api.os.getenv')
    @patch('llm_wrap.llms.claude_api.anthropic.Anthropic')
    def test_get_message_with_all_params(self, mock_anthropic, mock_getenv):
        # Setup
        mock_getenv.return_value = 'fake_api_key'
        mock_client_instance = MagicMock()
        mock_anthropic.return_value = mock_client_instance
        expected_message_content = "Test response"
        # Correctly adjust the mock to return a structure that matches the expected format
        mock_client_instance.messages.create.return_value = MagicMock(content=[MagicMock(text=expected_message_content)])

        # Execute
        actual_message_content = get_message(api_key='fake_api_key', messages=[{"role": "user", "content": "Hello, Claude"}], top_p=0.8)

        # Verify
        self.assertEqual(actual_message_content, expected_message_content)
        mock_anthropic.assert_called_once_with(api_key='fake_api_key')
        mock_client_instance.messages.create.assert_called_once_with(
            model="claude-3-opus-20240229",
            system="Please assist me",
            messages=[{"role": "user", "content": "Hello, Claude"}],
            temperature=0,
            max_tokens=2048,
            top_p=0.8,
        )


class TestClaudeAPIStreaming(unittest.TestCase):
    """
    Test cases for the get_message function with streaming enabled.
    """

    @skip_if_no_api()
    def test_streaming_output_type(self):
        """
        Test that the output of get_message with stream=True is a generator.
        """
        api_key = os.getenv("ANTHROPIC_API_KEY")
        messages = [{"role": "user", "content": "Hello"}]
        stream = True

        output = get_stream_message(api_key, messages)
        self.assertTrue(hasattr(output, '__iter__') and not hasattr(output, '__len__'), "Output should be a generator")

    @skip_if_no_api()
    def test_streaming_content(self):
        """
        Test that the streaming content is not empty and is a string.
        """
        api_key = os.getenv("ANTHROPIC_API_KEY")
        messages = [{"role": "user", "content": "Hello"}]

        output = get_stream_message(api_key, messages)
        try:
            first_message = next(output)
            self.assertIsInstance(first_message, str, "The streamed message should be a string")
            self.assertTrue(len(first_message) > 0, "The streamed message should not be empty")
        except StopIteration:
            self.fail("The generator did not yield any output")

if __name__ == '__main__':
    unittest.main()