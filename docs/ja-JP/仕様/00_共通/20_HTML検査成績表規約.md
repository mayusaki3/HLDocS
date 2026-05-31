<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260512-HtmlInspectionReport
lang: ja-JP
canonical_title: HTML検査成績表規約
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > 共通 > HTML検査成績表規約

# HTML検査成績表規約

本書は、「HLDocS 前提条件」という仕様が参照可能である場合にのみ適用される。

- 「HLDocS 前提条件」が入力として与えられていない場合、または当該仕様に基づく適用可否が確定していない場合、本書に基づく判断・生成・再作成・工程実行を行ってはならない。
- この場合、許可されるのは、提示された文書の受理および存在確認、ならびに前提条件が未参照または未確定である旨の通知のみとする。
- 「HLDocS 前提条件」が入力文書一覧に含まれない場合、生成・再作成・成果物提示を一切行ってはならない。

---

## 1. 目的

本書は、HLDocS における検査成績表・テスト結果・検証結果の HTML 表示方法を定義する。

本規約は、以下を安定化することを目的とする。

- テスト結果可視化
- 検査成績表生成
- evidence 表示
- review 支援
- Traceability 関係表示
- stale result 管理

---

## 2. 基本方針

HTML 検査成績表は、Markdown 正本または外部テスト結果から生成される generated operational representation とする。

HTML 検査成績表は canonical specification ではない。

HTML 検査成績表を編集正本として扱ってはならない（MUST NOT）。

HTML 検査成績表から Markdown 正本または test result source を逆生成してはならない（MUST NOT）。

---

## 3. 想定対象

HTML 検査成績表は、少なくとも以下を対象としてよい（MAY）。

- testspec 結果
- unit test 結果
- integration test 結果
- validation 結果
- migration validation
- restructuring validation
- CI result
- manual inspection

---

## 4. Test Report Page

HTML 検査成績表は、少なくとも以下を表示してよい（MAY）。

- test_id
- test_name
- PASS / FAIL
- SKIP
- execution_time
- environment
- evidence
- logs
- screenshots
- generated_at
- stale state

---

## 5. Traceability 関係

HTML 検査成績表は、少なくとも以下との Traceability 関係を表示してよい（MAY）。

```text
spec
↓
testspec
↓
code
↓
testcode
↓
test result
```

また、以下を表示してよい（MAY）。

- reverse traceability
- orphan relation
- missing relation
- stale relation

---

## 6. evidence

evidence として、少なくとも以下を表示してよい（MAY）。

- logs
- screenshots
- downloadable artifacts
- CI output
- validation summary
- generated report

Evidence は generated artifact として扱う。

Evidence を canonical specification とみなしてはならない（MUST NOT）。

---

## 7. stale result

以下を stale result として扱ってよい（MAY）。

- source markdown 更新後未再実行
- source code 更新後未再実行
- migration 後未再検証
- restructuring 後未再検証
- stale representation を対象とした結果

stale result は、最新 validation result と等価であるとみなしてはならない（MUST NOT）。

---

## 8. Coverage 表示

HTML 検査成績表は、Coverage 状態を表示してよい（MAY）。

想定例：

- implemented
- tested
- untested
- failed
- orphan
- stale

Coverage 表示は、review 支援用途を想定する。

---

## 9. review navigation

HTML 検査成績表は、レビュー支援 navigation を提供してよい（MAY）。

想定例：

- failed list
- stale result list
- untested list
- orphan relation list
- review target list
- migration warning list

---

## 10. profile 関係

HTML 検査成績表は、主に以下 profile に属する。

- `test-report`
- `full`

必要に応じて `overview` に summary を含めてよい（MAY）。

---

## 11. Link 解決

HTML 検査成績表間リンクは、HTML Site Manifest に基づいて解決しなければならない（MUST）。

Manifest に存在しないページへリンクしてはならない（MUST NOT）。

未生成ページは、必要に応じて `not generated` と表示してよい（MAY）。

---

## 12. 表示形式

HTML 検査成績表では、少なくとも以下を利用してよい（MAY）。

- table
- matrix
- graph
- dashboard
- timeline
- summary card

表示形式は canonical specification ではない。

---

## 13. restructuring / migration

HTML 検査成績表は、restructuring / migration 関係を表示してよい（MAY）。

想定例：

- migration validation result
- restructuring validation result
- old/new relation
- stale warning

---

## 14. 非目標

本規約は、以下を目的としない。

- CI system 固定
- test framework 固定
- GitHub Pages 固定
- DB server
- dynamic dashboard server
- AI automatic validation

LLM は、存在しない test result を推測生成してはならない（MUST NOT）。

---

## 15. 後続仕様化対象

後続仕様では、少なくとも以下を詳細化する。

- report JSON format
- evidence metadata
- screenshot relation
- downloadable artifact rule
- stale severity
- migration validation severity
- dashboard layout
- timeline format
- external CI adapter relation

---

[目次](../../目次.md) > 仕様 > 共通 > HTML検査成績表規約
