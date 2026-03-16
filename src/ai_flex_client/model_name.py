
# To regenerate: ask Claude to rebuild this file from the JSON data
from enum import Enum


class ModelName(str, Enum):

    # OpenAI
    GPT_5_4             = "gpt-5.4"
    GPT_5_4_PRO         = "gpt-5.4-pro"
    GPT_5               = "gpt-5-2025-08-07"
    GPT_5_MINI          = "gpt-5-mini"
    GPT_4_1             = "gpt-4.1"
    GPT_4_1_MINI        = "gpt-4.1-mini"
    GPT_4_1_NANO        = "gpt-4.1-nano"
    GPT_4O              = "gpt-4o"
    GPT_4O_MINI         = "gpt-4o-mini"
    O4_MINI             = "o4-mini"
    O3                  = "o3"
    O3_MINI             = "o3-mini"

    # Anthropic
    CLAUDE_OPUS_4_6     = "claude-opus-4-6"
    CLAUDE_SONNET_4_6   = "claude-sonnet-4-6"
    CLAUDE_HAIKU_4_5    = "claude-haiku-4-5-20251001"
    CLAUDE_OPUS_4_5     = "claude-opus-4-5-20251101"
    CLAUDE_SONNET_4_5   = "claude-sonnet-4-5-20250929"
    CLAUDE_OPUS_4_1     = "claude-opus-4-1-20250805"
    CLAUDE_SONNET_4     = "claude-sonnet-4-20250514"
    CLAUDE_OPUS_4       = "claude-opus-4-20250514"

    # Gemini
    GEMINI_3_1_PRO      = "gemini-3.1-pro-preview"
    GEMINI_3_1_FLASH_LITE = "gemini-3.1-flash-lite-preview"
    GEMINI_3_FLASH      = "gemini-3-flash-preview"
    GEMINI_2_5_PRO      = "gemini-2.5-pro"
    GEMINI_2_5_FLASH    = "gemini-2.5-flash"
    GEMINI_2_5_FLASH_LITE = "gemini-2.5-flash-lite"

    # Grok
    GROK_4_20_REASONING = "grok-4.20-beta-0309-reasoning"
    GROK_4_20           = "grok-4.20-beta-0309-non-reasoning"
    GROK_4              = "grok-4-0709"
    GROK_4_1_FAST_REASONING = "grok-4-1-fast-reasoning"
    GROK_4_1_FAST       = "grok-4-1-fast-non-reasoning"
    GROK_CODE_FAST      = "grok-code-fast-1"
    GROK_3              = "grok-3"
    GROK_3_MINI         = "grok-3-mini"

    # Venice
    VENICE_UNCENSORED   = "venice-uncensored"
    GLM_4_7             = "zai-org-glm-4.7"
    GLM_4_7_FLASH       = "zai-org-glm-4.7-flash"
    GLM_5               = "zai-org-glm-5"

    # Synthetic
    GPT_OSS_120B        = "hf:openai/gpt-oss-120b"
    LLAMA_3_3_70B       = "hf:meta-llama/Llama-3.3-70B-Instruct"
    DEEPSEEK_R1         = "hf:deepseek-ai/DeepSeek-R1-0528"
    DEEPSEEK_V3         = "hf:deepseek-ai/DeepSeek-V3"
    DEEPSEEK_V3_2       = "hf:deepseek-ai/DeepSeek-V3.2"
    QWEN3_235B_THINKING = "hf:Qwen/Qwen3-235B-A22B-Thinking-2507"
    QWEN3_CODER_480B    = "hf:Qwen/Qwen3-Coder-480B-A35B-Instruct"
    QWEN3_5_397B        = "hf:Qwen/Qwen3.5-397B-A17B"
    GLM_4_7_SYNTHETIC   = "hf:zai-org/GLM-4.7"
    GLM_4_7_FLASH_SYNTHETIC = "hf:zai-org/GLM-4.7-Flash"
    MINIMAX_M2_5        = "hf:MiniMaxAI/MiniMax-M2.5"
    KIMI_K2_5           = "hf:moonshotai/Kimi-K2.5"
