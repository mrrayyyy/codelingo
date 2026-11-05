"""Bounded, non-executing source-to-vocabulary extraction.

Run: python -m app.extraction ./tests/fixtures/sample_repo
"""
from __future__ import annotations

import json
import math
import re
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterator

import spacy
from langdetect import DetectorFactory, LangDetectException, detect
from tree_sitter import Language, Parser
from wordfreq import zipf_frequency

from .contracts import Context, Vocab
from .lexicon import A1_WORDS, KEYWORDS, LEXICON, TOPICS

DetectorFactory.seed = 0
SKIP_DIRS = {"node_modules", ".git", "vendor", "dist", "build", ".next", ".venv", "venv", "__pycache__", "coverage", "__snapshots__"}
SUFFIXES = {".ts", ".tsx", ".js", ".jsx", ".py", ".java", ".go", ".md", ".mdx"}
SECRET = re.compile(
    r"(?:password|passwd|secret|api[_-]?key|access[_-]?token|authorization)\s*[:=]\s*\S+"
    r"|\b(?:AKIA|ASIA)[A-Z0-9]{16}\b|\b(?:gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9_-]{16,})"
    r"|-----BEGIN .*PRIVATE KEY|\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+"
    r"|\b[a-fA-F0-9]{32,}\b|://[^\s/:]+:[^\s/@]+@", re.I,
)
WORD = re.compile(r"[A-Za-z]+(?:'[a-z]+)?")


def split_identifier(value: str) -> list[str]:
    value = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", value)
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", value)
    return [part.lower() for part in re.findall(r"[A-Za-z]+", value)]


@lru_cache(maxsize=1)
def nlp_model():
    try:
        return spacy.load("en_core_web_sm", disable=["ner"])
    except OSError as exc:
        raise RuntimeError("Install the English model: python -m spacy download en_core_web_sm") from exc


@lru_cache(maxsize=8)
def parser_for(suffix: str) -> Parser:
    import tree_sitter_python as py
    import tree_sitter_typescript as ts
    import tree_sitter_javascript as js
    import tree_sitter_java as java
    import tree_sitter_go as go

    languages = {".py": py.language, ".ts": ts.language_typescript, ".tsx": ts.language_tsx,
                 ".js": js.language, ".jsx": js.language, ".java": java.language, ".go": go.language}
    return Parser(Language(languages[suffix]()))


@dataclass(frozen=True)
class Snippet:
    text: str
    file_path: str
    line_number: int
    kind: str


def safe_path(path: str) -> bool:
    parts = Path(path).parts
    return not any(p in SKIP_DIRS or p.startswith(".") for p in parts) and not any(
        token in Path(path).name.lower() for token in ("lock.", ".lock", "secret", "credential", ".min.", ".map")
    )


def snippets(source: str, path: str) -> Iterator[Snippet]:
    """Yield text fragments with exact 1-based source references; never execute code."""
    if not safe_path(path):
        return
    suffix = Path(path).suffix.lower()
    if suffix in {".md", ".mdx"}:
        fence = False
        for line, text in enumerate(source.splitlines(), 1):
            if re.match(r"\s*(```|~~~)", text):
                fence = not fence
            elif not fence and text.strip() and not text.lstrip().startswith(("import ", "export ", "<", "![[", "![")):
                yield Snippet(text.strip(), path, line, "markdown")
        return
    if suffix not in SUFFIXES:
        return
    raw = source.encode("utf-8")
    tree = parser_for(suffix).parse(raw)
    stack = [tree.root_node]
    while stack:
        node = stack.pop()
        text = raw[node.start_byte:node.end_byte].decode("utf-8", errors="replace")
        if "comment" in node.type or node.type in {"string", "string_literal", "interpreted_string_literal", "raw_string_literal", "template_string"}:
            # Interpolated strings contain code; exclude instead of retaining it.
            if "${" in text or (suffix == ".py" and re.match(r"[rbu]*f", text, re.I)):
                continue
            for offset, line in enumerate(text.splitlines()):
                clean = re.sub(r"^\s*(?://+|/\*+|\*+/?|#+)\s?", "", line)
                clean = re.sub(r"\*/\s*$", "", clean)
                clean = re.sub(r"^[rRuUbB]*(?:\"\"\"|'''|[\"'`])", "", clean)
                clean = re.sub(r"(?:\"\"\"|'''|[\"'`])$", "", clean).strip()
                if clean:
                    yield Snippet(clean, path, node.start_point.row + offset + 1, "comment" if "comment" in node.type else "string")
            continue
        if node.type in {"identifier", "property_identifier", "type_identifier", "field_identifier"}:
            if len(text) <= 100:
                yield Snippet(text, path, node.start_point.row + 1, "identifier")
            continue
        stack.extend(reversed(node.children))


