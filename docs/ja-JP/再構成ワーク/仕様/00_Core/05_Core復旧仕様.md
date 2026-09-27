<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260927-000000Z-RCVR
lang: ja-JP
canonical_title: Core復旧仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Core > Core復旧仕様

# Core復旧仕様

## 1. 目的

本書は、Core起動後にState Machineへ制御を移譲できない場合の復旧方法を定義する。

復旧は通常運転用Workflowではなく、Coreが通常運転を成立させるために実施する限定処理である。

## 2. 復旧開始条件

Coreは、次のいずれかに該当する場合に復旧を開始しなければならない（MUST）。

- State Machine仕様を特定できない。
- State Machine仕様を取得できない。
- State Machine仕様を解釈できない。
- State Machineの初期化条件を満たせない。
- State Machineから有効な初期Stateを確定できない。
- State Machineへの制御移譲処理が失敗した。

HLDocSシステム起動条件そのものを満たしていない場合は、本復旧を開始してはならない（MUST NOT）。

## 3. 復旧中の実行状態

復旧中は、通常運転中のStateとして扱ってはならない（MUST NOT）。  
復旧を通常運転用State Machineへ登録されたStateとして扱うことを要求してはならない（MUST NOT）。

Coreは、復旧中であることをExecution Contextとは別のCore実行状態として識別できなければならない（MUST）。

復旧中に通常運転用Workflow、SubFlowまたはState遷移を開始してはならない（MUST NOT）。

## 4. 復旧制限

復旧開始時もCore基本制限を継続して適用しなければならない（MUST）。

Coreは復旧に必要な追加制限を「復旧Restriction Set」として読み込んでよい（MAY）。  
復旧Restriction SetはCore基本制限を緩和してはならない（MUST NOT）。

復旧Restriction Setを取得または適用できない場合は、Core基本制限だけで安全に実施できる次の処理に限定しなければならない（MUST）。

- 状況確認のための参照
- 不足または不整合の特定
- 利用者への状況提示
- 利用者判断の要求

この場合、HLDocS仕様/規約（正本）または作業対象正本を変更してはならない（MUST NOT）。

## 5. 復旧処理

Coreは、復旧を次の順序で実施しなければならない（MUST）。

1. 移譲失敗理由を特定する。
2. 復旧に必要な対象と操作を特定する。
3. 適用可能な復旧制限を確認する。
4. 利用者へ失敗理由、対象、必要な操作を提示する。
5. 変更が必要な場合は、利用者の明示的な指示または承認を得る。
6. 許可された対象および操作だけを実施する。
7. 修正後のState Machineを再検証する。
8. State Machineへの制御移譲を再試行する。

Coreは、復旧に不要な仕様を一括して読み込んではならない（MUST NOT）。

## 6. 復旧時の変更

復旧中の変更は、State Machineへの制御移譲を成立させるために必要な範囲に限定しなければならない（MUST）。

Coreは、利用者承認なしに次を行ってはならない（MUST NOT）。

- HLDocS仕様/規約（正本）の変更
- State定義の変更
- Workflow、SubFlowまたはTool定義の変更
- Restriction Set定義の変更
- 新しい仕様要素の追加
- 既存仕様要素の削除

Coreは、復旧中に通常作業上のIssueを解決するための変更を行ってはならない（MUST NOT）。

## 7. Interaction

復旧中の利用者との入出力はInteractionを利用する。

Interaction仕様を利用できないこと自体が移譲失敗原因である場合でも、Coreは実行環境が提供する最小限の利用者対話能力を使用して、少なくとも次を提示してよい（MAY）。

- HLDocSが通常運転を開始できないこと
- 特定できた失敗理由
- 利用者判断が必要な内容

この最小対話を通常運転開始と扱ってはならない（MUST NOT）。

## 8. 復旧成功

State Machineへの制御移譲に成功した場合、Coreは復旧を終了しなければならない（MUST）。

復旧用に追加したRestriction Setは復旧終了時に解除しなければならない（MUST）。  
Core基本制限は解除してはならない（MUST NOT）。

その後、State Machineが確定したCurrent Stateに必要なRestriction Setを適用してから通常運転を開始しなければならない（MUST）。

## 9. 復旧不能

復旧に必要な情報、仕様または利用者判断を得られない場合、Coreは通常運転へ移行してはならない（MUST NOT）。

Coreは安全側の状態を維持し、復旧不能理由と不足事項を利用者へ提示しなければならない（MUST）。

---

[目次](../../目次.md) > 仕様 > Core > Core復旧仕様
