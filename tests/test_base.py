import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from notion_to_markdown import NotionToMarkdown, NotionToMarkdownAsync


def test_block_to_markdown_calls_custom_transformer():
    custom_transformer_mock = MagicMock()
    n2m = NotionToMarkdown(notion_client={})
    n2m.set_custom_transformer("test", custom_transformer_mock)

    n2m.block_to_markdown(
        {
            "id": "test",
            "name": "test",
            "type": "test",
            "test": {"foo": "bar"},
        }
    )

    custom_transformer_mock.assert_called_once_with(
        {"id": "test", "name": "test", "type": "test", "test": {"foo": "bar"}}
    )


def test_supports_only_one_custom_transformer_per_type():
    custom_transformer_mock1 = MagicMock()
    custom_transformer_mock2 = MagicMock()
    n2m = NotionToMarkdown(notion_client={})

    n2m.set_custom_transformer("test", custom_transformer_mock1)
    n2m.set_custom_transformer("test", custom_transformer_mock2)

    n2m.block_to_markdown(
        {
            "id": "test",
            "name": "test",
            "type": "test",
            "test": {"foo": "bar"},
        }
    )

    custom_transformer_mock1.assert_not_called()
    custom_transformer_mock2.assert_called_once()


def test_custom_transformer_implementation_works():
    custom_transformer_mock = MagicMock()
    custom_transformer_mock.return_value = "hello"
    n2m = NotionToMarkdown(notion_client={})
    n2m.set_custom_transformer("divider", custom_transformer_mock)

    md = n2m.block_to_markdown(
        {
            "id": "test",
            "type": "divider",
            "divider": {},
            "object": "block",
        }
    )

    assert md == "hello"


def test_custom_transformer_default_implementation_works():
    custom_transformer_mock = MagicMock()
    custom_transformer_mock.return_value = False
    n2m = NotionToMarkdown(notion_client={})
    n2m.set_custom_transformer("divider", custom_transformer_mock)

    md = n2m.block_to_markdown(
        {
            "id": "test",
            "type": "divider",
            "divider": {},
            "object": "block",
        }
    )

    assert md == "---"


@pytest.mark.asyncio
async def test_block_to_markdown_calls_custom_transformer_async():
    custom_transformer_mock = AsyncMock()
    n2m = NotionToMarkdownAsync(notion_client={})
    n2m.set_custom_transformer("test", custom_transformer_mock)

    await n2m.block_to_markdown(
        {
            "id": "test",
            "name": "test",
            "type": "test",
            "test": {"foo": "bar"},
        }
    )

    custom_transformer_mock.assert_called_once_with(
        {"id": "test", "name": "test", "type": "test", "test": {"foo": "bar"}}
    )


@pytest.mark.asyncio
async def test_supports_only_one_custom_transformer_per_type_async():
    custom_transformer_mock1 = AsyncMock()
    custom_transformer_mock2 = AsyncMock()
    n2m = NotionToMarkdownAsync(notion_client={})

    n2m.set_custom_transformer("test", custom_transformer_mock1)
    n2m.set_custom_transformer("test", custom_transformer_mock2)

    await n2m.block_to_markdown(
        {
            "id": "test",
            "name": "test",
            "type": "test",
            "test": {"foo": "bar"},
        }
    )

    custom_transformer_mock1.assert_not_called()
    custom_transformer_mock2.assert_called_once()


@pytest.mark.asyncio
async def test_custom_transformer_implementation_works_async():
    custom_transformer_mock = AsyncMock(return_value="hello")
    n2m = NotionToMarkdownAsync(notion_client={})
    n2m.set_custom_transformer("divider", custom_transformer_mock)

    md = await n2m.block_to_markdown(
        {
            "id": "test",
            "type": "divider",
            "divider": {},
            "object": "block",
        }
    )

    assert md == "hello"


@pytest.mark.asyncio
async def test_custom_transformer_default_implementation_works_async():
    custom_transformer_mock = AsyncMock()
    custom_transformer_mock.return_value = False
    n2m = NotionToMarkdownAsync(notion_client={})
    n2m.set_custom_transformer("divider", custom_transformer_mock)

    md = await n2m.block_to_markdown(
        {
            "id": "test",
            "type": "divider",
            "divider": {},
            "object": "block",
        }
    )

    assert md == "---"


