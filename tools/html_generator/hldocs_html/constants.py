"""HLDocS HTML generator constants.

役割:
    HTML generator 全体で共有する定数を定義する。

注意点:
    - 仕様上の enum に相当する値はここへ集約する。
    - 変更時はテストと Presentation Model サンプルの整合を確認する。
"""

SUPPORTED_PROFILES = {"overview", "reference"}
DEFAULT_PROFILES = ["overview", "reference"]

PRESENTATION_MODEL_DIR = "Presentation-Model"

SUPPORTED_PRESENTATION_POLICIES = {
    "full_render",
    "overview_only",
    "link_only",
    "not_generated",
}

LEGACY_FALLBACK_POLICY = "full_render"
PRESENTATION_MODEL_FALLBACK_POLICY = "overview_only"
