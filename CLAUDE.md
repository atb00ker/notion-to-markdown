# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

**Testing:**

```bash
pytest
pytest --cov=./base --cov-report=xml
pytest tests/test_base.py
```

**Package Management:**

```bash
pip install -r requirements.txt
python setup.py sdist bdist_wheel
twine upload dist/*
```

## Architecture Overview

This is a Python library that converts Notion pages to Markdown format, providing both synchronous and asynchronous implementations.

### Core Components

**Main Classes:**

- `NotionToMarkdown` (sync) and `NotionToMarkdownAsync` (async) in `notion_to_markdown/base.py:468,559`
- Both inherit from `NotionToMarkdownBase` which provides shared functionality

**Key Methods:**

- `page_to_markdown()` - Converts entire Notion page to markdown blocks
- `block_to_markdown()` - Converts individual Notion blocks to markdown
- `block_list_to_markdown()` - Processes lists of blocks recursively
- `to_markdown_string()` - Converts markdown blocks to final string output

**Utilities:**

- `notion_to_markdown/utils/notion.py` - Notion API interaction helpers
- `notion_to_markdown/utils/md.py` - Markdown formatting utilities
- `notion_to_markdown/types/notion_types.py` - Type definitions

### Block Processing Architecture

The library uses a recursive approach to process Notion's nested block structure:

1. **Fetch blocks** from Notion API using `get_block_children()`
2. **Transform blocks** to markdown via `block_to_markdown()` with support for custom transformers
3. **Handle nested children** recursively for blocks with `has_children=true`
4. **Generate final output** by converting block tree to markdown strings

**Supported Block Types:**

- Text blocks: paragraph, headings (1-3), quote, code, callout
- Lists: bulleted_list_item, numbered_list_item, to_do
- Media: image, video, file, pdf
- Structure: divider, table, child_page, child_database
- Advanced: equation, bookmark, embed, toggle, synced_block

### Configuration Options

Available in constructor config dict:

- `separate_child_page: bool` - Whether to separate child pages in output
- `convert_images_to_base64: bool` - Convert images to base64 encoding
- `parse_child_pages: bool` - Whether to include child page content

### Custom Transformers

Use `set_custom_transformer(block_type, transformer_func)` to override default block processing for specific block types.
