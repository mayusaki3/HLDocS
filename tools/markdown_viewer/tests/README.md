# markdown_viewer Tests

## Purpose

Validate architectural boundaries of markdown_viewer.

## Scope

Allowed:

```text
- render
- navigation
- source browsing
- Mermaid rendering
```

Not allowed:

```text
- runtime platform
- graph runtime
- projection runtime
- capability registry
- distributed synchronization
```

## Goal

Prevent Browse Layer from evolving into Runtime Layer.
