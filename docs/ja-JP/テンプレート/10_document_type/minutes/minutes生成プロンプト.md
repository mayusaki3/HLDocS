<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260122-000050Z-M1N3
lang: ja-JP
canonical_title: document_type:minutes 生成プロンプト
document_type: prompt
canonical_document: true
transport: [download, ui_copy]
-->

[目次](../../../目次.md) > テンプレート > document_type > minutes > 生成プロンプト

# document_type:minutes 生成プロンプト

## 0. 最上位命令（MUST）

- 出力は最終成果物のみとする。
- 思考過程・理由・検査結果を出力してはならない。
- `minutes` は事実記録であり、仕様の代替ではない。

## 1. minutes 判定（MUST）

以下に該当する場合、`minutes` を生成してよい。

- 会議・ディスカッション・設計検討の内容を記録する目的である。
- 合意事項・未決事項・次アクションを保存したい。

## 2. minutes 禁止判定（MUST NOT）

以下に該当する場合、`minutes` を生成してはならない。

- 合意済み仕様・規約を宣言することが主目的である（spec）
- テスト条件・期待結果を定義することが主目的である（testspec）
- LLM の生成・判断規則を定義することが主目的である（prompt）

## 3. 内容生成（MUST）

- 日時（または期間）を必ず含める。
- 議題を含める。
- 議論内容を要約して記載する。
- 合意事項／未決事項／次アクションを分離して記載する。

## 4. spec への派生（任意）

- `minutes` の章は、後続で `spec` 化される可能性がある。
- ただし `minutes` 自体に仕様を確定事項として閉じ込めてはならない。
- 派生関係の扱いは Traceability 規約に従う。

---

[目次](../../../目次.md) > テンプレート > document_type > minutes > 生成プロンプト
