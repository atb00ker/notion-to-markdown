import pytest
from unittest.mock import MagicMock, AsyncMock
from notion_to_markdown.utils.notion import (
    get_block_children,
    get_block_children_async,
    modify_numbered_list_object,
)


@pytest.mark.parametrize(
    "total_pages,expected_results,expected_calls",
    [
        (None, 2, 2),
        (1, 1, 1),
    ],
)
def test_get_block_children(total_pages, expected_results, expected_calls):
    mock_client = MagicMock()
    mock_client.blocks.children.list.side_effect = [
        {"results": [{"id": "1"}], "next_cursor": "cursor1"},
        {"results": [{"id": "2"}], "next_cursor": None if total_pages is None else "cursor2"},
    ]

    kwargs = {} if total_pages is None else {"total_pages": total_pages}
    results = get_block_children(mock_client, "block_id", **kwargs)

    assert len(results) == expected_results
    assert results[0]["id"] == "1"
    if expected_results == 2:
        assert results[1]["id"] == "2"
    assert mock_client.blocks.children.list.call_count == expected_calls


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "total_pages,expected_results,expected_calls",
    [
        (None, 2, 2),
        (1, 1, 1),
    ],
)
async def test_get_block_children_async(total_pages, expected_results, expected_calls):
    mock_client = AsyncMock()
    mock_client.blocks.children.list.side_effect = [
        {"results": [{"id": "1"}], "next_cursor": "cursor1"},
        {"results": [{"id": "2"}], "next_cursor": None if total_pages is None else "cursor2"},
    ]

    kwargs = {} if total_pages is None else {"total_pages": total_pages}
    results = await get_block_children_async(mock_client, "block_id", **kwargs)

    assert len(results) == expected_results
    assert results[0]["id"] == "1"
    if expected_results == 2:
        assert results[1]["id"] == "2"
    assert mock_client.blocks.children.list.call_count == expected_calls


def test_modify_numbered_list_object():
    blocks = [
        {"type": "numbered_list_item", "numbered_list_item": {}},
        {"type": "numbered_list_item", "numbered_list_item": {}},
        {"type": "paragraph"},
        {"type": "numbered_list_item", "numbered_list_item": {}},
    ]

    modify_numbered_list_object(blocks)

    assert blocks[0]["numbered_list_item"]["number"] == 1
    assert blocks[1]["numbered_list_item"]["number"] == 2
    assert blocks[3]["numbered_list_item"]["number"] == 1