def is_english_prose(text: str) -> bool:
    if len(text) > 600 or SECRET.search(text):
        return False
    words = WORD.findall(text)
    if len(words) < 4 or len(words) > 75:
        return False
    if sum(len(w) for w in words) / max(1, len(text)) < 0.62:
        return False
    if any(token in text for token in ("=>", "===", "!=", "&&", "::", "\\n", "{", "}", "http://", "https://")):
        return False
    familiar = sum(zipf_frequency(w.lower(), "en") >= 3 or w.lower() in LEXICON for w in words) / len(words)
    if familiar < 0.65:
        return False
    # Short technical fragments are poorly classified by language detectors.
    if len(words) >= 7:
        try:
            return detect(text) == "en"
        except LangDetectException:
            return False
    return familiar >= 0.8


def extract_repository(root: Path, progress=None) -> list[Vocab]:
    nlp = nlp_model()
    records: dict[tuple[str, str], Vocab] = {}
    paths = sorted(p for p in root.rglob("*") if p.is_file() and not p.is_symlink()
                   and p.suffix.lower() in SUFFIXES and safe_path(p.relative_to(root).as_posix()))
    if len(paths) > 5000:
        raise ValueError("Repository exceeds 5,000 supported source files")
    scanned = 0
    for index, path in enumerate(paths):
        if path.stat().st_size > 512 * 1024:
            continue
        scanned += path.stat().st_size
        if scanned > 50 * 1024 * 1024:
            raise ValueError("Supported source exceeds 50 MiB")
        source = path.read_text(encoding="utf-8", errors="replace")
        candidates: list[tuple[Snippet, str]] = []
        for snippet in snippets(source, path.relative_to(root).as_posix()):
            if SECRET.search(snippet.text):
                continue
            if snippet.kind == "identifier":
                parts = [p for p in split_identifier(snippet.text) if p not in KEYWORDS]
                if not parts:
                    continue
                candidates.append((snippet, " ".join(parts)))
            elif is_english_prose(snippet.text):
                candidates.append((snippet, snippet.text))
        for (snippet, _), doc in zip(candidates, nlp.pipe([text for _, text in candidates], batch_size=64)):
            for token in doc:
                lemma = token.lemma_.lower().strip()
                if len(lemma) < 3 or not lemma.isascii() or not lemma.isalpha() or token.is_stop:
                    continue
                if lemma in A1_WORDS or lemma in KEYWORDS or token.pos_ in {"PROPN", "PUNCT", "NUM", "SYM"}:
                    continue
                if lemma not in LEXICON and zipf_frequency(lemma, "en") < 2.5:
                    continue
                pos = token.pos_ or "X"
                # Avoid fragment POS variation duplicating identifier-only terms.
                if snippet.kind == "identifier":
                    existing = next((k for k in records if k[0] == lemma), None)
                    if existing:
                        pos = existing[1]
                key = (lemma, pos)
                if key not in records:
                    level, definition, ipa = LEXICON.get(lemma, ("B2", None, None))
                    tags = [name for name, vocabulary in TOPICS.items() if lemma in vocabulary]
                    records[key] = Vocab(id="", lemma=lemma, part_of_speech=pos, frequency=0,
                                         cefr=level, definition=definition, ipa=ipa, tags=tags or ["general"])
                item = records[key]
                item.frequency += 1
                context = Context(text=snippet.text, file_path=snippet.file_path,
                                  line_number=snippet.line_number, kind=snippet.kind)
                if context not in item.contexts:
                    item.contexts.append(context)
                    item.contexts.sort(key=lambda c: c.kind == "identifier")
                    item.contexts = item.contexts[:3]
        if progress:
            progress(index + 1, len(paths))
    for item in records.values():
        difficulty = {"A2": 1.0, "B1": 1.4, "B2": 1.8, "C1": 2.2}.get(item.cefr, 1.8)
        usefulness = 1.6 if item.lemma in LEXICON else 1.0
        prose = 1.25 if any(c.kind != "identifier" for c in item.contexts) else 0.6
        item.rank = round(math.log2(1 + item.frequency) * difficulty * usefulness * prose, 3)
    return sorted(records.values(), key=lambda v: (-v.rank, v.lemma, v.part_of_speech))[:500]


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    args = parser.parse_args()
    print(json.dumps([item.model_dump() for item in extract_repository(args.repository)], indent=2, ensure_ascii=False))
