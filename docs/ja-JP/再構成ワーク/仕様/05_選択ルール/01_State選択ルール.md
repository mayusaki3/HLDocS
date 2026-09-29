<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260927-000000Z-SELS
lang: ja-JP
canonical_title: State選択ルール
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > 選択ルール > State選択ルール

# State(状態)選択ルール

## 1. 目的

本書は、WorkまたはWork Candidateを処理する遷移先候補Stateを抽出する選択ルールを定義する。

本ルールはStateを変更せず、遷移を許可せず、Execution Contextを変更しない。

## 2. 適用対象

State選択ルールは次に適用できる。

- NEW_WORK_REQUESTから構成されたWork Candidate
- ACTIVE Workの進行中に別Stateが必要となった場合
- Workflowその他からState遷移候補特定を要求された場合

新規Workについては、Workを確定生成する前のWork Candidateへ適用することを原則とする（MUST）。

## 3. 候補抽出元

候補StateはState Machineに登録され、現在Stateから遷移候補となり得るStateからのみ抽出する（MUST）。

未登録、到達不能、仕様取得不能なStateを候補としてはならない（MUST NOT）。

## 4. 選択根拠

候補StateはPurpose、明示的な利用者要求、既存Workの場合はWork Context、および候補Stateのwork_acceptanceその他の処理可能範囲から抽出する。

利用者要求に存在しない目的を推測で追加してはならない（MUST NOT）。

参照・調査と、その結果を条件とする変更が一つの利用者要求に明示されている場合、変更の実行が条件付きであってもPurposeは変更を含むものとして評価する。この場合、参照・調査だけを理由として情報参照Stateを別候補に追加し、`MULTIPLE(複数)`としてはならない（MUST NOT）。

純粋な情報参照Workの開始後に利用者が新たな変更要求を追加した場合、既存WorkのPurposeを暗黙に拡張してState候補を再選択してはならない（MUST NOT）。新しい変更要求はNEW_WORK_REQUESTとして評価する。

候補抽出に不要な全State詳細仕様を一括読込してはならない（MUST NOT）。

## 5. 選択結果

- UNIQUE: 候補が一つに確定した。
- MULTIPLE: 有効な候補が複数存在する。
- NONE: 有効な候補が存在しない。
- UNKNOWN: 必要情報不足により安全に判定できない。

## 6. UNIQUE

UNIQUEの場合、候補StateをState Machineへ提示してよい（MAY）。

UNIQUEは遷移許可を意味しない。  
新規Work Candidateの場合、State MachineとCoreによる検証完了までWorkをACTIVEとして確定してはならない（MUST NOT）。

## 7. MULTIPLE

候補を推測で一つにしてはならない（MUST NOT）。

利用者選択が必要な場合、InteractionへDecision Requestを発行する。  
回答後もState Machineによる遷移判定を省略してはならない（MUST NOT）。

## 8. NONE

既存Stateへ強制割当してはならない（MUST NOT）。

新規Work Candidateの場合、Workを生成せず、現在のHLDocSでは要求を処理できるStateがないことを必要に応じInteractionから通知する。

NONEを理由としてState、Workflowまたは仕様を自動生成してはならない（MUST NOT）。

## 9. UNKNOWN

Stateを推測してはならない（MUST NOT）。

利用者から不足情報を取得できる場合はInteractionへ確認を要求し、同じWork Candidateを再評価してよい（MAY）。

仕様不足が原因の場合は仕様不足として扱う。

## 10. 境界

State選択ルールは「どのStateが処理候補か」を扱う。  
State Machineは「現在Stateから候補Stateへ遷移してよいか」を扱う。  
Coreは確定変更を適用する。

---

[目次](../../目次.md) > 仕様 > 選択ルール > State選択ルール
