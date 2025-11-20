import pytest
import httpx
from unittest.mock import patch, MagicMock
from notion_to_markdown.utils import md


def test_callout_without_emoji():
    text = "Call out text content."
    assert md.callout(text) == f"> {text}"


def test_callout_with_emoji():
    text = "Call out text content."
    assert (
        md.callout(
            text,
            {
                "type": "emoji",
                "emoji": "😍",
            },
        )
        == f"> 😍 {text}"
    )


def test_markdown_table():
    mock_table = [
        ["number", "char"],
        ["1", "a"],
        ["2", "b"],
    ]
    expected_output = """
| number | char |
| ------ | ---- |
| 1      | a    |
| 2      | b    |
""".strip()
    assert md.table(mock_table) == expected_output





def test_code_block():
    expected_output = """
```javascript
simple text
```
""".strip()
    assert md.code_block("simple text", "javascript") == expected_output


def test_code_block_plain_text():
    expected_output = """
```text
simple text
```
""".strip()
    assert md.code_block("simple text", "plain text") == expected_output


def test_inline_equation():
    assert md.inline_equation("E = mc^2") == "$E = mc^2$"


def test_equation_block():
    expected_output = """
$$
E = mc^2
$$
""".strip()
    assert md.equation("E = mc^2") == expected_output


@pytest.mark.parametrize(
    "func,expected",
    [
        (md.bold, "**simple text**"),
        (md.italic, "_simple text_"),
        (md.strikethrough, "~~simple text~~"),
        (md.underline, "<u>simple text</u>"),
        (md.inline_code, "`simple text`"),
    ],
)
def test_text_formatting(func, expected):
    assert func("simple text") == expected


@pytest.mark.parametrize(
    "func,expected",
    [
        (md.heading1, "# simple text"),
        (md.heading2, "## simple text"),
        (md.heading3, "### simple text"),
    ],
)
def test_headings(func, expected):
    assert func("simple text") == expected


def test_bullet():
    assert md.bullet("simple text") == "- simple text"


def test_checked_todo():
    assert md.todo("simple text", True) == "- [x] simple text"


def test_unchecked_todo():
    assert md.todo("simple text", False) == "- [ ] simple text"


@pytest.mark.asyncio
async def test_image_with_alt_text_async():
    result = await md.image_async("simple text", "https://example.com/image", False)
    assert result == "![simple text](https://example.com/image)"


def test_image_with_alt_text():
    result = md.image("simple text", "https://example.com/image", False)
    assert result == "![simple text](https://example.com/image)"


@pytest.mark.asyncio
async def test_image_to_base64_async():
    result = await md.image_async(
        "simple text", "https://w.wallhaven.cc/full/ex/wallhaven-ex9gwo.png", True
    )
    assert result.startswith(
        "![simple text](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAB4AAAAQ4CAY"
    )


def test_image_to_base64():
    result = md.image(
        "simple text", "https://w.wallhaven.cc/full/ex/wallhaven-ex9gwo.png", True
    )
    assert result.startswith(
        "![simple text](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAB4AAAAQ4CAY"
    )


def test_toggle_without_title():
    assert md.toggle(None, "content").replace(" ", "") == "content"


def test_toggle_empty_title_and_content():
    assert md.toggle(None, None).replace(" ", "") == ""


def test_toggle_with_title_and_content():
    result = md.toggle("title", "content").replace(" ", "")
    expected_output = "<details><summary>title</summary>content</details>"
    assert result == expected_output


def test_link():
    assert md.link("Example", "https://example.com") == "[Example](https://example.com)"
    assert md.link("With space", "/path/with space") == "[With space](/path/with space)"


def test_quote():
    assert md.quote("Simple quote") == "> Simple quote"
    assert md.quote("Multi\nline\nquote") == "> Multi\n> line\n> quote"


def test_add_tab_space():
    assert md.add_tab_space("text") == "text"
    assert md.add_tab_space("text", 1) == "\ttext"
    assert md.add_tab_space("line1\nline2", 2) == "\t\tline1\n\t\tline2"


def test_divider():
    assert md.divider() == "---"


def test_callout_with_heading():
    text = "# Heading"
    emoji = {"type": "emoji", "emoji": "ℹ️"}
    assert md.callout(text, emoji) == "> # ℹ️ Heading"


def test_callout_with_multiline():
    text = "Line 1\nLine 2"
    assert md.callout(text) == "> Line 1\n> Line 2"


@pytest.mark.parametrize("is_async", [False, True])
@pytest.mark.asyncio
async def test_image_error_handling(is_async):
    client_mock = "httpx.AsyncClient" if is_async else "httpx.Client"
    context_manager = "__aenter__" if is_async else "__enter__"
    image_func = md.image_async if is_async else md.image

    with patch(client_mock) as mock_client:
        mock_response = MagicMock()
        mock_response.content = b"image data"
        getattr(mock_client.return_value, context_manager).return_value.get.return_value = mock_response

        result = await image_func("alt", "https://example.com/image.png", convert_to_base64=True) if is_async else image_func("alt", "https://example.com/image.png", convert_to_base64=True)
        assert result == "![alt](data:image/png;base64,aW1hZ2UgZGF0YQ==)"

        result = await image_func("alt", "data:image/png;base64,abc123") if is_async else image_func("alt", "data:image/png;base64,abc123")
        assert result == "![alt](data:image/png;base64,abc123)"