def test_block_to_markdown_image():
    n2m = NotionToMarkdown(notion_client={})

    # External image
    md = n2m.block_to_markdown({
        "type": "image",
        "image": {
            "type": "external",
            "external": {"url": "https://example.com/image.png"},
            "caption": [{"plain_text": "Test Image"}]
        }
    })
    assert md == "![Test Image](https://example.com/image.png)"

    # File image
    md = n2m.block_to_markdown({
        "type": "image",
        "image": {
            "type": "file",
            "file": {"url": "https://example.com/image.png"},
            "caption": []
        }
    })
    assert md == "![image.png](https://example.com/image.png)"


def test_block_to_markdown_divider():
    n2m = NotionToMarkdown(notion_client={})
    md = n2m.block_to_markdown({"type": "divider", "divider": {}})
    assert md == "---"


def test_block_to_markdown_equation():
    n2m = NotionToMarkdown(notion_client={})
    md = n2m.block_to_markdown({
        "type": "equation",
        "equation": {"expression": "E=mc^2"}
    })
    assert md == "$$\nE=mc^2\n$$"


def test_block_to_markdown_files():
    n2m = NotionToMarkdown(notion_client={})

    # Video
    md = n2m.block_to_markdown({
        "type": "video",
        "video": {
            "type": "external",
            "external": {"url": "https://example.com/video.mp4"},
            "caption": [{"plain_text": "Test Video"}]
        }
    })
    assert md == "[Test Video](https://example.com/video.mp4)"

    # File
    md = n2m.block_to_markdown({
        "type": "file",
        "file": {
            "type": "file",
            "file": {"url": "https://example.com/file.pdf"},
            "caption": []
        }
    })
    assert md == "[file.pdf](https://example.com/file.pdf)"


def test_block_to_markdown_links():
    n2m = NotionToMarkdown(notion_client={})

    # Bookmark
    md = n2m.block_to_markdown({
        "type": "bookmark",
        "bookmark": {"url": "https://example.com"}
    })
    assert md == "[bookmark](https://example.com)"

    # Link to page
    md = n2m.block_to_markdown({
        "type": "link_to_page",
        "link_to_page": {"type": "page_id", "page_id": "123"}
    })
    assert md == "[link_to_page](https://www.notion.so/123)"

    md = n2m.block_to_markdown({
        "type": "link_to_page",
        "link_to_page": {"type": "database_id", "database_id": "456"}
    })
    assert md == "[link_to_page](https://www.notion.so/456)"


def test_block_to_markdown_child_page():
    n2m = NotionToMarkdown(notion_client={}, config={"parse_child_pages": True})

    # Default config
    md = n2m.block_to_markdown({
        "type": "child_page",
        "child_page": {"title": "Child Page"}
    })
    assert md == "## Child Page"

    # Separate child page config
    n2m.config["separate_child_page"] = True
    md = n2m.block_to_markdown({
        "type": "child_page",
        "child_page": {"title": "Child Page"}
    })
    assert md == "Child Page"

    # Parse child pages disabled
    n2m.config["parse_child_pages"] = False
    md = n2m.block_to_markdown({
        "type": "child_page",
        "child_page": {"title": "Child Page"}
    })
    assert md == ""


