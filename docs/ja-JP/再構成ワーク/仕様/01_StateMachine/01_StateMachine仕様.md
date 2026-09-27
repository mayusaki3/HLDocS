<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260927-000000Z-SM01
lang: ja-JP
canonical_title: State Machine仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > State Machine > State Machine仕様

# State Machine仕様

## 1. 目的

本書は、HLDocS通常運転におけるStateの構成およびState遷移規則を定義する。

State Machineは、作業内容、Workflow内部処理または利用者入力の意味を処理する機構ではない。

## 2. 責務

State Machineは次を担当する。

- 登録されたStateの識別
- Initial Stateの定義
- State間の遷移関係の定義
- State遷移要求に対する遷移可否の判断
- 遷移可能な場合のState変更要求

State MachineはCurrent Stateを直接変更してはならない（MUST NOT）。  
Current Stateの確定変更はCoreが行う。

## 3. State一覧

State Machineは、通常運転で利用可能なStateを登録しなければならない（MUST）。

登録されたStateには、個別State仕様への参照先が存在しなければならない（MUST）。  
登録されていないStateを通常運転で利用してはならない（MUST NOT）。

State Machineは、State個別仕様の内容を一覧へ複製して保持することを要求しない。  
Stateの詳細が必要な場合は、対象Stateの個別仕様を参照する。

## 4. Initial State

State MachineはInitial Stateを一つ定義しなければならない（MUST）。

初回の通常運転開始時は、Initial Stateへの進入要求をCoreへ行わなければならない（MUST）。

既存Workの復元時は、保存情報だけを根拠としてInitial Stateへ戻してはならない（MUST NOT）。  
復元対象のCurrent Stateおよび現在のState Machineとの整合性を確認し、復元可能な場合は対象Stateへの復元要求を行う。

Initial Stateを特定できない、登録を確認できない、または個別State仕様を取得できない場合、State Machineへの制御移譲は失敗として扱わなければならない（MUST）。

## 5. State遷移

State Machineは、State間の許可された遷移を定義しなければならない（MUST）。

State遷移要求を受けた場合は、少なくとも次を確認する。

- 遷移元が現在のCurrent Stateと一致すること。
- 遷移先Stateが登録されていること。
- 遷移元から遷移先への遷移が定義されていること。
- 遷移規則に定義された条件を満たすこと。

State Machineは、遷移条件を満たす場合に限りCoreへState変更要求を行ってよい（MAY）。

State Machineは、State遷移を成立させるために未定義のStateまたは遷移を推測して生成してはならない（MUST NOT）。

## 6. State変更適用

CoreはState MachineからState変更要求を受けた場合、Execution ContextおよびCore基本制限との整合性を確認する。

State変更を適用する場合、Coreは次の順序を保証しなければならない（MUST）。

1. 遷移元Stateに属する実行中処理がState遷移可能な状態であることを確認する。
2. 遷移先State仕様を参照する。
3. 遷移先Stateが宣言するRestriction Setを取得し、適用可能であることを検証する。
4. 遷移先Stateの開始に必要なExecution Context条件を検証する。
5. 遷移元State由来Restriction Setの解除と、遷移先State由来Restriction Setの適用をステージする。
6. Current StateおよびState由来Restriction Contextを、一つの整合した変更として確定する。
7. 確定後にのみ、遷移先Stateでの通常処理を開始可能とする。

検証またはステージ中に失敗した場合、Current Stateおよび有効な遷移元Restriction Contextを変更してはならない（MUST NOT）。

Core基本制限はState遷移中も解除してはならない（MUST NOT）。

遷移先Stateの必須Restriction Setを適用できない場合、制限なしで通常処理を開始してはならない（MUST NOT）。

## 7. State Machineが行ってはならないこと

State Machineは次を行ってはならない（MUST NOT）。

- 利用者入力をWorkflowへ配送する。
- Workflow候補を意味判断によって選択する。
- Workflow Planを生成または変更する。
- Workflowを開始、中断、再開または終了する。
- 利用者判断待ちを理由として自動的に別Stateへ遷移する。
- InteractionのDecision Requestを処理する。
- Restriction Setの内容を変更する。
- Execution Contextを直接変更する。

## 8. 待機との関係

利用者判断待ち、追加情報待ちまたはDecision Requestの存在だけを理由として、待機Stateへ遷移してはならない（MUST NOT）。

待機Stateは、通常運転中であり、現在実行すべきWorkまたはWorkflowが存在しない状態を表すStateとして定義する。

## 9. 制御移譲成立条件

CoreからState Machineへの制御移譲を成立させるには、少なくとも次を満たさなければならない（MUST）。

- State Machine仕様を解釈できること。
- State一覧を解決できること。
- Initial Stateを一意に特定できること。
- Initial StateがState一覧へ登録されていること。
- Initial State個別仕様を取得できること。
- Initial Stateの必須Restriction Setを適用できること。

成立しない場合は、Core復旧仕様に従う。

---

[目次](../../目次.md) > 仕様 > State Machine > State Machine仕様
