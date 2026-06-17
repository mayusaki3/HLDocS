```{=html}
<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260617-000000Z-HLDOCS-ABOUT-01
lang: ja-JP
canonical_title: HLDocSとは
document_type: spec
canonical_document: false
status: draft
version_target: v0.7.0-preview
-->
```
[目次](../../../目次.md) \> 再構成ワーク \> 仕様 \> 00_共通 \>
HLDocSとは

# HLDocSとは

## 1. HLDocSとは何か

HLDocSは、LLMがドキュメントの生成・更新・検証を行うための共通仕様である。
LLMは利用者が正本として指定した仕様を根拠として処理を実行する。

## 2. HLDocSの目的

-   正本仕様を根拠として作業する
-   作業の再現性・検証性を高める
-   Workflowに基づいて作業を進める
-   推測や記憶への過度な依存を抑制する

## 3. HLDocSの構成

HLDocSは主に次の要素で構成される。

-   共通仕様
-   ドキュメント種別仕様
-   テンプレート
-   Workflow
-   利用ガイド

## 4. LLM_WORKSPACE

LLM_WORKSPACEとは、HLDocS実行中にLLMが利用する作業領域である。

LLM_WORKSPACEには、作業状態、引継ぎ情報、作業記録などWorkflowの継続に必要な情報を保持する。

LLM_WORKSPACEは正本仕様ではない。

正本仕様は利用者が指定した仕様であり、LLM_WORKSPACEは実行支援情報として扱う。

詳細はLLM_WORKSPACE規約に従う。

## 5. 基本ルール

-   正本仕様を最優先する。
-   共通仕様成立後にHLDocSを開始する。
-   Workflowに従って状態遷移する。
-   現在の状態で必要な仕様のみを参照する。
-   実行環境を確認した上で処理を開始する。

## 6. 最初の状態

HLDocS開始時は、次の順序で処理を開始する。

1.  実行環境を確認する。
2.  共通仕様成立を確認する。
3.  最初のWorkflowへ遷移する。

------------------------------------------------------------------------

[目次](../../../目次.md) \> 再構成ワーク \> 仕様 \> 00_共通 \>
HLDocSとは
