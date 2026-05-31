"""Compatibility test entrypoint for split HLDocS HTML generator tests.

役割:
    従来の `pytest tools/html_generator/test_generate_html.py` を維持しつつ、
    責務別に分割した tests 配下のテストを実行対象にする。

注意点:
    - 実テストは `tools/html_generator/tests/` 配下に配置する。
    - 本ファイルにはテストロジックを持たせない。
"""

from __future__ import annotations

from tests.test_generator import *  # noqa: F401,F403
from tests.test_markdown_loader import *  # noqa: F401,F403
from tests.test_presentation_model import *  # noqa: F401,F403
from tests.test_renderer import *  # noqa: F401,F403
