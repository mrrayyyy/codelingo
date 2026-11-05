"""Provider-independent, JSON-serializable learning plugin contracts."""
from enum import Enum
from typing import Protocol, Literal, TypedDict

from pydantic import BaseModel, Field


class Skill(str, Enum):
    reading = "reading"
    listening = "listening"
    speaking = "speaking"
    writing = "writing"
    review = "review"
    workplace = "workplace"


class Context(BaseModel):
    text: str
    file_path: str
    line_number: int
    kind: str


class Vocab(BaseModel):
    id: str
    lemma: str
    part_of_speech: str
    frequency: int
    cefr: str
    cefr_estimated: bool = True
    ipa: str | None = None
    definition: str | None = None
    tags: list[str] = Field(default_factory=list)
    rank: float = 0
    contexts: list[Context] = Field(default_factory=list)


class UserProfile(BaseModel):
    native_language: str = "vi"
    target_level: str = "B1"
    daily_goal: int = 10
    tts_voice: str = "en_US"


class PluginManifest(BaseModel):
    id: str
    version: str
    title: str
    skills: list[Skill]
    services: list[Literal["tts", "stt", "llm", "dictionary"]]


class DictationPayload(TypedDict):
    voice: str
    audio_available: bool


class DictationAnswerKey(TypedDict):
    transcript: str


class Exercise(BaseModel):
    id: str
    plugin_id: str
    vocab_id: str
    kind: str
    prompt: str
    payload: dict = Field(default_factory=dict)
    # Internal only. Public exercise serializers MUST exclude this field.
    answer_key: dict = Field(default_factory=dict)


class Answer(BaseModel):
    text: str = Field(default="", max_length=8000)


class Feedback(BaseModel):
    score: float = Field(ge=0, le=1)
    explanation: str
    corrections: list[str] = Field(default_factory=list)
    reference: str | None = None


class LearningPlugin(Protocol):
    manifest: PluginManifest

    async def generate(self, vocabulary: list[Vocab], profile: UserProfile) -> list[Exercise]: ...

    async def grade(self, exercise: Exercise, answer: Answer) -> Feedback: ...


class TTSAdapter(Protocol):
    async def synthesize(self, text: str, voice: str) -> bytes: ...


class STTAdapter(Protocol):
    async def transcribe(self, audio: bytes, filename: str) -> str: ...


class LLMAdapter(Protocol):
    async def grade_writing(self, prompt: str, answer: str) -> Feedback: ...


class DictionaryEntry(BaseModel):
    definition: str | None = None
    ipa: str | None = None
    source: str = "bundled"


class DictionaryAdapter(Protocol):
    async def lookup(self, lemma: str) -> DictionaryEntry: ...
