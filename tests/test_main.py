import pytest
from notion_to_markdown.main import MarkdownProvider
from unittest.mock import MagicMock, patch, AsyncMock


def test_get_markdown_string():
    mock_notion = MagicMock()
    mock_n2m = MagicMock()
    mock_blocks = [
        {
            "type": "paragraph",
            "paragraph": {"rich_text": [{"text": {"content": "Test content"}}]},
        }
    ]
    mock_md_result = {"parent": "# Test content"}

    with patch(
        "notion_to_markdown.main.NotionToMarkdown", return_value=mock_n2m
    ) as mock_n2m_class:
        mock_n2m.page_to_markdown.return_value = mock_blocks
        mock_n2m.to_markdown_string.return_value = mock_md_result

        provider = MarkdownProvider(mock_notion)
        result = provider.get_markdown_string("test_page_id")

        assert result == "# Test content"
        mock_n2m_class.assert_called_once_with(mock_notion)
        mock_n2m.page_to_markdown.assert_called_once_with("test_page_id")
        mock_n2m.to_markdown_string.assert_called_once_with(mock_blocks)


def test_get_markdown_string_async():
    mock_notion = MagicMock()
    mock_n2m = AsyncMock()
    mock_blocks = [
        {
            "type": "paragraph",
            "paragraph": {"rich_text": [{"text": {"content": "Test content"}}]},
        }
    ]
    mock_md_result = {"parent": "# Test content"}

    with patch(
        "notion_to_markdown.main.NotionToMarkdownAsync", return_value=mock_n2m
    ) as mock_n2m_class:
        mock_n2m.page_to_markdown.return_value = mock_blocks
        mock_n2m.to_markdown_string = MagicMock(return_value=mock_md_result)

        provider = MarkdownProvider(mock_notion)
        result = provider.get_markdown_string_async("test_page_id")

        assert result == "# Test content"
        mock_n2m_class.assert_called_once_with(mock_notion)
        mock_n2m.page_to_markdown.assert_called_once_with("test_page_id")
        mock_n2m.to_markdown_string.assert_called_once_with(mock_blocks)


def test_notion_client_none_raises_error():
    """Test that ValueError is raised when notion_client is None"""
    from notion_to_markdown import NotionToMarkdown
    with pytest.raises(ValueError, match="Notion client is not provided"):
        NotionToMarkdown(notion_client=None)
