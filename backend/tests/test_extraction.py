from pathlib import Path

import pytest

from app.extraction import extract_repository, is_english_prose, snippets, split_identifier


@pytest.mark.parametrize("identifier,expected", [
    ("getUserPermissions", ["get", "user", "permissions"]),
    ("HTTPResponseParser", ["http", "response", "parser"]),
    ("retrieve_user_permissions", ["retrieve", "user", "permissions"]),
    ("refreshOAuth2Token", ["refresh", "o", "auth", "token"]),
])
def test_identifier_splitting(identifier, expected):
    assert split_identifier(identifier) == expected


def test_parser_keeps_correct_lines():
    source = '// Validate the session before retrieving protected resources.\nconst x = "Authentication requires a valid session.";'
    results = list(snippets(source, "auth.ts"))
    assert any(s.line_number == 1 and s.kind == "comment" and s.text.startswith("Validate") for s in results)
    assert any(s.line_number == 2 and s.kind == "string" and s.text.startswith("Authentication") for s in results)


def test_markdown_skips_fences_and_sensitive_files():
    assert [s.text for s in snippets("Helpful documentation is available here.\n```ts\nvalidateToken()\n```", "README.md")] == ["Helpful documentation is available here."]
    assert not list(snippets("Authentication requires a valid session", "credentials.py"))
    assert not list(snippets("Authentication requires a valid session", "node_modules/lib.ts"))


@pytest.mark.parametrize("text", [
    "api_key = sk-abcdefghijklmnopqrstuv", "const permissions = (user) => { return user.permissions; }",
    "Xin chào bạn, đây là tài liệu xác thực người dùng.", "hello", "-----BEGIN RSA PRIVATE KEY-----",
    "Use this credential: AKIAABCDEFGHIJKLMNOP to authenticate the request.",
])
def test_low_quality_and_secrets_rejected(text):
    assert not is_english_prose(text)


def test_extraction_lemmatizes_and_ranks_original_context(sample: Path):
    words = extract_repository(sample)
    by_lemma = {w.lemma: w for w in words}
    assert {"authentication", "permission", "retrieve", "validate", "transaction"}.issubset(by_lemma)
    assert not {"the", "user", "return", "get"}.intersection(by_lemma)
    assert "permissions" not in by_lemma
    assert words == sorted(words, key=lambda w: (-w.rank, w.lemma, w.part_of_speech))
    assert by_lemma["authentication"].cefr_estimated
    for word in words:
        assert 1 <= len(word.contexts) <= 3
        assert word.frequency >= 1
        for context in word.contexts:
            original = (sample / context.file_path).read_text().splitlines()[context.line_number - 1]
            assert context.text in original


def test_no_secrets_retained(tmp_path):
    (tmp_path / "source.ts").write_text('// Authenticate the request using api_key=sk-abcdefghijklmnopqrstuv\n// Validate the session before retrieving protected resources.')
    words = extract_repository(tmp_path)
    assert words
    assert all("sk-" not in c.text and "api_key=" not in c.text for w in words for c in w.contexts)


@pytest.mark.parametrize("name,source", [
    ("sample.java", "class Example { /* Validate the session before retrieving protected resources. */ void validateSession() {} }"),
    ("sample.go", "package main\n// Validate the session before retrieving protected resources.\nfunc validateSession() {}"),
    ("sample.tsx", "// Validate the session before retrieving protected resources.\nconst Page = () => <div />;"),
])
def test_additional_grammars(name, source):
    assert any(s.kind == "comment" and "Validate" in s.text for s in snippets(source, name))
