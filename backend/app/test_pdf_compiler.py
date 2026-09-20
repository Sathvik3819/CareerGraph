from pathlib import Path

from app.pdf.generator import _resolve_xelatex_binary


def test_resolve_xelatex_binary_uses_miktex_name(monkeypatch):
    monkeypatch.setattr("app.pdf.generator.shutil.which", lambda name: None if name == "xelatex" else f"C:/MiKTeX/bin/{name}.exe")
    monkeypatch.setattr("app.pdf.generator.Path.exists", lambda self: str(self).endswith("miktex-xelatex.exe"))

    resolved = _resolve_xelatex_binary()

    assert resolved.endswith("miktex-xelatex.exe")
