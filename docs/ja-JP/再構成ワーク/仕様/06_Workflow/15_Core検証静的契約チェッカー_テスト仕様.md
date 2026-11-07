<!--
HLDocS:LLM-MANAGED
doc_id: doc-20261107-021500Z-CVT1
lang: ja-JP
canonical_title: Core検証静的契約チェッカー テスト仕様
document_type: testspec
canonical_document: true
-->

[目次](../../目次.md) > 再構成ワーク > 仕様 > Workflow > Core検証静的契約チェッカー テスト仕様

# Core検証静的契約チェッカー テスト仕様

## 1. 適用範囲

対象：`scripts/core_validation_contract.py`。既存10件と追加設計16件を対象とし、Coreランタイム正常性ではなくSTATIC契約チェッカーを検証する。参照仕様：`doc-20261030-000000Z-CV06`。

既存番号CV-CONTRACT-001〜010、追加番号CV-CONTRACT-011〜026はテスト表示ラベルであり、恒久キーは各ケースの`sec_id`とする。実装テストコードには`@hldocs.ref`で本書の`doc_id#sec_id`を記載する。

## 2. 共通条件

- テスト実行ごとに独立した一時ディレクトリを利用する。
- 正常目録はWS-01〜04、FC-01〜10の各IDを1回ずつ含む。
- 正常fixtureは14必須キーと適合する型・値を持つ。
- 異常系では、対象項目以外は適合値とする。必要に応じて14件のfixtureを配置する。
- CLI検証では終了コードとJSON結果の双方を確認する。内部関数専用の検証では戻り値を確認する。
- `contract_check=PASS`でも`runtime_executed=false`、`core_normality_verdict=UNDETERMINED`を維持する。
- 行・分岐カバレッジ100%は別途実測して判定する。ケース数だけで達成を宣言しない。

## 3. テストケース

### CV-CONTRACT-001 既存：目録のみのSTATIC PASS
<!-- hldocs:sec_id=sec_7a13bc90c48f2a7183d1e602b6e9402c -->

**前提条件：** 共通条件を適用する。

**検証内容：** fixture未指定で完全な目録を入力。

**期待結果：** 終了0、contract_check=PASS、runtime_executed=false、core_normality_verdict=UNDETERMINED。

**参照仕様：** `doc-20261030-000000Z-CV06#sec_f48c1a72e9d6430b8a25d7c69e104f53`

### CV-CONTRACT-002 既存：fixture空ディレクトリ
<!-- hldocs:sec_id=sec_7a27023bc4b447aa83eca9f3b6fd6613 -->

**前提条件：** 共通条件を適用する。

**検証内容：** 空のfixtureディレクトリを指定。

**期待結果：** 14ケース欠落を検出し終了1。

**参照仕様：** `doc-20261030-000000Z-CV06#sec_20a7d5e94c6148b3a82f0c6e7d951a42`

### CV-CONTRACT-003 既存：14 fixture正常
<!-- hldocs:sec_id=sec_7a3a47e6c4d964e384076de4b7118bfa -->

**前提条件：** 共通条件を適用する。

**検証内容：** 14件の適合fixtureを指定。

**期待結果：** 終了0、fixtures_checked=14、Core実行判定はUNDETERMINED。

**参照仕様：** `doc-20261030-000000Z-CV06#sec_f48c1a72e9d6430b8a25d7c69e104f53`

### CV-CONTRACT-004 既存：fixture欠落
<!-- hldocs:sec_id=sec_7a4d8d91c4fe821c842231d5b725b1e1 -->

**前提条件：** 共通条件を適用する。

**検証内容：** FC-10を除いた13件を指定。

**期待結果：** FC-10欠落を検出し終了1。

**参照仕様：** `doc-20261030-000000Z-CV06#sec_20a7d5e94c6148b3a82f0c6e7d951a42`

### CV-CONTRACT-005 既存：fixture重複
<!-- hldocs:sec_id=sec_7a60d33cc5239f55843cf5c6b739d7c8 -->

**前提条件：** 共通条件を適用する。

**検証内容：** 同じcase_idのfixtureを2ファイルに格納。

**期待結果：** 重複を検出し終了1。

**参照仕様：** `doc-20261030-000000Z-CV06#sec_20a7d5e94c6148b3a82f0c6e7d951a42`

### CV-CONTRACT-006 既存：不正SHA
<!-- hldocs:sec_id=sec_7a7418e7c548bc8e8457b9b7b74dfdaf -->

**前提条件：** 共通条件を適用する。

**検証内容：** target_sha=developを指定。

**期待結果：** SHA形式違反を検出し終了1。

**参照仕様：** `doc-20261030-000000Z-CV06#sec_c9e51b6a28d74f03b65a90e2d1c87f44`

### CV-CONTRACT-007 既存：目録ケース欠落
<!-- hldocs:sec_id=sec_7a875e92c56dd9c784727da8b7622396 -->

**前提条件：** 共通条件を適用する。