def test_sync_missing_coverage():
    mock_client = MagicMock()
    n2m = NotionToMarkdown(notion_client=mock_client)

    assert n2m.to_markdown_string([]) == {}

    assert n2m.block_to_markdown(None) == ""
    assert n2m.block_to_markdown({}) == ""

    assert n2m.block_to_markdown({
        "type": "heading_2",
        "heading_2": {"rich_text": [{"plain_text": "H2", "annotations": {}}]}
    }) == "## H2"
    assert n2m.block_to_markdown({
        "type": "heading_3",
        "heading_3": {"rich_text": [{"plain_text": "H3", "annotations": {}}]}
    }) == "### H3"

    assert n2m.block_list_to_markdown([]) == []
    assert n2m.block_list_to_markdown([{"type": "unsupported"}]) == []

    mock_client.blocks.children.list.return_value = {
        "results": [
            {
                "type": "paragraph",
                "id": "child_para",
                "paragraph": {"rich_text": [{"plain_text": "Child Content"}]}
            }
        ],
        "next_cursor": None
    }

    blocks = [{
        "type": "child_page",
        "id": "child_page_id",
        "has_children": True,
        "parent": "Child Page Title",
        "child_page": {"title": "Child Page Title"}
    }]

    md_blocks = n2m.block_list_to_markdown(blocks)
    result = n2m.to_markdown_string(md_blocks)
    assert "Child Page Title" in result.get("parent", "")
    assert "Child Content" in result.get("parent", "")

    mock_client.blocks.children.list.return_value = {"results": [], "next_cursor": None}
    n2m.page_to_markdown("page_id")


@pytest.mark.asyncio
async def test_async_missing_coverage():
    mock_client = AsyncMock()
    n2m = NotionToMarkdownAsync(notion_client=mock_client)

    mock_client.blocks.children.list.return_value = {"results": [], "next_cursor": None}
    await n2m.page_to_markdown("page_id")

    assert await n2m.block_list_to_markdown([]) == []

    assert await n2m.block_list_to_markdown([{"type": "unsupported"}]) == []

    assert await n2m.block_to_markdown(None) == ""
    assert await n2m.block_to_markdown({}) == ""

    assert await n2m.block_to_markdown({
        "type": "equation",
        "equation": {"expression": "x=y"}
    }) == "$$\nx=y\n$$"

    assert await n2m.block_to_markdown({
        "type": "bookmark",
        "bookmark": {"url": "https://example.com"}
    }) == "[bookmark](https://example.com)"

    assert await n2m.block_to_markdown({
        "type": "link_to_page",
        "link_to_page": {"type": "page_id", "page_id": "123"}
    }) == "[link_to_page](https://www.notion.so/123)"

    assert await n2m.block_to_markdown({
        "type": "link_to_page",
        "link_to_page": {"type": "database_id", "database_id": "456"}
    }) == "[link_to_page](https://www.notion.so/456)"

    assert await n2m.block_to_markdown({
        "type": "child_page",
        "child_page": {"title": "Async Child"}
    }) == "## Async Child"

    assert await n2m.block_to_markdown({
        "type": "child_database",
        "child_database": {"title": "Async DB"}
    }) == "## Async DB"

    assert await n2m.block_to_markdown({
        "type": "code",
        "code": {"language": "python", "rich_text": [{"plain_text": "print()"}]}
    }) == "```python\nprint()\n```"

    assert await n2m.block_to_markdown({
        "type": "heading_1",
        "heading_1": {"rich_text": [{"plain_text": "H1"}]}
    }) == "# H1"

    assert await n2m.block_to_markdown({
        "type": "callout",
        "has_children": False,
        "callout": {"icon": {"emoji": "x", "type": "emoji"}, "rich_text": [{"plain_text": "Callout"}]}
    }) == "> x "

    assert await n2m.block_to_markdown({
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": [{"plain_text": "Bullet"}]}
    }) == "- Bullet"

    assert await n2m.block_to_markdown({
        "type": "numbered_list_item",
        "numbered_list_item": {"rich_text": [{"plain_text": "Number"}], "number": 1}
    }) == "1. Number"

    assert await n2m.block_to_markdown({
        "type": "to_do",
        "to_do": {"rich_text": [{"plain_text": "Todo"}], "checked": True}
    }) == "- [x] Todo"


@pytest.mark.asyncio
async def test_async_child_page_configs():
    mock_client = AsyncMock()

    n2m_no_parse = NotionToMarkdownAsync(notion_client=mock_client, config={"parse_child_pages": False})
    assert await n2m_no_parse.block_to_markdown({
        "type": "child_page",
        "child_page": {"title": "Skip Me"}
    }) == ""

    n2m_separate = NotionToMarkdownAsync(notion_client=mock_client, config={"separate_child_page": True})
    assert await n2m_separate.block_to_markdown({
        "type": "child_page",
        "child_page": {"title": "Separate Me"}
    }) == "Separate Me"


