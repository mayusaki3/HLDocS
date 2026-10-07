<!--
HLDocS:LLM-MANAGED
doc_id: doc-20261007-000000Z-RS02
lang: ja-JP
canonical_title: Restriction Set登録簿
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Restriction > Restriction Set登録簿

# Restriction Set(制限セット)登録簿

## 1. 目的

本書は、HLDocSで利用可能なRestriction Set(制限セット)と、その個別仕様の参照先を登録する。

本登録簿はRestriction Setの存在確認および参照先解決のための登録情報であり、制限内容、実行順序または優先順位の正本ではない。

## 2. 登録規則

State(状態)、Workflow(ワークフロー)またはSubFlow(サブフロー)が通常運転で参照するRestriction Setは、本登録簿へ登録されていなければならない（MUST）。

Core(中核)は登録名だけから制限内容を推測してはならず（MUST NOT）、登録された個別仕様を参照して適用しなければならない（MUST）。

同一restriction_setを複数の個別仕様へ曖昧に関連付けてはならない（MUST NOT）。

## 3. 登録一覧

現時点で新構造側へ再構成済みの個別Restriction Setはない。

| restriction_set | 個別仕様 | 状態 |
| --- | --- | --- |
| - | - | 未登録 |

旧`00_共通`その他の旧仕様に存在する制限定義を、本登録簿へ登録せず暗黙に新構造のRestriction Setとして利用してはならない（MUST NOT）。

個別Restriction Setを再構成または新規追加した場合は、その個別仕様を確定したうえで本登録簿へ追加する。

---

[目次](../../目次.md) > 仕様 > Restriction > Restriction Set登録簿
