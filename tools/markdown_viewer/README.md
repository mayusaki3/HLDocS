# HLDocS Markdown Viewer

## 1. Purpose

markdown_viewer は、HLDocS Canonical Markdown を軽量に閲覧するための Browse 系 UI である。

```text
Canonical Markdown
→ Read / Navigate / Render
```

viewer は Markdown 正本を閲覧することのみを目的とする。

---

## 2. Positioning

markdown_viewer は：

```text
Lightweight Canonical Markdown Browser
```

である。

以下ではない。

```text
- graph runtime
- runtime platform
- operational runtime
- projection platform
- distributed synchronization framework
```

---

## 3. Responsibilities

markdown_viewer は Browse 系責務のみを扱う。

### 対象

```text
- markdown render
- source view
- TOC
- hash navigation
- section navigation
- sticky toolbar
- Mermaid rendering
```

---

## 4. Non-responsibilities

以下は markdown_viewer の責務ではない。

```text
- relationship graph generation
- graph runtime
- graph synchronization
- projection model
- runtime orchestration
- capability registry
- renderer abstraction framework
```

これらは html_generator または別 runtime 側責務。

---

## 5. Mermaid Positioning

viewer における Mermaid は：

```text
canonical explicit diagram
```

として扱う。

viewer は Markdown に存在する Mermaid を描画するのみ。

```markdown
```mermaid
graph TD
```
```

viewer は以下を行わない。

```text
- graph synthesis
- relationship inference
- graph mutation
```

---

## 6. Architecture Boundary

### markdown_viewer

```text
Browse Layer
```

### html_generator

```text
Generate Layer
```

### Runtime

```text
Separate Responsibility
```

Browse / Generate / Runtime を混在させない。

---

## 7. Expected Directory Structure

```text
tools/markdown_viewer/
├── README.md
├── viewer.js
├── viewer.css
├── viewer_template.py
├── templates/
│   └── viewer.html
├── assets/
│   ├── css/
│   └── js/
└── examples/
```

---

## 8. JavaScript Design Principle

viewer.js は：

```text
UI interaction helper
```

に限定する。

禁止例：

```text
- RuntimeManager
- ProjectionEngine
- CapabilityRegistry
- RendererPipeline
```

---

## 9. CSS Design Principle

viewer.css は document readability を優先する。

### 推奨

```text
- readable typography
- sticky TOC
- code readability
- Mermaid readability
- mobile readability
```

### 非目標

```text
runtime visualization dashboard
```

---

## 10. Performance Goal

viewer は lightweight を維持する。

### 目的

```text
single document fast render
```

### 非目的

```text
runtime scalability
```

---

## 11. Final Principle

markdown_viewer は：

```text
Document Browser
```

に徹する。

Operational Runtime 化しない。