def test_nested_parent_key_logic():
    mock_client = MagicMock()
    n2m = NotionToMarkdown(notion_client=mock_client)

    original_to_markdown = n2m.to_markdown_string

    def side_effect(md_blocks=None, page_identifier="parent", nesting_level=0):
        if page_identifier == "Child Page" and nesting_level > 0:
            return {"parent": "Nested Parent Content"}
        return original_to_markdown(md_blocks, page_identifier, nesting_level)

    with patch.object(n2m, 'to_markdown_string', side_effect=side_effect):
        input_blocks = [{
            "type": "child_page",
            "parent": "Child Page",
            "children": [
                {
                    "type": "paragraph",
                    "parent": "Para",
                    "children": [{"type": "paragraph"}]
                }
            ]
        }]

        n2m.config = {"separate_child_page": False, "parse_child_pages": True}
        result = n2m.to_markdown_string(input_blocks)
        assert "Nested Parent Content" in result.get("parent", "")


@pytest.mark.asyncio
async def test_async_table_coverage():
    mock_client = AsyncMock()

    mock_client.blocks.children.list.return_value = {
        "results": [
            {
                "type": "table_row",
                "table_row": {"cells": [[{"plain_text": "Cell1"}], [{"plain_text": "Cell2"}]]}
            }
        ],
        "next_cursor": None
    }

    n2m = NotionToMarkdownAsync(notion_client=mock_client)
    md = await n2m.block_to_markdown({
        "type": "table",
        "id": "table_id",
        "has_children": True,
        "table": {}
    })

    assert "Cell1" in md and "Cell2" in md


@pytest.mark.asyncio
async def test_async_recursion_coverage():
    mock_client = AsyncMock()

    mock_client.blocks.children.list.return_value = {
        "results": [
            {
                "type": "paragraph",
                "id": "child_para",
                "paragraph": {"rich_text": [{"plain_text": "Synced Content"}]}
            }
        ],
        "next_cursor": None
    }

    n2m = NotionToMarkdownAsync(notion_client=mock_client)
    blocks = [{
        "type": "synced_block",
        "id": "synced_id",
        "has_children": True,
        "synced_block": {
            "synced_from": {"block_id": "origin_id"}
        }
    }]

    md_blocks = await n2m.block_list_to_markdown(blocks)
    assert len(md_blocks[0]["children"]) > 0
    assert md_blocks[0]["children"][0]["parent"] == "Synced Content"


@pytest.mark.asyncio
async def test_text_annotations_async():
    n2m = NotionToMarkdownAsync(notion_client={})


    md = await n2m.block_to_markdown({
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{
                "plain_text": "Bold italic",
                "annotations": {"bold": True, "italic": True}
            }]
        }
    })
    assert "**" in md and "_" in md


@pytest.mark.asyncio
async def test_inline_equation_async():
    n2m = NotionToMarkdownAsync(notion_client={})
    md = await n2m.block_to_markdown({
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {"type": "equation", "equation": {"expression": "x^2"}}
            ]
        }
    })
    assert "$x^2$" in md


@pytest.mark.asyncio
async def test_link_in_text_async():
    n2m = NotionToMarkdownAsync(notion_client={})
    md = await n2m.block_to_markdown({
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{
                "plain_text": "Link",
                "annotations": {},
                "href": "https://test.com"
            }]
        }
    })
    assert "[Link](https://test.com)" in md


@pytest.mark.asyncio
async def test_pdf_block_async():
    n2m = NotionToMarkdownAsync(notion_client={})
    md = await n2m.block_to_markdown({
        "type": "pdf",
        "pdf": {
            "type": "external",
            "external": {"url": "https://example.com/doc.pdf"},
            "caption": []
        }
    })
    assert "doc.pdf" in md


@pytest.mark.asyncio
async def test_heading_blocks_async():
    n2m = NotionToMarkdownAsync(notion_client={})

    md = await n2m.block_to_markdown({
        "type": "heading_2",
        "heading_2": {"rich_text": [{"plain_text": "Heading 2", "annotations": {}}]}
    })
    assert md == "## Heading 2"

    md = await n2m.block_to_markdown({
        "type": "heading_3",
        "heading_3": {"rich_text": [{"plain_text": "Heading 3", "annotations": {}}]}
    })
    assert md == "### Heading 3"


