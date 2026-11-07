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
<!-- hldocs:sec_id=sec_7f2a91c4e6b84d03a59f72c0b18e6d43 -->

`scripts/core_validation_contract.py`は、Core正常性確認ケース定義のケースID集合とJSON fixtureの静的な形式契約を検査する補助ツールである。Coreを起動、模擬実行、障害注入するものではない（MUST NOT）。本ツールの検査成功はCore正常性を保証しない。

## 2. 入力と呼出し
<!-- hldocs:sec_id=sec_c9e51b6a28d74f03b65a90e2d1c87f44 -->

呼出し例：

```sh
python scripts/core_validation_contract.py --catalog "docs/ja-JP/再構成ワーク/仕様/06_Workflow/12_Core正常性確認ケース定義.md" --fixtures "tests/fixtures/core_validation"
```

`--catalog`は必須、`--fixtures`は任意とする。fixtureを指定しない場合のPASSはケース目録の形式検査PASSのみを意味する。指定したfixtureディレクトリが存在しない場合はエラーとする。

JSON fixtureの必須キーは次の14個とする（MUST）。

- 基本情報：`fixture_id`、`case_id`、`target_sha`、`mode`、`initial_state`、`preconditions`、`stimulus`、`expected`
- SUT境界情報：`canonical_snapshot`、`initial_context`、`provider_stub`、`restriction_stub`、`fault_injection`
- 不変条件：`expected_invariants`

基本型の条件は以下とする。

- `fixture_id`、`initial_state`：空でない文字列。
- `case_id`：WS-01〜WS-04またはFC-01〜FC-10。
- `target_sha`：小文字16進数40文字のコミットSHA形式。実在性や参照先内容は検査しない。
- `mode`：`STATIC`、`SIMULATED`、`EXECUTED`のいずれか。これはfixtureの宣言値であり、ツールがCoreを実行したことを意味しない。
- `preconditions`：配列。
- `stimulus`、`expected`：空でないJSONオブジェクト。
- 5つのSUT境界情報：空でないJSONオブジェクト。`status`が`UNRESOLVED`の場合、`reason`は文字列でなければならない。
- `expected_invariants`：空でない文字列からなる、空でない配列。

## 3. ケース目録とfixtureの検査
<!-- hldocs:sec_id=sec_20a7d5e94c6148b3a82f0c6e7d951a42 -->

- ケース目録ではWS-01〜04およびFC-01〜10がそれぞれ1回だけ存在することを検査する（MUST）。
- 目録内の予期しないWS/FC形式のケースID、および必須ケースIDの欠落・重複をエラーとする（MUST）。
- fixtureを指定した場合、直下の`*.json`を読み取り、必須キー、基本型、ケースID、SHA形式、境界情報、不変条件を検査する（MUST）。
- fixture間の`case_id`重複、および14ケースに対応するfixtureの欠落をエラーとする（MUST）。
- JSON解析失敗、カタログ読込失敗、fixture読込失敗はエラーとする（MUST）。
- `validate_fixture`に`expected_case`が指定された場合、`case_id`との一致を検査する。CLIの現行経路ではこの引数を指定しない。

fixtureの期待結果とCore正本の意味的一致、障害注入の成立、Observerの独立性、SUT実装の存在、実Coreの正常性は検査しない（MUST NOT）。

## 4. 判定と出力
<!-- hldocs:sec_id=sec_f48c1a72e9d6430b8a25d7c69e104f53 -->

標準出力にはJSONを出力し、`contract_check`は形式検査のPASS/FAILを表す。エラーがあれば終了コード1、なければ0とする（MUST）。

- `tool`：`core_validation_contract`
- `validation_mode`：常に`STATIC`
- `runtime_executed`：常に`false`
- `core_normality_verdict`：常に`UNDETERMINED`
- `catalog_cases_expected`：14
- `fixtures_checked`：読み取り対象として列挙したJSONファイル数
- `unresolved_boundary_fields`：`status=UNRESOLVED`の境界フィールド数
- `sut_execution_ready`：常に`false`
- `contract_check`：`PASS`または`FAIL`
- `errors`：検出エラーの配列

`contract_check=PASS`をCoreセルフ検証項目のPASSやEXECUTED PASSに読み替えてはならない（MUST NOT）。未解決境界フィールドが存在しても、形式が適合すれば静的契約検査はPASSになり得る。

## 5. 次工程
<!-- hldocs:sec_id=sec_a60d3c8f14b249e7a25c90f63e81d4b2 -->

実Coreの実行入口とObserverを特定できた後、SUT境界アダプターとfixtureを別途実装し、隔離・副作用・停止の成立を検証する。それまでは専用WorkflowをState/Planに登録しない。

---

[目次](../../目次.md) > 仕様 > Workflow > Core検証静的契約チェッカー仕様
