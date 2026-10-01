# Vista Digital V2 — strategy-aligned preview

32 responsive pages implementing ATTRACT → CONVERT → GROW, business-led solutions and the project → growth retainer → growth partnership ladder.

Build from the repository root: `python3 src/build-pages.py`.

GitHub Pages serves `docs/`. The preview is excluded from search crawling. Canonical URLs use the preview domain and must change at production launch.

Growth Assessment V2: website URL → animated demo checks → five progressively revealed scores → calculated Digital Growth Score and illustrative opportunity count → “Get My Full Assessment” → contact details and reviewed email follow-up. Deterministic values are explicitly simulated and are not website findings. `src/assessment.js` isolates the provider contract for a future backend adapter. No live scan, automatic submission, CRM capture or browser storage is configured. Reduced motion disables animation and shortens the staged wait.

Build: `python3 src/build-pages.py`. Browser verification: run a local server serving `docs/` at `/vista-digital-v2-preview/`, then run `node verify-assessment.cjs` (Playwright runtime path is configured in that file). `VISTA_TEST_URL` can target the deployed preview.

Preserved versions: `pre-growth-assessment-v2` points to the previous published commit `1150f89ef738daa834d358ffbfc9ea943945fda7`; `pre-growth-assessment-v2-local` points to the improved pre-edit snapshot `cbf4b8b`. Both branches are on GitHub.

Team credentials and project results awaiting approval are marked with a visible 📌 placeholder. Portfolio categories and visuals remain grounded in Vista’s published portfolio; no performance results are invented.

Responsive WebP variants are included. Open Sans is self-hosted in compressed WOFF format under the included OFL license (345KB, down from 533KB).