@pytest.mark.asyncio
async def test_quote_async():
    n2m = NotionToMarkdownAsync(notion_client={})
    md = await n2m.block_to_markdown({
        "type": "quote",
        "quote": {"rich_text": [{"plain_text": "Quote text", "annotations": {}}]}
    })
    assert md == "> Quote text"


def test_block_to_markdown_child_database():
    n2m = NotionToMarkdown(notion_client={})
    md = n2m.block_to_markdown({
        "type": "child_database",
        "child_database": {"title": "Database"}
    })
    assert md == "## Database"


def test_block_to_markdown_table():
    mock_client = MagicMock()
    mock_client.blocks.children.list.return_value = {
        "results": [
            {
                "type": "table_row",
                "table_row": {
                    "cells": [
                        [{"plain_text": "Header 1", "annotations": {}}],
                        [{"plain_text": "Header 2", "annotations": {}}]
                    ]
                }
            },
            {
                "type": "table_row",
                "table_row": {
                    "cells": [
                        [{"plain_text": "Cell 1", "annotations": {}}],
                        [{"plain_text": "Cell 2", "annotations": {}}]
                    ]
                }
            }
        ],
        "next_cursor": None
    }

    n2m = NotionToMarkdown(notion_client=mock_client)
    md = n2m.block_to_markdown({
        "id": "table_id",
        "type": "table",
        "has_children": True
    })

    assert "| Header 1 | Header 2 |" in md
    assert "Cell 1" in md and "Cell 2" in md


def test_block_to_markdown_text_blocks():
    n2m = NotionToMarkdown(notion_client={})

    md = n2m.block_to_markdown({
        "type": "paragraph",
        "paragraph": {"rich_text": [{"plain_text": "Hello", "annotations": {}}]}
    })
    assert md == "Hello"

    md = n2m.block_to_markdown({
        "type": "heading_1",
        "heading_1": {"rich_text": [{"plain_text": "Heading 1", "annotations": {}}]}
    })
    assert md == "# Heading 1"

    md = n2m.block_to_markdown({
        "type": "code",
        "code": {
            "language": "python",
            "rich_text": [{"plain_text": "print('hi')", "annotations": {}}]
        }
    })
    assert md == "```python\nprint('hi')\n```"

    md = n2m.block_to_markdown({
        "type": "quote",
        "quote": {"rich_text": [{"plain_text": "Quote", "annotations": {}}]}
    })
    assert md == "> Quote"

    md = n2m.block_to_markdown({
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": [{"plain_text": "Item", "annotations": {}}]}
    })
    assert md == "- Item"

    md = n2m.block_to_markdown({
        "type": "numbered_list_item",
        "numbered_list_item": {
            "rich_text": [{"plain_text": "Item", "annotations": {}}],
            "number": 1
        }
    })
    assert md == "1. Item"

    md = n2m.block_to_markdown({
        "type": "to_do",
        "to_do": {
            "rich_text": [{"plain_text": "Task", "annotations": {}}],
            "checked": True
        }
    })
    assert md == "- [x] Task"


def test_block_to_markdown_callout():
    n2m = NotionToMarkdown(notion_client={})

    md = n2m.block_to_markdown({
        "id": "callout_id",
        "type": "callout",
        "has_children": False,
        "callout": {
            "rich_text": [{"plain_text": "Callout", "annotations": {}}],
            "icon": {"emoji": "💡", "type": "emoji"}
        }
    })
    assert md == "> 💡 "


@pytest.mark.asyncio
async def test_custom_transformer_default_implementation_works_async():
    custom_transformer_mock = AsyncMock()
    custom_transformer_mock.return_value = False
    n2m = NotionToMarkdownAsync(notion_client={})
    n2m.set_custom_transformer("divider", custom_transformer_mock)

    md = await n2m.block_to_markdown(
        {
            "id": "test",
            "type": "divider",
            "divider": {},
            "object": "block",
        }
    )

    assert md == "---"


