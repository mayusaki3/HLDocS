<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260927-000000Z-SELS
lang: ja-JP
canonical_title: State選択ルール
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > 選択ルール > State選択ルール

# State選択ルール

## 1. 目的

本書は、Workを処理するためにState遷移が必要な場合、遷移先候補Stateを抽出するための選択ルールを定義する。

State選択ルールは管理機構ではない。  
Stateを変更せず、State遷移を許可せず、Execution Contextを変更しない。

## 2. 適用条件

State選択ルールは、少なくとも次の場合に適用してよい（MAY）。

- 新規Workを生成した後、現在StateではそのWorkを処理できない場合。
- Workの進行により、別Stateでの処理が必要になった場合。
- Workflowその他の処理からState遷移候補の特定を要求された場合。

State遷移を必要としない処理に対して、Stateを選択することを目的として本ルールを適用してはならない（MUST NOT）。

## 3. 候補抽出元

候補Stateは、State Machineに登録されたStateからのみ抽出しなければならない（MUST）。

さらに、現在StateからState Machine上で遷移候補となり得るStateだけを対象とする。

未登録State、到達不能Stateまたは仕様を取得できないStateを候補としてはならない（MUST NOT）。

State選択ルールは、候補を得るために新しいStateを生成してはならない（MUST NOT）。

## 4. 選択根拠

候補Stateは、Work Purpose、現在のWork Context、利用者の明示的な作業要求、および候補Stateの目的・処理可能範囲を根拠として抽出する。

候補抽出に必要な範囲を超えて、全Stateの詳細仕様を一括して読み込むことを要求してはならない（MUST NOT）。

State MachineのState一覧に候補抽出に必要な情報が不足する場合は、必要な候補Stateの個別仕様だけを参照する。

利用者要求に存在しない作業目的を推測で追加し、それを根拠としてState候補を選択してはならない（MUST NOT）。

## 5. 選択結果

State選択ルールの結果は次のいずれかとする。

- UNIQUE: 候補が一つに確定した。
- MULTIPLE: 有効な候補が複数存在し、一意に確定できない。
- NONE: 有効な候補が存在しない。
- UNKNOWN: 必要情報が不足し、候補を安全に確定できない。

## 6. UNIQUE

結果がUNIQUEの場合、選択されたStateをState遷移候補としてState Machineへ提示してよい（MAY）。

UNIQUEはState遷移の許可を意味しない。  
State Machineは、通常のState遷移規則に従って遷移可否を判断しなければならない（MUST）。

CoreはState Machineの判断を経ずに、State選択結果だけを根拠としてCurrent Stateを変更してはならない（MUST NOT）。

## 7. MULTIPLE

結果がMULTIPLEの場合、候補を一つに推測してはならない（MUST NOT）。

利用者判断によって選択可能な場合は、候補と選択理由をInteractionへDecision Requestとして提示する。

利用者が候補を選択した場合も、その選択結果をState遷移許可として扱ってはならない（MUST NOT）。  
選択後はState MachineへState遷移候補を提示する。

## 8. NONE

結果がNONEの場合、既存Stateへ強制的に割り当ててはならない（MUST NOT）。

NONEは、少なくとも次の可能性を示す。

- 現在のState Machineでは当該Workを処理するStateが定義されていない。
- 必要なStateは存在するが、現在Stateから到達できない。
- 利用者要求がHLDocSの現在の通常運転範囲外である。

必要な場合はInteractionを通じて状況を提示し、利用者へ作業方針を確認する。

NONEを理由として新しいState、Workflowまたは仕様を自動生成してはならない（MUST NOT）。

## 9. UNKNOWN

結果がUNKNOWNの場合、Stateを推測してはならない（MUST NOT）。

不足情報が利用者から取得可能な場合はInteractionへDecision Requestまたは情報要求を行う。  
不足している仕様が本来存在すべきものである場合は、仕様不足として扱う。

## 10. State Machineとの境界

State選択ルールは「どのStateが処理候補か」を扱う。  
State Machineは「現在Stateから候補Stateへ遷移してよいか」を扱う。

次を混同してはならない（MUST NOT）。

- State候補の意味上の適合性
- State Machine上の遷移可能性
- CoreによるState変更適用可能性

---

[目次](../../目次.md) > 仕様 > 選択ルール > State選択ルール
