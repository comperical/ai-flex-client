# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**ai-flex-client** is a Python library providing a unified interface for multiple LLM APIs. It allows transparent swapping between providers (OpenAI, Anthropic, Google Gemini, Grok, Venice.AI, HuggingFace/Synthetic) through a common BaseQuery/DataWrapper abstraction.

## Commands

```bash
# Install in development mode
pip install -e .

# Run integration tests (requires API keys in environment)
python -m ai_flex_client.test_all
```

There is no linter, formatter, or unit test framework configured. Tests are integration tests that make real API calls.

## Architecture

The codebase follows a plugin pattern with two abstract base classes:

- **BaseQuery** (`base_query.py`) — Represents a query to an LLM. Subclasses override `_sub_run_query()` to call provider APIs and `normalize_response()` to convert responses to a standard dict format. Provides fluent builder methods (`set_simple_prompt()`, `set_small_tier()`, etc.) and serialization via `to_dict()`/`from_dict()`.

- **DataWrapper** (`data_wrapper.py`) — Wraps normalized responses for standardized data access: text extraction (`get_basic_text()`), token usage, and cost calculation (`get_cost_dollar()`). Each provider subclass defines its own pricing in `get_cost_pair()`.

**Provider implementations** (`*_impl.py`) each export: `register_api_key()`, `opt_register()`, `is_configured()`, `build_query()`, and `get_client()`. Some providers reuse others' base classes (Grok extends Anthropic's classes; Venice and Synthetic extend OpenAI's).

**Routing** — `utility.lookup_implementation(modelcode)` is the factory that maps model code strings (e.g., "claude-*", "gpt*", "gemini*") to the appropriate Query subclass.

## Environment Variables

Each provider uses its own API key env var: `OPENAI_API_KEY`, `ANTHRO_API_KEY`, `GEMINI_API_KEY`, `GROK_API_KEY`, `VENICE_API_KEY`, `SYNTHETIC_API_KEY`.

## Key Conventions

- API clients are cached via `@functools.lru_cache` on `get_client()` functions
- All provider implementations follow the same module-level structure: global `_API_KEY`, register/configure functions, Query subclass, DataWrapper subclass
- Model tiers (small/medium/large) map to provider-specific model codes within each implementation
- No pip dependencies are declared in pyproject.toml; provider SDKs (openai, anthropic, google-genai) must be installed separately