@pytest.mark.asyncio
async def test_block_to_markdown_async_types():
    n2m = NotionToMarkdownAsync(notion_client={})

    # Image
    md = await n2m.block_to_markdown({
        "type": "image",
        "image": {
            "type": "external",
            "external": {"url": "https://example.com/image.png"},
            "caption": []
        }
    })
    assert md == "![image.png](https://example.com/image.png)"

    # Divider
    md = await n2m.block_to_markdown({"type": "divider", "divider": {}})
    assert md == "---"


    # Paragraph
    md = await n2m.block_to_markdown({
        "type": "paragraph",
        "paragraph": {"rich_text": [{"plain_text": "Hello", "annotations": {}}]}
    })
    assert md == "Hello"


def test_callout_with_children():
    mock_client = MagicMock()
    mock_client.blocks.children.list.return_value = {
        "results": [
            {
                "type": "paragraph",
                "paragraph": {"rich_text": [{"plain_text": "Child content", "annotations": {}}]},
                "id": "child1",
                "has_children": False
            }
        ],
        "next_cursor": None
    }

    n2m = NotionToMarkdown(notion_client=mock_client)
    md = n2m.block_to_markdown({
        "id": "callout_id",
        "type": "callout",
        "has_children": True,
        "callout": {
            "rich_text": [{"plain_text": "Callout text", "annotations": {}}],
            "icon": {"emoji": "💡", "type": "emoji"}
        }
    })

    assert "💡" in md
    assert "Child content" in md


@pytest.mark.asyncio
async def test_callout_with_children_async():
    mock_client = AsyncMock()
    mock_client.blocks.children.list.return_value = {
        "results": [
            {
                "type": "paragraph",
                "paragraph": {"rich_text": [{"plain_text": "Child content", "annotations": {}}]},
                "id": "child1",
                "has_children": False
            }
        ],
        "next_cursor": None
    }

    n2m = NotionToMarkdownAsync(notion_client=mock_client)
    md = await n2m.block_to_markdown({
        "id": "callout_id",
        "type": "callout",
        "has_children": True,
        "callout": {
            "rich_text": [{"plain_text": "Callout text", "annotations": {}}],
            "icon": {"emoji": "💡", "type": "emoji"}
        }
    })

    assert "💡" in md
    assert "Child content" in md


def test_toggle_block():
    mock_client = MagicMock()
    mock_client.blocks.children.list.return_value = {
        "results": [
            {
                "type": "paragraph",
                "paragraph": {"rich_text": [{"plain_text": "Hidden content", "annotations": {}}]},
                "id": "child1",
                "has_children": False
            }
        ],
        "next_cursor": None
    }

    n2m = NotionToMarkdown(notion_client=mock_client)
    blocks = [{
        "id": "toggle_id",
        "type": "toggle",
        "has_children": True,
        "toggle": {
            "rich_text": [{"plain_text": "Toggle summary", "annotations": {}}]
        }
    }]

    md_blocks = n2m.block_list_to_markdown(blocks)
    md_string = n2m.to_markdown_string(md_blocks)

    assert "Toggle summary" in md_string.get("parent", "")
    assert "Hidden content" in md_string.get("parent", "")


def test_column_list_and_column():
    mock_client = MagicMock()

    def mock_list_side_effect(block_id, page_size=None, **kwargs):
        if block_id == "column_list_id":
            return {
                "results": [
                    {
                        "type": "column",
                        "id": "column1",
                        "has_children": True,
                        "column": {}
                    }
                ],
                "next_cursor": None
            }
        elif block_id == "column1":
            return {
                "results": [
                    {
                        "type": "paragraph",
                        "paragraph": {"rich_text": [{"plain_text": "Column content", "annotations": {}}]},
                        "id": "para1",
                        "has_children": False
                    }
                ],
                "next_cursor": None
            }
        return {"results": [], "next_cursor": None}

    mock_client.blocks.children.list.side_effect = mock_list_side_effect

    n2m = NotionToMarkdown(notion_client=mock_client)
    blocks = [{
        "id": "column_list_id",
        "type": "column_list",
        "has_children": True,
        "column_list": {}
    }]

    md_blocks = n2m.block_list_to_markdown(blocks)
    md_string = n2m.to_markdown_string(md_blocks)

    assert "Column content" in md_string.get("parent", "")


