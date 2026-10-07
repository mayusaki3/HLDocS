<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260927-000000Z-BASE
lang: ja-JP
canonical_title: Core基本制限仕様
document_type: spec
canonical_document: true
-->

[目次](../../目次.md) > 仕様 > Core > Core基本制限仕様

# Core基本制限仕様

## 1. 目的

本書は、HLDocSシステム起動前からCoreが常時適用する、解除不能な安全側の基本制限を定義する。

Core基本制限は、通常運転用のRestriction Setではない。  
State、WorkflowまたはSubFlowによるRestriction Setが存在しない場合でも適用されなければならない（MUST）。

## 2. 適用期間

Core基本制限は、HLDocSシステムの起動判定を開始した時点から適用しなければならない（MUST）。  
HLDocSの通常運転中、待機中、Workflow中断中および復旧中も継続して適用しなければならない（MUST）。

State、Workflow、SubFlow、Tool、Restriction Setその他の仕様要素は、Core基本制限を解除または緩和してはならない（MUST NOT）。

## 3. 基本原則

Coreは、処理を実行する前に、その処理が現在の制限に適合することを確認しなければならない（MUST）。

必要な仕様、制限、対象、要求元または利用者判断を確認できない場合は、許可されているものとして処理してはならない（MUST NOT）。

Core基本制限と他の制限が競合する場合は、Core基本制限またはより厳しい制限を適用しなければならない（MUST）。

## 4. Execution Context保護

Execution ContextはCoreだけが確定状態を変更できる（MUST）。

SubsystemはExecution Contextの変更をCoreへ要求できる。  
Coreは、要求元、変更対象、現在値、要求値および必要な承認根拠を確認できない変更要求を適用してはならない（MUST NOT）。

Execution Contextの不整合を検出した場合は、不整合を推測で補完して通常処理を継続してはならない（MUST NOT）。

## 5. 利用者判断の保護

利用者の承認または選択を必要とする処理は、明示的な利用者判断を確認するまで確定してはならない（MUST NOT）。

次を利用者承認として扱ってはならない（MUST NOT）。

- LLM自身の提案
- Issueの発見
- WorkflowまたはSubFlowの処理結果だけを根拠とした新規作業の追加
- 利用者判断を必要とする待機理由が解消されていない状態での「進めて」「続けて」等の継続指示

利用者判断が不足している場合は、Interactionを通じて必要な判断を求めなければならない（MUST）。

## 6. Workflow Plan保護

Workflow Planへの次の構成変更は、Plan Ownerに対応する正当な変更根拠なしに確定してはならない（MUST NOT）。

- Workflowの追加
- Workflowの削除
- Workflow順序の変更
- WorkflowのSKIPPED化

Owner=WORKの場合、利用者の明示的な指示または承認を必要とする。

Owner=SYSTEMの場合、対応するStateまたはSYSTEM処理仕様に明示された変更規則と、その条件が現在成立している根拠を必要とする。利用者承認だけをSYSTEM Plan変更規則の代替としてはならない（MUST NOT）。

Issueを記録することとWorkflow Planを変更することを同一処理として扱ってはならない（MUST NOT）。

## 7. 仕様参照の保護

現在の処理に必要な仕様だけを参照しなければならない（MUST）。

仕様要素の存在、識別子、参照先または内容を確認できない場合、それらを推測して存在するものとして扱ってはならない（MUST NOT）。

登録が必要な仕様要素は、登録確認後に個別仕様を参照しなければならない（MUST）。

## 8. Restriction Context保護

Coreは、現在のState、Active Workflowおよび実行中SubFlowに対応するRestriction Setが宣言されている場合、それらをRestriction Contextへ積み上げなければならない（MUST）。

下位のRestriction Setは上位の制限を緩和してはならない（MUST NOT）。

宣言されたRestriction Setを取得、検証または適用できない場合、対象処理を制限なしで継続してはならない（MUST NOT）。

## 9. Toolおよび能力実行の保護

Toolその他の実行手段を実行する前に、Coreは実行しようとするCapability(能力)、操作、対象範囲および選択されたCapability Provider(能力提供手段)がRestriction Contextで許容されることを確認しなければならない（MUST）。

同じ能力を別のToolで実行できることを、制限回避の理由としてはならない（MUST NOT）。

制限はTool名だけでなく、対象、操作種別および実行能力に対して適用できなければならない（MUST）。

## 10. 復旧時の制限

State Machineへ制御移譲できない場合でも、Core基本制限は維持しなければならない（MUST）。

復旧中は、復旧に必要な対象および操作だけを許容しなければならない（MUST）。  
通常運転用Workflowを開始してはならない（MUST NOT）。  
復旧を理由としてCore基本制限を解除してはならない（MUST NOT）。

復旧に必要な追加制限を取得できない場合は、Core基本制限だけで安全に実施できる参照、状況提示および利用者判断要求を除き、変更操作を実施してはならない（MUST NOT）。

## 11. Fail-closed

Coreは、処理を許可できる根拠を確認できない場合、その処理を実行してはならない（MUST NOT）。

Fail-closedによって処理を継続できない場合は、処理を無言で終了してはならず（MUST NOT）、利用可能なInteractionを通じて、停止理由および必要な判断または不足情報を利用者へ提示しなければならない（MUST）。

---

[目次](../../目次.md) > 仕様 > Core > Core基本制限仕様