**検証内容：** FC-10を欠いた目録を入力。

**期待結果：** FC-10欠落を検出し終了1。

**参照仕様：** `doc-20261030-000000Z-CV06#sec_20a7d5e94c6148b3a82f0c6e7d951a42`

### CV-CONTRACT-008 既存：必須フィールド欠落
<!-- hldocs:sec_id=sec_7a9aa43dc592f700848d4199b776497d -->

**前提条件：** 共通条件を適用する。

**検証内容：** canonical_snapshotを削除。

**期待結果：** 必須フィールド欠落を検出し終了1。

**参照仕様：** `doc-20261030-000000Z-CV06#sec_c9e51b6a28d74f03b65a90e2d1c87f44`

### CV-CONTRACT-009 既存：未解決理由欠落
<!-- hldocs:sec_id=sec_7aade9e8c5b8143984a8058ab78a6f64 -->

**前提条件：** 共通条件を適用する。

**検証内容：** fault_injectionをstatus=UNRESOLVEDのみとする。

**期待結果：** reasonの型違反を検出し終了1。

**参照仕様：** `doc-20261030-000000Z-CV06#sec_c9e51b6a28d74f03b65a90e2d1c87f44`

### CV-CONTRACT-010 既存：不変条件空配列
<!-- hldocs:sec_id=sec_7ac12f93c5dd317284c2c97bb79e954b -->

**前提条件：** 共通条件を適用する。

**検証内容：** expected_invariants=[]を指定。

**期待結果：** 不変条件違反を検出し終了1。

**参照仕様：** `doc-20261030-000000Z-CV06#sec_c9e51b6a28d74f03b65a90e2d1c87f44`

### CV-CONTRACT-011 追加：fixture非オブジェクト
<!-- hldocs:sec_id=sec_7ad4753ec6024eab84dd8d6cb7b2bb32 -->

**前提条件：** 共通条件を適用する。

**検証内容：** fixture JSONのトップレベルを配列にする。

**期待結果：** JSONオブジェクト必須のエラー、終了1。

**参照仕様：** `doc-20261030-000000Z-CV06#sec_c9e51b6a28d74f03b65a90e2d1c87f44`

### CV-CONTRACT-012 追加：未知case_id
<!-- hldocs:sec_id=sec_7ae7bae9c6276be484f8515db7c6e119 -->

**前提条件：** 共通条件を適用する。

**検証内容：** case_id=WS-99を指定。

**期待結果：** 未知IDエラー、終了1。

**参照仕様：** `doc-20261030-000000Z-CV06#sec_c9e51b6a28d74f03b65a90e2d1c87f44`

### CV-CONTRACT-013 追加：expected_case不一致
<!-- hldocs:sec_id=sec_7afb0094c64c891d8513154eb7db0700 -->

**前提条件：** 共通条件を適用する。

**検証内容：** validate_fixtureにexpected_case=FC-01、fixture case_id=WS-01を指定。

**期待結果：** 不一致エラーを返す。

**参照仕様：** `doc-20261030-000000Z-CV06#sec_20a7d5e94c6148b3a82f0c6e7d951a42`

### CV-CONTRACT-014 追加：fixture_id不正
<!-- hldocs:sec_id=sec_7b0e463fc671a656852dd93fb7ef2ce7 -->

**前提条件：** 共通条件を適用する。

**検証内容：** fixture_idに空文字列・数値をそれぞれ指定。

**期待結果：** 各入力を拒否する。

**参照仕様：** `doc-20261030-000000Z-CV06#sec_c9e51b6a28d74f03b65a90e2d1c87f44`

### CV-CONTRACT-015 追加：mode不正
<!-- hldocs:sec_id=sec_7b218beac696c38f85489d30b80352ce -->

**前提条件：** 共通条件を適用する。

**検証内容：** mode=INVALIDを指定。

**期待結果：** モード違反を検出し終了1。

**参照仕様：** `doc-20261030-000000Z-CV06#sec_c9e51b6a28d74f03b65a90e2d1c87f44`

### CV-CONTRACT-016 追加：initial_state不正
<!-- hldocs:sec_id=sec_7b34d195c6bbe0c885636121b81778b5 -->

**前提条件：** 共通条件を適用する。

**検証内容：** initial_stateに空文字列・数値をそれぞれ指定。

**期待結果：** 各入力を拒否する。

**参照仕様：** `doc-20261030-000000Z-CV06#sec_c9e51b6a28d74f03b65a90e2d1c87f44`

### CV-CONTRACT-017 追加：preconditions不正
<!-- hldocs:sec_id=sec_7b481740c6e0fe01857e2512b82b9e9c -->

**前提条件：** 共通条件を適用する。

**検証内容：** preconditionsを配列以外にする。

**期待結果：** 型違反を検出し終了1。

**参照仕様：** `doc-20261030-000000Z-CV06#sec_c9e51b6a28d74f03b65a90e2d1c87f44`