def test_synced_block():
    mock_client = MagicMock()

    def mock_list_side_effect(block_id, page_size=None, **kwargs):
        if block_id == "original_block_id":
            return {
                "results": [
                    {
                        "type": "paragraph",
                        "paragraph": {"rich_text": [{"plain_text": "Synced content", "annotations": {}}]},
                        "id": "para1",
                        "has_children": False
                    }
                ],
                "next_cursor": None
            }
        return {"results": [], "next_cursor": None}

    mock_client.blocks.children.list.side_effect = mock_list_side_effect

    n2m = NotionToMarkdown(notion_client=mock_client)
    blocks = [{
        "id": "synced_id",
        "type": "synced_block",
        "has_children": True,
        "synced_block": {
            "synced_from": {
                "block_id": "original_block_id"
            }
        }
    }]

    md_blocks = n2m.block_list_to_markdown(blocks)
    md_string = n2m.to_markdown_string(md_blocks)

    assert "Synced content" in md_string.get("parent", "")


def test_template_block():
    n2m = NotionToMarkdown(notion_client={})
    md = n2m.block_to_markdown({
        "type": "template",
        "template": {
            "rich_text": [{"plain_text": "Template text", "annotations": {}}]
        }
    })
    assert md == "Template text"


@pytest.mark.parametrize(
    "annotation,text,expected",
    [
        ({"bold": True}, "Bold text", "**Bold text**"),
        ({"italic": True}, "Italic text", "_Italic text_"),
        ({"strikethrough": True}, "Strike", "~~Strike~~"),
        ({"underline": True}, "Underline", "<u>Underline</u>"),
        ({"code": True}, "code", "`code`"),
    ],
)
def test_text_annotations(annotation, text, expected):
    n2m = NotionToMarkdown(notion_client={})
    md = n2m.block_to_markdown({
        "type": "paragraph",
        "paragraph": {"rich_text": [{"plain_text": text, "annotations": annotation}]}
    })
    assert md == expected


def test_inline_equation():
    n2m = NotionToMarkdown(notion_client={})
    md = n2m.block_to_markdown({
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {"plain_text": "Text with ", "annotations": {}},
                {"type": "equation", "equation": {"expression": "E=mc^2"}},
                {"plain_text": " equation", "annotations": {}}
            ]
        }
    })
    assert "$E=mc^2$" in md


def test_link_in_text():
    n2m = NotionToMarkdown(notion_client={})
    md = n2m.block_to_markdown({
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{
                "plain_text": "Click here",
                "annotations": {},
                "href": "https://example.com"
            }]
        }
    })
    assert md == "[Click here](https://example.com)"


def test_child_page_with_separate_config():
    mock_client = MagicMock()
    mock_client.blocks.children.list.return_value = {
        "results": [
            {
                "type": "paragraph",
                "paragraph": {"rich_text": [{"plain_text": "Child content", "annotations": {}}]},
                "id": "child1",
                "has_children": False
            }
        ],
        "next_cursor": None
    }

    n2m = NotionToMarkdown(notion_client=mock_client, config={"separate_child_page": True})
    blocks = [{
        "id": "child_page_id",
        "type": "child_page",
        "has_children": True,
        "child_page": {"title": "My Page"}
    }]

    md_blocks = n2m.block_list_to_markdown(blocks)
    md_string = n2m.to_markdown_string(md_blocks)

    assert "My Page" in md_string


def test_quote_with_children():
    mock_client = MagicMock()
    mock_client.blocks.children.list.return_value = {
        "results": [
            {
                "type": "paragraph",
                "paragraph": {"rich_text": [{"plain_text": "Nested content", "annotations": {}}]},
                "id": "child1",
                "has_children": False
            }
        ],
        "next_cursor": None
    }

    n2m = NotionToMarkdown(notion_client=mock_client)
    blocks = [{
        "id": "quote_id",
        "type": "quote",
        "has_children": True,
        "quote": {"rich_text": [{"plain_text": "Quote text", "annotations": {}}]}
    }]

    md_blocks = n2m.block_list_to_markdown(blocks)
    md_string = n2m.to_markdown_string(md_blocks)

    assert "Quote text" in md_string.get("parent", "")
    assert "Nested content" in md_string.get("parent", "")


