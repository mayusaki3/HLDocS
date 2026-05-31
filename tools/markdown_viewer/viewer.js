/*
 * HLDocS Markdown Viewer
 *
 * Responsibilities:
 * - markdown rendering
 * - TOC navigation
 * - hash navigation
 * - source/render toggle
 * - Mermaid rendering bootstrap
 *
 * Non-responsibilities:
 * - graph runtime
 * - projection runtime
 * - distributed synchronization
 * - capability registry
 * - runtime orchestration
 */

/**
 * Initialize lightweight markdown viewer.
 *
 * The viewer is intentionally limited to Browse responsibilities.
 */
export function initializeViewer() {
    initializeHashNavigation();
    initializeSourceToggle();
    initializeMermaid();
}

/**
 * Initialize document-local hash navigation.
 */
function initializeHashNavigation() {
    window.addEventListener("hashchange", () => {
        const hash = window.location.hash;

        if (!hash) {
            return;
        }

        const target = document.querySelector(hash);

        if (target) {
            target.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
        }
    });
}

/**
 * Initialize render/source toggle.
 */
function initializeSourceToggle() {
    const toggle = document.querySelector("[data-view-toggle]");

    if (!toggle) {
        return;
    }

    toggle.addEventListener("click", () => {
        document.body.classList.toggle("source-visible");
    });
}

/**
 * Initialize Mermaid rendering.
 *
 * Mermaid blocks are treated as canonical explicit diagrams.
 */
function initializeMermaid() {
    if (!window.mermaid) {
        return;
    }

    window.mermaid.initialize({
        startOnLoad: true
    });
}