### CV-CONTRACT-018 追加：stimulus/expected不正
<!-- hldocs:sec_id=sec_7b5b5cebc7061b3a8598e903b83fc483 -->

**前提条件：** 共通条件を適用する。

**検証内容：** stimulus、expectedをそれぞれ空オブジェクト・配列にする。

**期待結果：** 各入力を拒否する。

**参照仕様：** `doc-20261030-000000Z-CV06#sec_c9e51b6a28d74f03b65a90e2d1c87f44`

### CV-CONTRACT-019 追加：境界フィールド不正
<!-- hldocs:sec_id=sec_7b6ea296c72b387385b3acf4b853ea6a -->

**前提条件：** 共通条件を適用する。

**検証内容：** 5境界フィールドの代表値を空オブジェクト・配列にする。

**期待結果：** 各入力を拒否する。

**参照仕様：** `doc-20261030-000000Z-CV06#sec_c9e51b6a28d74f03b65a90e2d1c87f44`

### CV-CONTRACT-020 追加：不変条件要素不正
<!-- hldocs:sec_id=sec_7b81e841c75055ac85ce70e5b8681051 -->

**前提条件：** 共通条件を適用する。

**検証内容：** expected_invariantsに空文字列・数値を含める。

**期待結果：** 各入力を拒否する。

**参照仕様：** `doc-20261030-000000Z-CV06#sec_c9e51b6a28d74f03b65a90e2d1c87f44`

### CV-CONTRACT-021 追加：目録未知ID
<!-- hldocs:sec_id=sec_7b952decc77572e585e934d6b87c3638 -->

**前提条件：** 共通条件を適用する。

**検証内容：** 目録にWS-99を追加。

**期待結果：** 予期しないケースIDを検出し終了1。

**参照仕様：** `doc-20261030-000000Z-CV06#sec_20a7d5e94c6148b3a82f0c6e7d951a42`

### CV-CONTRACT-022 追加：目録重複ID
<!-- hldocs:sec_id=sec_7ba87397c79a901e8603f8c7b8905c1f -->

**前提条件：** 共通条件を適用する。

**検証内容：** 目録にWS-01を2行記載。

**期待結果：** 重複を検出し終了1。

**参照仕様：** `doc-20261030-000000Z-CV06#sec_20a7d5e94c6148b3a82f0c6e7d951a42`

### CV-CONTRACT-023 追加：目録読込失敗
<!-- hldocs:sec_id=sec_7bbbb942c7bfad57861ebcb8b8a48206 -->

**前提条件：** 共通条件を適用する。

**検証内容：** 存在しないcatalogパスを指定。

**期待結果：** 読込エラーをJSONに記録し終了1。

**参照仕様：** `doc-20261030-000000Z-CV06#sec_20a7d5e94c6148b3a82f0c6e7d951a42`

### CV-CONTRACT-024 追加：fixtureディレクトリ不存在
<!-- hldocs:sec_id=sec_7bcefeedc7e4ca90863980a9b8b8a7ed -->

**前提条件：** 共通条件を適用する。

**検証内容：** 存在しないfixturesパスを指定。

**期待結果：** ディレクトリ不存在エラー、終了1。

**参照仕様：** `doc-20261030-000000Z-CV06#sec_c9e51b6a28d74f03b65a90e2d1c87f44`

### CV-CONTRACT-025 追加：JSON構文不正
<!-- hldocs:sec_id=sec_7be24498c809e7c98654449ab8cccdd4 -->

**前提条件：** 共通条件を適用する。

**検証内容：** fixtureファイルに不正JSONを記載。

**期待結果：** JSON解析エラー、終了1。

**参照仕様：** `doc-20261030-000000Z-CV06#sec_20a7d5e94c6148b3a82f0c6e7d951a42`

### CV-CONTRACT-026 追加：fixture読込失敗
<!-- hldocs:sec_id=sec_7bf58a43c82f0502866f088bb8e0f3bb -->

**前提条件：** 共通条件を適用する。

**検証内容：** fixture読込時にOSErrorを注入する。

**期待結果：** 読込エラーをJSONに記録し終了1。

**参照仕様：** `doc-20261030-000000Z-CV06#sec_20a7d5e94c6148b3a82f0c6e7d951a42`

## 4. カバレッジ判定と補完

- `coverage.py`のbranch測定を有効にし、subprocessの実行データを統合する。
- 対象は`scripts/core_validation_contract.py`。行・分岐とも100%を合格基準とする。
- 既存・追加26件の実行後、未実行行または未網羅分岐が残る場合は、実測結果に基づきテストケースを追加設計してから実装する。
- モジュールimport時の`__main__`分岐など、CLIのみで測れない経路は直接importを使う追加テストの要否を実測で判断する。
- Coreの実行正常性は本仕様の判定対象外とする。

---

[目次](../../目次.md) > 再構成ワーク > 仕様 > Workflow > Core検証静的契約チェッカー テスト仕様