def test_bulleted_list_with_children():
    mock_client = MagicMock()
    mock_client.blocks.children.list.return_value = {
        "results": [
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"plain_text": "Sub-item", "annotations": {}}]},
                "id": "child1",
                "has_children": False
            }
        ],
        "next_cursor": None
    }

    n2m = NotionToMarkdown(notion_client=mock_client)
    blocks = [{
        "id": "list_id",
        "type": "bulleted_list_item",
        "has_children": True,
        "bulleted_list_item": {"rich_text": [{"plain_text": "Main item", "annotations": {}}]}
    }]

    md_blocks = n2m.block_list_to_markdown(blocks)
    md_string = n2m.to_markdown_string(md_blocks)

    assert "Main item" in md_string.get("parent", "")
    assert "Sub-item" in md_string.get("parent", "")


def test_numbered_list_with_children():
    mock_client = MagicMock()
    mock_client.blocks.children.list.return_value = {
        "results": [
            {
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [{"plain_text": "Sub-item", "annotations": {}}],
                    "number": 1
                },
                "id": "child1",
                "has_children": False
            }
        ],
        "next_cursor": None
    }

    n2m = NotionToMarkdown(notion_client=mock_client)
    blocks = [{
        "id": "list_id",
        "type": "numbered_list_item",
        "has_children": True,
        "numbered_list_item": {
            "rich_text": [{"plain_text": "Main item", "annotations": {}}],
            "number": 1
        }
    }]

    md_blocks = n2m.block_list_to_markdown(blocks)
    md_string = n2m.to_markdown_string(md_blocks)

    assert "Main item" in md_string.get("parent", "")
    assert "Sub-item" in md_string.get("parent", "")


def test_to_do_with_children():
    mock_client = MagicMock()
    mock_client.blocks.children.list.return_value = {
        "results": [
            {
                "type": "paragraph",
                "paragraph": {"rich_text": [{"plain_text": "Details", "annotations": {}}]},
                "id": "child1",
                "has_children": False
            }
        ],
        "next_cursor": None
    }

    n2m = NotionToMarkdown(notion_client=mock_client)
    blocks = [{
        "id": "todo_id",
        "type": "to_do",
        "has_children": True,
        "to_do": {
            "rich_text": [{"plain_text": "Task", "annotations": {}}],
            "checked": False
        }
    }]

    md_blocks = n2m.block_list_to_markdown(blocks)
    md_string = n2m.to_markdown_string(md_blocks)

    assert "Task" in md_string.get("parent", "")
    assert "Details" in md_string.get("parent", "")


def test_pdf_block():
    n2m = NotionToMarkdown(notion_client={})
    md = n2m.block_to_markdown({
        "type": "pdf",
        "pdf": {
            "type": "file",
            "file": {"url": "https://example.com/doc.pdf"},
            "caption": [{"plain_text": "PDF Document"}]
        }
    })
    assert "PDF Document" in md
    assert "https://example.com/doc.pdf" in md


def test_embed_block():
    n2m = NotionToMarkdown(notion_client={})
    md = n2m.block_to_markdown({
        "type": "embed",
        "embed": {"url": "https://example.com/embed"}
    })
    assert md == "[embed](https://example.com/embed)"


def test_link_preview_block():
    n2m = NotionToMarkdown(notion_client={})
    md = n2m.block_to_markdown({
        "type": "link_preview",
        "link_preview": {"url": "https://example.com"}
    })
    assert md == "[link_preview](https://example.com)"


def test_whitespace_only_annotation():
    n2m = NotionToMarkdown(notion_client={})
    md = n2m.block_to_markdown({
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{
                "plain_text": "   ",
                "annotations": {"bold": True}
            }]
        }
    })
    assert md == "   "
