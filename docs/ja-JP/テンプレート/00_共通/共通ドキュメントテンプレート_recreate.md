<!--
HLDocS:LLM-MANAGED
doc_id: doc-20260428-130000Z-A1B2
lang: ja-JP
canonical_title: 共通ドキュメントテンプレート
document_type: template
canonical_document: true
-->

[目次](__TOC_REL_PATH__) > __HIERARCHY_PATH__

# __TITLE__

本テンプレートは、HLDocS におけるすべての document_type に共通して適用される文書外枠構造を定義するためのものである。  
本テンプレートは、仕様・プロンプト・テンプレートなどすべての HLDocS 文書の基盤となる構造を提供し、再現可能な文書生成および構造検証を可能にすることを目的とする。  
本テンプレートは、HLDocS 共通仕様が成立していることを前提として使用される。  

__COMMON_TEMPLATE_BEGIN__
<LLM_MANAGED_BLOCK>
<BLANK_LINE>
[目次](__TOC_REL_PATH__) > __HIERARCHY_PATH__
<BLANK_LINE>
# __TITLE__
<BLANK_LINE>
__DOCUMENT_BODY__
<BLANK_LINE>
<SECTION_SEPARATOR>
<BLANK_LINE>
[目次](__TOC_REL_PATH__) > __HIERARCHY_PATH__
__COMMON_TEMPLATE_END__

---

[目次](__TOC_REL_PATH__) > __HIERARCHY_PATH__
