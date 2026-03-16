
# Enum names must match the enum_name fields in data/llm_models.json
from enum import Enum, auto


class ModelName(Enum):

    # OpenAI
    GPT_5_4             = auto()
    GPT_5_4_PRO         = auto()
    GPT_5               = auto()
    GPT_5_MINI          = auto()
    GPT_4_1             = auto()
    GPT_4_1_MINI        = auto()
    GPT_4_1_NANO        = auto()
    GPT_4O              = auto()
    GPT_4O_MINI         = auto()
    O4_MINI             = auto()
    O3                  = auto()
    O3_MINI             = auto()

    # Anthropic
    CLAUDE_OPUS_4_6     = auto()
    CLAUDE_SONNET_4_6   = auto()
    CLAUDE_HAIKU_4_5    = auto()
    CLAUDE_OPUS_4_5     = auto()
    CLAUDE_SONNET_4_5   = auto()
    CLAUDE_OPUS_4_1     = auto()
    CLAUDE_SONNET_4     = auto()
    CLAUDE_OPUS_4       = auto()

    # Gemini
    GEMINI_3_1_PRO      = auto()
    GEMINI_3_1_FLASH_LITE = auto()
    GEMINI_3_FLASH      = auto()
    GEMINI_2_5_PRO      = auto()
    GEMINI_2_5_FLASH    = auto()
    GEMINI_2_5_FLASH_LITE = auto()

    # Grok
    GROK_4_20_REASONING = auto()
    GROK_4_20           = auto()
    GROK_4              = auto()
    GROK_4_1_FAST_REASONING = auto()
    GROK_4_1_FAST       = auto()
    GROK_CODE_FAST      = auto()
    GROK_3              = auto()
    GROK_3_MINI         = auto()

    # Venice
    VENICE_UNCENSORED   = auto()
    GLM_4_7             = auto()
    GLM_4_7_FLASH       = auto()
    GLM_5               = auto()

    # Synthetic
    GPT_OSS_120B        = auto()
    LLAMA_3_3_70B       = auto()
    DEEPSEEK_R1         = auto()
    DEEPSEEK_V3         = auto()
    DEEPSEEK_V3_2       = auto()
    QWEN3_235B_THINKING = auto()
    QWEN3_CODER_480B    = auto()
    QWEN3_5_397B        = auto()
    GLM_4_7_SYNTHETIC   = auto()
    GLM_4_7_FLASH_SYNTHETIC = auto()
    MINIMAX_M2_5        = auto()
    KIMI_K2_5           = auto()

    @property
    def code(self):
        from . import utility as UTIL
        return UTIL.get_registry().lookup_by_enum_name(self.name)
