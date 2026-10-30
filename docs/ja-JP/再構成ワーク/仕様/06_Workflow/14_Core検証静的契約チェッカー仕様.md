<!--
HLDocS:LLM-MANAGED
doc_id: doc-20261030-000000Z-CV06
lang: ja-JP
canonical_title: Core検証静的契約チェッカー仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Workflow > Core検証静的契約チェッカー仕様

# Core検証静的契約チェッカー仕様

## 1. 目的と位置付け

`scripts/core_validation_contract.py`は、Core正常性確認ケース定義のケースID集合と、将来作成するJSON fixtureの最小契約を検査する補助ツールである。Coreを起動、模擬実行、障害注入するものではない（MUST NOT）。

## 2. 入出力

呼出し例：

```sh
python scripts/core_validation_contract.py --catalog "docs/ja-JP/再構成ワーク/仕様/06_Workflow/12_Core正常性確認ケース定義.md"
```

JSON fixtureが存在する場合のみ`--fixtures <directory>`を指定する。存在しないディレクトリを指定した場合はエラーとする。fixture未指定のPASSは**ケース目録の形式検査PASS**のみを意味する。

入力fixtureの必須キーは`case_id`、`target_sha`、`mode`、`initial_state`、`preconditions`、`stimulus`、`expected`とする。target_shaは小文字40桁のGitコミットSHA形式を要求するが、当該SHAの存在・正本内容の整合性までは検証しない。

## 3. 検査範囲

- WS-01〜04とFC-01〜10が目録にそれぞれ1回だけ存在する。
- fixtureの必須キー、基本型、case_id、mode、target_sha形式を確認する。
- 複数fixture間のcase_id重複を検出する。

fixtureの期待結果がCore正本と意味的に一致すること、障害注入の成立、Observerの独立性、SUT実装の存在、実Coreの正常性は検査しない（MUST NOT）。

## 4. 判定

出力JSONの`contract_check`は形式検査のPASS/FAILを表す。`validation_mode`は常にSTATIC、`runtime_executed`は常にfalse、`core_normality_verdict`は常にUNDETERMINEDとする（MUST）。

このPASSをCoreセルフ検証項目のPASSやEXECUTED PASSに読み替えてはならない（MUST NOT）。

## 5. 次工程

実Coreの実行入口とObserverを特定できた後、SUT境界アダプターとfixtureを別途実装し、隔離・副作用・停止の成立を検証する。それまでは専用WorkflowをState/Planに登録しない。

---

[目次](../../目次.md) > 仕様 > Workflow > Core検証静的契約チェッカー仕様
